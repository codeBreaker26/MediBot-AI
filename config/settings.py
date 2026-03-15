import os
from dotenv import load_dotenv

load_dotenv()

# Gemini Developer API via Google's OpenAI-compatible endpoint.
GEMINI_API_KEY = os.getenv("GEMINI_API_KEY") or os.getenv("GOOGLE_API_KEY")
GEMINI_MODEL = os.getenv("GEMINI_MODEL", "gemini-2.5-flash")
GEMINI_BASE_URL = os.getenv(
    "GEMINI_BASE_URL",
    "https://generativelanguage.googleapis.com/v1beta/openai/",
)
GEMINI_MAX_TOKENS = int(os.getenv("GEMINI_MAX_TOKENS", 512))
GEMINI_TEMPERATURE = float(os.getenv("GEMINI_TEMPERATURE", 0.4))

# Pinecone
PINECONE_API_KEY = os.getenv("PINECONE_API_KEY")
PINECONE_HOST = os.getenv("PINECONE_HOST", "https://medical-chatbot-pv4ded8.svc.aped-4627-b74a.pinecone.io")
PINECONE_INDEX_NAME = os.getenv("PINECONE_INDEX_NAME", "medical-chatbot")

# Embeddings
EMBEDDING_MODEL = os.getenv("EMBEDDING_MODEL", "sentence-transformers/all-MiniLM-L6-v2")

# Retrieval
RETRIEVAL_TOP_K = int(os.getenv("RETRIEVAL_TOP_K", "3"))
