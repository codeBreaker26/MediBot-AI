import streamlit as st
from pinecone import Pinecone
from langchain_pinecone import PineconeVectorStore
from config.settings import PINECONE_API_KEY, PINECONE_HOST, RETRIEVAL_TOP_K
from core.embeddings import get_embeddings


@st.cache_resource(show_spinner=False)
def get_vectorstore() -> PineconeVectorStore:
    if not PINECONE_API_KEY:
        raise ValueError("PINECONE_API_KEY is not set in your .env / Secrets.")
    pc = Pinecone(api_key=PINECONE_API_KEY)
    index = pc.Index(host=PINECONE_HOST)
    embeddings = get_embeddings()
    return PineconeVectorStore(index=index, embedding=embeddings, text_key="text")


def get_retriever():
    return get_vectorstore().as_retriever(search_kwargs={"k": RETRIEVAL_TOP_K})
