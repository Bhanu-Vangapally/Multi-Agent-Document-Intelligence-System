import streamlit as st
import tempfile
import json
import pandas as pd
import requests

from rag_store import load_pdf
from memory import init_memory

st.set_page_config(page_title="Deep Document Intelligence")

st.title("Multi-Agent Deep Document Intelligence System")
st.markdown("Upload long PDF documents and extract structured insights.")

if "memory" not in st.session_state:
    st.session_state.memory = init_memory()

pdf_file = st.file_uploader("Upload a Document PDF", type=["pdf"])

if pdf_file and st.button("Run Multi-Agent Analysis"):

    with st.spinner("Agents are analyzing your document..."):

        with tempfile.NamedTemporaryFile(delete=False, suffix=".pdf") as f:
            f.write(pdf_file.read())
            path = f.name
        docs = load_pdf(path)
        document_text = "\n".join([d.page_content for d in docs])

        st.session_state.memory["document_text"] = document_text

        try:
            api_url = "http://localhost:8000/analyze"
            response = requests.post(api_url, json={"document_text": document_text})
            
            if response.status_code == 200:
                output = response.json()
                st.success("✅ Multi-Agent Analysis Complete!")

                st.divider()
                st.subheader("Summary Output")
                st.write(output.get("summary", "No summary provided."))
                st.divider()
                st.subheader("Action Items Table")

                actions = output.get("action_items", [])
                if actions:
                    action_df = pd.DataFrame(actions)
                    st.dataframe(action_df)
                else:
                    st.info("No action items found.")

                st.divider()
                st.subheader("Risks & Open Issues")

                risks = output.get("risks_and_open_issues", {})

                st.markdown("**Open Questions**")
                for q in risks.get("open_questions", []):
                    st.markdown(f"- {q}")

                st.divider()

                st.markdown("**Risks**")
                for r in risks.get("risks", []):
                    st.markdown(f"- {r}")

                st.divider()

                st.markdown("**Assumptions**")
                for a in risks.get("assumptions", []):
                    st.markdown(f"- {a}")


                st.divider()

                st.subheader("Agent Communication Log")

                agent_messages = output.get("agent_messages", [])

                for msg in agent_messages:
                    st.markdown(f"**{msg.get('from', 'Agent')}**")
                    st.markdown(msg.get("message", ""))
                    st.divider()


                st.divider()
                st.subheader("Download Full JSON Report")

                json_str = json.dumps(output, indent=4)

                st.download_button(
                    label="Download Report as JSON",
                    data=json_str,
                    file_name="deep_document_report.json",
                    mime="application/json"
                )
            else:
                st.error(f"Backend Error: {response.status_code} - {response.text}")

        except Exception as e:
            st.error(f"Failed to connect to backend: {e}")
