import streamlit as st
from langchain_openai import ChatOpenAI
from langchain_core.prompts import ChatPromptTemplate
from langchain_core.output_parsers import StrOutputParser
from config.settings import (
    GEMINI_API_KEY,
    GEMINI_BASE_URL,
    GEMINI_MAX_TOKENS,
    GEMINI_MODEL,
    GEMINI_TEMPERATURE,
)
from core.vectorstore import get_retriever


PROMPT_TEMPLATE = """You are MediBotIQ, a knowledgeable and empathetic medical information assistant.
Use ONLY the context retrieved from the medical knowledge base below to answer the question.

Rules:
- If the context does not contain enough information, say so clearly, never fabricate medical facts.
- Be concise but complete. Use plain language a patient would understand.
- For serious symptoms, always recommend seeing a doctor.
- Never diagnose. Never prescribe. Inform only.

Conversation so far:
{chat_history}

Retrieved medical context:
{context}

Patient's question: {question}

Your response:"""


def format_chat_history(history: list) -> str:
    if not history:
        return "None"
    lines = []
    for msg in history[-6:]:
        if "user" in msg:
            lines.append(f"Patient: {msg['user']}")
        elif "bot" in msg:
            lines.append(f"MediBotIQ: {msg['bot']}")
    return "\n".join(lines)


def format_docs(docs) -> str:
    return "\n\n".join(doc.page_content for doc in docs)


@st.cache_resource(show_spinner=False)
def get_llm():
    if not GEMINI_API_KEY:
        raise ValueError("GEMINI_API_KEY is not set in your .env / Secrets.")

    # Gemini exposes an OpenAI-compatible endpoint, which lets us keep the
    # existing LangChain chat chain with only configuration changes.
    return ChatOpenAI(
        model=GEMINI_MODEL,
        api_key=GEMINI_API_KEY,
        base_url=GEMINI_BASE_URL,
        max_tokens=GEMINI_MAX_TOKENS,
        temperature=GEMINI_TEMPERATURE,
    )


def get_answer(user_query: str, chat_history: list) -> tuple:
    try:
        llm = get_llm()
        retriever = get_retriever()
        # Fetch documents using whichever retriever API is available.
        def fetch_docs(retriever, query, k=3):
            try:
                if hasattr(retriever, "get_relevant_documents"):
                    return retriever.get_relevant_documents(query)
                if hasattr(retriever, "aget_relevant_documents"):
                    import asyncio

                    return asyncio.run(retriever.aget_relevant_documents(query))
                if hasattr(retriever, "similarity_search"):
                    try:
                        return retriever.similarity_search(query, k)
                    except TypeError:
                        return retriever.similarity_search(query)
                if hasattr(retriever, "get_documents"):
                    return retriever.get_documents(query)
                if callable(retriever):
                    return retriever(query)
            except Exception:
                return []
            return []

        docs = fetch_docs(retriever, user_query)
        context = format_docs(docs)
        prompt = ChatPromptTemplate.from_template(PROMPT_TEMPLATE)
        chain = prompt | llm | StrOutputParser()
        answer = chain.invoke({
            "question": user_query,
            "context": context,
            "chat_history": format_chat_history(chat_history),
        })
        return answer.strip(), docs
    except Exception as e:
        return f"⚠️ Something went wrong: {str(e)}", []
