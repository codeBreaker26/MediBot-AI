import os


def validate_env() -> list[str]:
    """Return list of missing required environment variables."""
    return [v for v in ["OPENAI_API_KEY", "PINECONE_API_KEY"] if not os.getenv(v)]


def needs_disclaimer(text: str) -> bool:
    """Return True if the answer contains specific medical content warranting a disclaimer."""
    triggers = ["dosage", "mg", "medication", "prescri", "diagnos", "treatment", "drug", "tablet", "inject"]
    return any(t in text.lower() for t in triggers)


def sanitize(query: str) -> str:
    return query.strip()
