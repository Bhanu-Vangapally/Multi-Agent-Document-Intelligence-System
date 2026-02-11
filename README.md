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

<img width="480" height="211" alt="image" src="https://github.com/user-attachments/assets/66a70a6f-6f37-49aa-9513-bd4039e59b41" />

---


---

## ⚙️ Local Setup

### 1️⃣ Clone Repository

```bash
git clone https://github.com/Bhanu-Vangapally/Multi-Agent-Document-Intelligence-System.git
cd Multi-Agent-Document-Intelligence-System

---

<img width="338" height="39" alt="image" src="https://github.com/user-attachments/assets/7a8a2526-f522-4a80-a71e-61b1349c7dc9" />

```bash
python -m venv venv
venv\Scripts\activate

---

<img width="272" height="46" alt="image" src="https://github.com/user-attachments/assets/967ba890-5b4d-478f-a04c-6b6fddae6492" />

```bash
pip install -r requirements.txt

---

<img width="403" height="79" alt="image" src="https://github.com/user-attachments/assets/349d4700-dcc5-4df8-9148-c75a93aca60f" />

```bash
OPENAI_API_KEY=your_api_key_here


