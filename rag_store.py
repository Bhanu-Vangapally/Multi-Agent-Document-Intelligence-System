import os
from dotenv import load_dotenv

load_dotenv()

if not os.getenv("OPENAI_API_KEY"):
    raise RuntimeError("OPENAI_API_KEY missing")


from langchain_openai import OpenAIEmbeddings
from langchain_text_splitters import RecursiveCharacterTextSplitter
from langchain_community.vectorstores import FAISS
from langchain_community.document_loaders import PyPDFLoader
from langchain_core.documents import Document


def load_pdf(path: str):
    loader = PyPDFLoader(path)
    return loader.load()


def build_vector_store(docs):
    if isinstance(docs, str):
        docs = [Document(page_content=docs)]

    splitter = RecursiveCharacterTextSplitter(
        chunk_size=800,
        chunk_overlap=250
    )

    chunks = splitter.split_documents(docs)

    embeddings = OpenAIEmbeddings()
    vectorstore = FAISS.from_documents(chunks, embeddings)

    return vectorstore


def rag_query(vectorstore, query: str):
    docs = vectorstore.similarity_search(query, k=7)
    return "\n".join([d.page_content for d in docs])