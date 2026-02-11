import uvicorn
from fastapi import FastAPI, HTTPException
from pydantic import BaseModel
from typing import List, Dict, Any, Optional


from ai_engine import orchestrator
from rag_store import build_vector_store, rag_query
from langchain_community.vectorstores import FAISS
from langchain_openai import OpenAIEmbeddings
from memory import init_memory

app = FastAPI(title="AI Engine API")

class AnalyzeRequest(BaseModel):
    document_text: str

class AnalyzeResponse(BaseModel):
    summary: str
    action_items: List[Dict[str, Any]]
    risks_and_open_issues: Dict[str, Any]
    agent_messages: List[Dict[str, Any]]

@app.post("/analyze", response_model=AnalyzeResponse)
async def analyze_document(request: AnalyzeRequest):
    try:
        document_text = request.document_text
        if not document_text:
            raise HTTPException(status_code=400, detail="Document text is empty")
        
        vectorstore = build_vector_store(document_text)
        
        memory = init_memory()
        result = orchestrator(document_text, vectorstore, memory)
        
        return AnalyzeResponse(
            summary=result.get("summary", ""),
            action_items=result.get("action_items", []),
            risks_and_open_issues=result.get("risks_and_open_issues", {}),
            agent_messages=result.get("agent_messages", [])
        )

    except Exception as e:
        import traceback
        traceback.print_exc()
        raise HTTPException(status_code=500, detail=str(e))
@app.get("/")
def home():
    return {"message": "AI Engine Backend Running"}

if __name__ == "__main__":
    uvicorn.run(app, host="0.0.0.0", port=8000)
