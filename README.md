---
title: MediBotIQ
emoji: 🩺
colorFrom: green
colorTo: blue
sdk: streamlit
sdk_version: 1.36.0
app_file: app.py
pinned: false
license: mit
---

<div align="center">

# 🩺 MediBotIQ
### AI-Powered Medical Information Assistant

[![Python](https://img.shields.io/badge/Python-3.11+-3776ab?style=flat-square&logo=python&logoColor=white)](https://python.org)
[![Streamlit](https://img.shields.io/badge/Streamlit-1.36-ff4b4b?style=flat-square&logo=streamlit&logoColor=white)](https://streamlit.io)
[![Gemini](https://img.shields.io/badge/Gemini-2.5%20Flash-4285f4?style=flat-square&logo=google&logoColor=white)](https://ai.google.dev)
[![Pinecone](https://img.shields.io/badge/Pinecone-Vector%20DB-000000?style=flat-square)](https://pinecone.io)
[![LangChain](https://img.shields.io/badge/LangChain-0.2-1c3c3c?style=flat-square)](https://langchain.com)
[![License: MIT](https://img.shields.io/badge/License-MIT-22c55e?style=flat-square)](LICENSE)

*Ask medical questions. Get grounded, knowledge-base-backed answers in seconds.*

</div>

---

## 📌 Overview

MediBotIQ is a **Retrieval-Augmented Generation (RAG) medical chatbot** built with a clean, modular architecture. It retrieves relevant context from a curated medical knowledge base stored in Pinecone, then uses Gemini 2.5 Flash to generate accurate, context-aware responses — all through a polished dark-themed Streamlit interface.

> ⚠️ **Disclaimer:** MediBotIQ provides general medical information only and is not a substitute for professional medical advice. Always consult a qualified healthcare provider for personal health concerns.

---

## ✨ Features

- 🔍 **RAG Pipeline** — Retrieves relevant chunks from a medical knowledge base before generating answers, grounding every response in real medical content
- ⚡ **Fast responses** — Gemini 2.5 Flash via the Gemini Developer API delivers answers in 1–3 seconds
- 🧠 **Conversation memory** — Maintains context across the last 3 exchanges for follow-up questions
- 📄 **Source transparency** — Every answer shows which pages of the knowledge base it was retrieved from
- 🛡️ **Smart disclaimers** — Automatically adds medical disclaimers when responses involve dosages, treatments, or prescriptions
- 🎨 **Clinical dark UI** — Custom-designed interface with Playfair Display typography and a professional medical aesthetic

---

## 🏗️ Architecture

```
User Query
    │
    ▼
HuggingFace Embeddings
(sentence-transformers/all-MiniLM-L6-v2)
    │
    ▼
Pinecone Vector Search ──► Top-3 relevant medical text chunks
    │
    ▼
Gemini 2.5 Flash (Google) ──► Grounded, context-aware answer
    │
    ▼
Streamlit UI (with sources + disclaimer)
```

---

## 🛠️ Tech Stack

| Layer | Technology |
|---|---|
| LLM | Gemini 2.5 Flash |
| Embeddings | sentence-transformers/all-MiniLM-L6-v2 |
| Vector Database | Pinecone |
| Orchestration | LangChain |
| UI | Streamlit |
| Language | Python 3.11 |

---

## 📂 Project Structure

```
MediBotIQ/
│
├── app.py                  # Streamlit UI — clean, thin layer only
│
├── core/
│   ├── chain.py            # LCEL chain — prompt + Gemini + output parser
│   ├── vectorstore.py      # Pinecone connection & retriever
│   └── embeddings.py       # HuggingFace embeddings (cached)
│
├── config/
│   └── settings.py         # All configuration loaded from .env
│
├── utils/
│   └── helpers.py          # Input sanitization & disclaimer logic
│
├── data/
│   └── Medical_book.pdf    # Medical knowledge base
│
├── ingest.py               # One-time script to upload PDF to Pinecone
├── .env.example            # Environment variable template
├── requirements.txt        # Python dependencies
└── README.md
```

---
🚀 Live Demo

Try the deployed application here:

👉 https://medibot-ai-me9ncrwuwnyusjcbwkkw3b.streamlit.app/

## ⚡ Local Setup

### 1. Clone the repository
```bash
git clone https://github.com/codeBreaker26/MediBotIQ
cd MediBotIQ
```

### 2. Create a virtual environment
```bash
python3.11 -m venv venv
source venv/bin/activate       # Mac/Linux
# venv\Scripts\activate        # Windows
```

### 3. Install dependencies
```bash
pip install -r requirements.txt
```

### 4. Configure environment variables
```bash
cp .env.example .env
```
Open `.env` and fill in your keys:
```
GEMINI_API_KEY=...
PINECONE_API_KEY=...
PINECONE_HOST=https://your-index-host.pinecone.io
```

### 5. Ingest the knowledge base (run once)
```bash
python ingest.py
```
This uploads the medical PDF into your Pinecone index. Only needs to be run once.

### 6. Run the app
```bash
streamlit run app.py
```
Open http://localhost:8501 in your browser.

---

## 🤝 Contributing

Contributions are welcome!

```bash
# Fork the repo, then:
git checkout -b feature/your-feature
git commit -m "Add your feature"
git push origin feature/your-feature
# Open a Pull Request
```

---

## 📜 License

This project is licensed under the MIT License.

---

<div align="center">

Developed by **Ishan Sahani**

[GitHub](https://github.com/codeBreaker26)

If you found this useful, consider giving it a star ⭐

</div>
