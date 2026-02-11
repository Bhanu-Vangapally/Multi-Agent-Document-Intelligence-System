# 🚀 Multi-Agent Deep Document Intelligence System

![Python](https://img.shields.io/badge/Python-3.10+-blue.svg)
![FastAPI](https://img.shields.io/badge/FastAPI-Backend-green)
![Streamlit](https://img.shields.io/badge/Streamlit-Frontend-red)
![OpenAI](https://img.shields.io/badge/OpenAI-LLM-orange)
![RAG](https://img.shields.io/badge/Architecture-RAG-purple)
![Deployment](https://img.shields.io/badge/Deployment-Render-black)

An AI-powered document intelligence platform that uses **Multi-Agent Orchestration + Retrieval Augmented Generation (RAG)** to transform complex documents into structured, actionable insights.

---

## 🌐 Live Demo

🔹 **Frontend:** https://ai-engine-frontend-zcyx.onrender.com  
🔹 **API Docs:** https://ai-engine-backend-hnq7.onrender.com/docs  

---

## ✨ Key Features

- 🤖 Multi-Agent AI System  
- 📄 Context-Aware Summarization  
- 📋 Action Item & Dependency Extraction  
- ⚠️ Risk & Open Issue Detection  
- 🔍 Vector Search with FAISS  
- 🧠 Dynamic Model Selection  
- 📊 Interactive Streamlit UI  
- 🔐 Secure Environment-Based Configuration  
- ☁️ Production Deployment on Render  

---

## 🧠 System Architecture

            ┌────────────────────┐
            │   User Uploads PDF │
            └───────────┬────────┘
                        ↓
            ┌────────────────────┐
            │  Streamlit Frontend│
            └───────────┬────────┘
                        ↓
            ┌────────────────────┐
            │  FastAPI Backend   │
            └───────────┬────────┘
                        ↓
    ┌──────────────────────────────────┐
    │   RAG Pipeline (FAISS + Embeds) │
    └───────────┬───────────┬─────────┘
                ↓           ↓
       Summary Agent   Action Agent
                ↓           ↓
            Risk Agent  ←─────────
                ↓
    ┌────────────────────────────┐
    │ Structured JSON Output     │
    └────────────────────────────┘

---

## 🛠️ Tech Stack

### 🔹 Backend
- FastAPI
- LangChain
- OpenAI GPT Models
- FAISS Vector Store
- Python

### 🔹 Frontend
- Streamlit
- Pandas
- Requests

### 🔹 AI Architecture
- Multi-Agent Orchestration
- Retrieval Augmented Generation (RAG)
- Vector Similarity Search

### 🔹 Deployment
- Render Cloud
- Environment Variable Secret Management

---

## 📂 Project Structure

├── api_server.py # FastAPI API endpoints
├── ai_engine.py # Multi-agent orchestration logic
├── rag_store.py # RAG pipeline & vector store
├── memory.py # Agent memory handling
├── app.py # Streamlit frontend
├── requirements.txt # Project dependencies


---

## ⚙️ Local Setup

### 1️⃣ Clone Repository

```bash
git clone https://github.com/Bhanu-Vangapally/Multi-Agent-Document-Intelligence-System.git
cd Multi-Agent-Document-Intelligence-System
2️⃣ Create Virtual Environment
python -m venv venv
venv\Scripts\activate

3️⃣ Install Dependencies
pip install -r requirements.txt

4️⃣ Configure Environment Variables

Create .env file:

OPENAI_API_KEY=your_api_key_here

5️⃣ Run Backend
uvicorn api_server:app --reload

6️⃣ Run Frontend
streamlit run app.py

📊 Output Generated

The system produces:

📌 Executive Summary

📋 Structured Action Items (with dependencies)

⚠️ Risk & Assumption Analysis

💬 Agent Communication Log

🎯 Use Cases

Business Meeting Intelligence

Legal & Policy Review

Project Planning Automation

Enterprise Knowledge Mining

Research Paper Analysis

🚀 Deployment

Deployed using Render Cloud Platform:

FastAPI backend service

Streamlit frontend service

Secure environment variable configuration

Production-ready microservice architecture

📈 Future Enhancements

User Authentication

Persistent Database Storage

Multi-document batch processing

Dashboard analytics visualization

Docker containerization

👨‍💻 Author

Bhanu Vangapally
GitHub: https://github.com/Bhanu-Vangapally

⭐ Support

If you find this project useful, please give it a ⭐ on GitHub!
