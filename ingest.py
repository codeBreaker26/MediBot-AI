"""
ingest.py — Run this ONCE to upload Medical_book.pdf into your Pinecone index.
After it finishes, you never need to run it again.

Usage:
    python ingest.py
"""

import os
from dotenv import load_dotenv
from langchain_community.document_loaders import PyPDFLoader
from langchain.text_splitter import RecursiveCharacterTextSplitter
from langchain_community.embeddings import HuggingFaceEmbeddings
from pinecone import Pinecone, ServerlessSpec

load_dotenv()

PINECONE_API_KEY   = os.getenv("PINECONE_API_KEY")
PINECONE_HOST      = os.getenv("PINECONE_HOST")
INDEX_NAME         = os.getenv("PINECONE_INDEX_NAME", "medical-chatbot")
PDF_PATH           = "data/Medical_book.pdf"
EMBEDDING_MODEL    = "sentence-transformers/all-MiniLM-L6-v2"
CHUNK_SIZE         = 500
CHUNK_OVERLAP      = 50
BATCH_SIZE         = 100  # upload 100 vectors at a time

def main():
    print("=" * 50)
    print("MediBotIQ — Pinecone Ingestion Script")
    print("=" * 50)

    # ── 1. Load PDF ───────────────────────────────
    print(f"\n[1/4] Loading PDF from '{PDF_PATH}'...")
    loader = PyPDFLoader(PDF_PATH)
    documents = loader.load()
    print(f"      Loaded {len(documents)} pages.")

    # ── 2. Split into chunks ──────────────────────
    print(f"\n[2/4] Splitting into chunks (size={CHUNK_SIZE}, overlap={CHUNK_OVERLAP})...")
    splitter = RecursiveCharacterTextSplitter(
        chunk_size=CHUNK_SIZE,
        chunk_overlap=CHUNK_OVERLAP,
    )
    chunks = splitter.split_documents(documents)
    print(f"      Created {len(chunks)} chunks.")

    # ── 3. Load embedding model ───────────────────
    print(f"\n[3/4] Loading embedding model '{EMBEDDING_MODEL}'...")
    print("      (First time may take a minute to download ~90MB)")
    embeddings = HuggingFaceEmbeddings(
        model_name=EMBEDDING_MODEL,
        model_kwargs={"device": "cpu"},
        encode_kwargs={"normalize_embeddings": True},
    )
    print("      Embedding model ready.")

    # ── 4. Upload to Pinecone ─────────────────────
    print(f"\n[4/4] Uploading vectors to Pinecone index '{INDEX_NAME}'...")
    pc = Pinecone(api_key=PINECONE_API_KEY)
    index = pc.Index(host=PINECONE_HOST)

    # Upload in batches
    total = len(chunks)
    for i in range(0, total, BATCH_SIZE):
        batch = chunks[i : i + BATCH_SIZE]
        texts = [doc.page_content for doc in batch]
        metadatas = [{"page": doc.metadata.get("page", 0), "source": PDF_PATH} for doc in batch]

        # Generate embeddings for this batch
        vectors = embeddings.embed_documents(texts)

        # Format for Pinecone upsert
        upsert_data = [
            {
                "id": f"chunk-{i + j}",
                "values": vectors[j],
                "metadata": {**metadatas[j], "text": texts[j]},
            }
            for j in range(len(batch))
        ]

        index.upsert(vectors=upsert_data)
        print(f"      Uploaded {min(i + BATCH_SIZE, total)}/{total} chunks...")

    print("\n✅ Done! Your Pinecone index is ready.")
    print("   You can now run: streamlit run app.py")
    print("=" * 50)


if __name__ == "__main__":
    main()