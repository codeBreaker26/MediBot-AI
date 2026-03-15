import os
import streamlit as st
from dotenv import load_dotenv

load_dotenv()

def get_env(key, default=None):
    return os.getenv(key) or st.secrets.get(key, default)


# Gemini
GEMINI_API_KEY = get_env("GEMINI_API_KEY") or get_env("GOOGLE_API_KEY")
GEMINI_MODEL = get_env("GEMINI_MODEL", "gemini-2.5-flash")
GEMINI_BASE_URL = get_env(
    "GEMINI_BASE_URL",
    "https://generativelanguage.googleapis.com/v1beta/openai/",
)
GEMINI_MAX_TOKENS = int(get_env("GEMINI_MAX_TOKENS", 512))
GEMINI_TEMPERATURE = float(get_env("GEMINI_TEMPERATURE", 0.4))

# Pinecone
PINECONE_API_KEY = get_env("PINECONE_API_KEY")
PINECONE_HOST = get_env(
    "PINECONE_HOST",
    "https://medical-chatbot-pv4ded8.svc.aped-4627-b74a.pinecone.io"
)
PINECONE_INDEX_NAME = get_env("PINECONE_INDEX_NAME", "medical-chatbot")

# Embeddings
EMBEDDING_MODEL = get_env(
    "EMBEDDING_MODEL",
    "sentence-transformers/all-MiniLM-L6-v2"
)

# Retrieval
RETRIEVAL_TOP_K = int(get_env("RETRIEVAL_TOP_K", 3))
