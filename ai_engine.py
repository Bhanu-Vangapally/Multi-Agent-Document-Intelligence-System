import os
import json
from typing import Any

from dotenv import load_dotenv
import os
load_dotenv()

api_key = os.getenv("OPENAI_API_KEY")
if not os.getenv("OPENAI_API_KEY"):
    raise ValueError("OPENAI_API_KEY not found in environment variables")

from langchain_openai import ChatOpenAI
from langchain_core.messages import HumanMessage

from langchain.agents import create_agent
from langchain.agents.middleware import (
    before_model,
    AgentState,
)
from langgraph.runtime import Runtime

from rag_store import rag_query

basic_model = ChatOpenAI(
    model="gpt-4o-mini",
    temperature=0.2,
    streaming=True,
)

advanced_model = ChatOpenAI(
    model="gpt-4o",
    temperature=0.2,
    streaming=True,
)

@before_model
def dynamic_model_selection(
    state: AgentState,
    runtime: Runtime,
) -> dict[str, Any] | None:
    messages = state.get("messages", [])
    total_chars = sum(
        len(m.content)
        for m in messages
        if hasattr(m, "content") and isinstance(m.content, str)
    )

    if total_chars > 5000:
        return {"model": advanced_model}

    return {"model": basic_model}


def safe_json_load(raw_text: str | None):
    if not raw_text or not raw_text.strip():
        return None

    try:
        return json.loads(raw_text)
    except Exception:
        pass

    start, end = raw_text.find("["), raw_text.rfind("]")
    if start != -1 and end != -1:
        try:
            return json.loads(raw_text[start : end + 1])
        except Exception:
            pass

    start, end = raw_text.find("{"), raw_text.rfind("}")
    if start != -1 and end != -1:
        try:
            return json.loads(raw_text[start : end + 1])
        except Exception:
            pass

    return None


def add_agent_message(memory, agent_name, content):
    memory["agent_messages"].append({
        "from": agent_name,
        "message": content.strip(),
    })


summary_agent_runner = create_agent(
    model=basic_model,
    middleware=[dynamic_model_selection, ],
    name="SummaryAgent",
)

action_agent_runner = create_agent(
    model=basic_model,
    middleware=[dynamic_model_selection, ],
    name="ActionAgent",
)

risk_agent_runner = create_agent(
    model=basic_model,
    middleware=[dynamic_model_selection, ],
    name="RiskAgent",
)

def summary_agent(document_text, vectorstore, memory):
    context = rag_query(vectorstore, "key decisions constraints deadlines")

    prompt = f"""
You are the Context-Aware Summary Agent.

Document Evidence:
{context}

Task:
Write a concise summary preserving:
- intent
- constraints
- critical decisions

Return ONLY summary text.
"""

    state = summary_agent_runner.invoke({"messages": [HumanMessage(content=prompt)]})

    messages = state.get("messages", [])
    summary = messages[-1].content.strip() if messages else ""

    memory["summary"] = summary

    meta_prompt = f"""
You are an internal communicator agent.

Based on this summary:

{summary}

Extract 3 key constraints or decisions
that downstream agents must know.

Return bullet points only.
"""

    notes_state = summary_agent_runner.invoke(
        {"messages": [HumanMessage(content=meta_prompt)]}
    )

    notes = notes_state["messages"][-1].content.strip()
    add_agent_message(memory, "SummaryAgent", notes)

    return summary


def action_extraction_agent(document_text, vectorstore, memory):
    context = rag_query(vectorstore, "tasks responsibilities deadlines action items")

    summary_notes = memory["agent_messages"][0]["message"]

    prompt = f"""
You are the Action & Dependency Extraction Agent.

Important context from SummaryAgent:
{summary_notes}

Document Evidence:
{context}

Task:
Extract actionable tasks WITH dependencies.

Rules:
- Dependencies MUST NOT be empty if another task must happen first.
- If a task has no dependencies, its "dependencies" field must be an empty list: [].
- Infer dependencies logically (approval → execution, logs → assessment, etc.)
- Output must be valid JSON ONLY.

Return JSON list:

[
  {{
    "task": "...",
    "owner": "... or null",
    "deadline": "... or null",
    "dependencies": ["Task X", "Task Y"]
  }}
]
"""


    state = action_agent_runner.invoke({"messages": [HumanMessage(content=prompt)]})

    raw = state["messages"][-1].content
    actions = safe_json_load(raw) or []

    memory["actions"] = actions

    dep_prompt = f"""
You are the ActionAgent communicator.

These are extracted tasks:

{actions}

Generate 2-3 bullet points explaining:
- most important dependency chain
- most urgent blocker task

Return bullet points only.
"""

    dep_state = action_agent_runner.invoke(
        {"messages": [HumanMessage(content=dep_prompt)]}
    )

    dep_notes = dep_state["messages"][-1].content.strip()
    add_agent_message(memory, "ActionAgent", dep_notes)

    return actions


def risk_agent(document_text, vectorstore, memory):
    context = rag_query(vectorstore, "risks unresolved issues missing information")

    action_notes = memory["agent_messages"][1]["message"]

    prompt = f"""
You are the Risk & Open-Issues Agent.

Important dependency warnings from ActionAgent:
{action_notes}

Document Evidence:
{context}

Task:
Identify:
- unresolved questions
- risks
- assumptions

Return ONLY valid JSON object:

{{
  "open_questions": ["..."],
  "risks": ["..."],
  "assumptions": ["..."]
}}
"""

    state = risk_agent_runner.invoke({"messages": [HumanMessage(content=prompt)]})

    raw = state["messages"][-1].content
    risks = safe_json_load(raw) or {
        "open_questions": [],
        "risks": [],
        "assumptions": [],
    }

    memory["risks"] = risks

    risk_prompt = f"""
You are the RiskAgent communicator.

Given these risks:

{risks}

Send:
- top 2 urgent risks
- 1 critical unresolved question

Return bullet points only.
"""

    risk_state = risk_agent_runner.invoke(
        {"messages": [HumanMessage(content=risk_prompt)]}
    )

    risk_notes = risk_state["messages"][-1].content.strip()
    add_agent_message(memory, "RiskAgent", risk_notes)

    return risks



def orchestrator(document_text, vectorstore, memory):
    memory["agent_messages"] = []

    summary = summary_agent(document_text, vectorstore, memory)
    actions = action_extraction_agent(document_text, vectorstore, memory)
    risks = risk_agent(document_text, vectorstore, memory)

    final_output = {
        "summary": summary,
        "action_items": actions,
        "risks_and_open_issues": risks,
        "agent_messages": memory["agent_messages"],
    }

    memory["final_output"] = final_output
    return final_output
