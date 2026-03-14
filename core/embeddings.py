import streamlit as st
# Prefer LangChain's HuggingFaceEmbeddings when available, otherwise fall back
# to a lightweight SentenceTransformers wrapper so the app still works.
try:
    from langchain.embeddings import HuggingFaceEmbeddings
except Exception:
    try:
        from langchain_community.embeddings import HuggingFaceEmbeddings
    except Exception:
        HuggingFaceEmbeddings = None

from config.settings import EMBEDDING_MODEL


@st.cache_resource(show_spinner=False)
def get_embeddings():
    """Return an embeddings object compatible with LangChain's vectorstores.

    If LangChain's HuggingFaceEmbeddings is available, use it. Otherwise
    instantiate a small wrapper around `sentence-transformers`.
    """
    if HuggingFaceEmbeddings is not None:
        return HuggingFaceEmbeddings(
            model_name=EMBEDDING_MODEL,
            model_kwargs={"device": "cpu"},
            encode_kwargs={"normalize_embeddings": True},
        )

    # Fallback: use sentence-transformers directly
    try:
        from sentence_transformers import SentenceTransformer
        import numpy as np
    except Exception as e:
        raise ImportError(
            "No HuggingFaceEmbeddings found and sentence-transformers is not installed: "
            + str(e)
        )

    class STWrapper:
        def __init__(self, model_name: str):
            self.model = SentenceTransformer(model_name)

        def embed_documents(self, texts):
            arr = self.model.encode(texts, convert_to_numpy=True)
            # ensure 2D
            if arr.ndim == 1:
                arr = np.expand_dims(arr, 0)
            return [list(x) for x in arr.tolist()]

        def embed_query(self, text: str):
            vec = self.model.encode([text], convert_to_numpy=True)[0]
            return list(vec.tolist())

    return STWrapper(EMBEDDING_MODEL)
