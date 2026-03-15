import os


def validate_env() -> list[str]:
    """Return list of missing required environment variables."""
    missing = []

    if not (os.getenv("GEMINI_API_KEY") or os.getenv("GOOGLE_API_KEY")):
        missing.append("GEMINI_API_KEY")
    if not os.getenv("PINECONE_API_KEY"):
        missing.append("PINECONE_API_KEY")

    return missing


def needs_disclaimer(text: str) -> bool:
    """Return True if the answer contains specific medical content warranting a disclaimer."""
    triggers = ["dosage", "mg", "medication", "prescri", "diagnos", "treatment", "drug", "tablet", "inject"]
    return any(t in text.lower() for t in triggers)


def sanitize(query: str) -> str:
    return query.strip()
