import streamlit as st
from core.chain import get_answer
from config.settings import GEMINI_MODEL
from utils.helpers import validate_env, sanitize, needs_disclaimer

# ── Page config ───────────────────────────────────────────────────────────────
st.set_page_config(
    page_title="MediBotIQ",
    page_icon="🩺",
    layout="wide",
    initial_sidebar_state="expanded",
)

# ── Styles ────────────────────────────────────────────────────────────────────
st.markdown("""
<style>
@import url('https://fonts.googleapis.com/css2?family=Playfair+Display:wght@600&family=IBM+Plex+Sans:wght@300;400;500&family=IBM+Plex+Mono:wght@400&display=swap');

:root {
    --bg:        #0d1117;
    --surface:   #161b22;
    --border:    #21262d;
    --accent:    #2ea87e;
    --accent2:   #1a7a5e;
    --text:      #e6edf3;
    --muted:     #7d8590;
    --warn:      #d29922;
    --warn-bg:   #1c1810;
    --error:     #f85149;
    --user-bg:   #1c2128;
    --bot-bg:    #161b22;
}

/* ── Base ── */
html, body, [class*="css"] {
    font-family: 'IBM Plex Sans', sans-serif !important;
    background: var(--bg) !important;
    color: var(--text) !important;
}

.stApp { background: var(--bg) !important; }

/* ── Sidebar ── */
section[data-testid="stSidebar"] {
    background: var(--surface) !important;
    border-right: 1px solid var(--border) !important;
}
section[data-testid="stSidebar"] * { color: var(--text) !important; }
section[data-testid="stSidebar"] hr { border-color: var(--border) !important; }

/* ── Header ── */
.medibot-header {
    display: flex;
    align-items: center;
    gap: 14px;
    padding: 8px 0 24px 0;
    border-bottom: 1px solid var(--border);
    margin-bottom: 24px;
}
.medibot-cross {
    width: 44px; height: 44px;
    background: var(--accent);
    border-radius: 10px;
    display: flex; align-items: center; justify-content: center;
    font-size: 22px;
    flex-shrink: 0;
    box-shadow: 0 0 20px rgba(46,168,126,0.3);
}
.medibot-title {
    font-family: 'Playfair Display', serif !important;
    font-size: 1.85rem !important;
    color: var(--text) !important;
    line-height: 1.1;
    margin: 0;
}
.medibot-subtitle {
    font-size: 0.8rem;
    color: var(--muted);
    font-weight: 300;
    letter-spacing: 0.04em;
    text-transform: uppercase;
}

/* ── Status badge ── */
.status-badge {
    display: inline-flex;
    align-items: center;
    gap: 6px;
    background: rgba(46,168,126,0.1);
    border: 1px solid rgba(46,168,126,0.3);
    border-radius: 20px;
    padding: 3px 10px;
    font-size: 0.75rem;
    color: var(--accent);
    margin-bottom: 20px;
    font-family: 'IBM Plex Mono', monospace;
}
.status-dot {
    width: 6px; height: 6px;
    background: var(--accent);
    border-radius: 50%;
    animation: pulse 2s infinite;
}
@keyframes pulse {
    0%, 100% { opacity: 1; }
    50% { opacity: 0.3; }
}

/* ── Chat messages ── */
[data-testid="stChatMessage"] {
    background: transparent !important;
    border: none !important;
    padding: 4px 0 !important;
}

/* User bubble */
[data-testid="stChatMessage"]:has([data-testid="stChatMessageAvatarUser"]) {
    background: var(--user-bg) !important;
    border: 1px solid var(--border) !important;
    border-radius: 12px !important;
    padding: 12px 16px !important;
    margin: 6px 0 !important;
}

/* Bot bubble */
[data-testid="stChatMessage"]:has([data-testid="stChatMessageAvatarAssistant"]) {
    background: var(--bot-bg) !important;
    border: 1px solid var(--border) !important;
    border-radius: 12px !important;
    padding: 12px 16px !important;
    margin: 6px 0 !important;
}

[data-testid="stChatMessageContent"] p {
    font-size: 0.95rem !important;
    line-height: 1.75 !important;
    color: var(--text) !important;
}

/* ── Input ── */
[data-testid="stChatInput"] {
    border-top: 1px solid var(--border) !important;
    padding-top: 12px !important;
}
[data-testid="stChatInput"] textarea {
    background: var(--surface) !important;
    border: 1px solid var(--border) !important;
    border-radius: 10px !important;
    color: var(--text) !important;
    font-family: 'IBM Plex Sans', sans-serif !important;
    font-size: 0.92rem !important;
}
[data-testid="stChatInput"] textarea:focus {
    border-color: var(--accent) !important;
    box-shadow: 0 0 0 2px rgba(46,168,126,0.15) !important;
}
[data-testid="stChatInput"] textarea::placeholder { color: var(--muted) !important; }

/* ── Disclaimer ── */
.disclaimer {
    background: var(--warn-bg);
    border-left: 3px solid var(--warn);
    border-radius: 0 8px 8px 0;
    padding: 8px 12px;
    font-size: 0.78rem;
    color: var(--warn);
    margin-top: 10px;
    font-family: 'IBM Plex Mono', monospace;
}

/* ── Source expander ── */
.streamlit-expanderHeader {
    background: transparent !important;
    color: var(--muted) !important;
    font-size: 0.78rem !important;
    font-family: 'IBM Plex Mono', monospace !important;
    border: 1px solid var(--border) !important;
    border-radius: 6px !important;
}
.streamlit-expanderContent {
    background: var(--surface) !important;
    border: 1px solid var(--border) !important;
    border-top: none !important;
    border-radius: 0 0 6px 6px !important;
}

/* ── Source card ── */
.source-card {
    background: var(--bg);
    border: 1px solid var(--border);
    border-radius: 8px;
    padding: 10px 14px;
    margin-bottom: 8px;
    font-size: 0.8rem;
    color: var(--muted);
    font-family: 'IBM Plex Mono', monospace;
}
.source-card strong { color: var(--accent); }

/* ── Error box ── */
.env-error {
    background: rgba(248,81,73,0.08);
    border: 1px solid rgba(248,81,73,0.4);
    border-radius: 10px;
    padding: 14px 18px;
    color: var(--error);
    font-size: 0.88rem;
}

/* ── Buttons ── */
.stButton > button {
    background: transparent !important;
    border: 1px solid var(--border) !important;
    color: var(--muted) !important;
    border-radius: 8px !important;
    font-family: 'IBM Plex Sans', sans-serif !important;
    font-size: 0.82rem !important;
    transition: all 0.15s ease !important;
}
.stButton > button:hover {
    border-color: var(--accent) !important;
    color: var(--accent) !important;
    background: rgba(46,168,126,0.06) !important;
}

/* ── Sidebar section headers ── */
.sidebar-section {
    font-family: 'IBM Plex Mono', monospace;
    font-size: 0.7rem;
    text-transform: uppercase;
    letter-spacing: 0.1em;
    color: var(--accent) !important;
    margin: 16px 0 6px 0;
}

/* ── Welcome card ── */
.welcome-card {
    background: linear-gradient(135deg, rgba(46,168,126,0.08) 0%, rgba(13,17,23,0) 60%);
    border: 1px solid rgba(46,168,126,0.2);
    border-radius: 14px;
    padding: 20px 24px;
    margin-bottom: 20px;
}
.welcome-card h3 {
    font-family: 'Playfair Display', serif !important;
    color: var(--text) !important;
    margin-bottom: 8px !important;
}
.welcome-card p {
    color: var(--muted) !important;
    font-size: 0.88rem !important;
    line-height: 1.6 !important;
}
.welcome-chips {
    display: flex; flex-wrap: wrap; gap: 8px; margin-top: 14px;
}
.chip {
    background: var(--surface);
    border: 1px solid var(--border);
    border-radius: 20px;
    padding: 4px 12px;
    font-size: 0.78rem;
    color: var(--muted);
    cursor: default;
}
</style>
""", unsafe_allow_html=True)

# ── Session state ─────────────────────────────────────────────────────────────
if "chat_history" not in st.session_state:
    st.session_state.chat_history = []
if "msg_count" not in st.session_state:
    st.session_state.msg_count = 0

# ── Sidebar ───────────────────────────────────────────────────────────────────
with st.sidebar:
    st.markdown('<div class="sidebar-section">System</div>', unsafe_allow_html=True)
    st.markdown(f"""
<div style="font-size:0.82rem; color:#7d8590; line-height:1.6;">
    <b style="color:#e6edf3;">Model</b> {GEMINI_MODEL}<br>
    <b style="color:#e6edf3;">Knowledge base</b> Medical textbook<br>
    <b style="color:#e6edf3;">Vector DB</b> Pinecone<br>
    <b style="color:#e6edf3;">Embeddings</b> MiniLM-L6-v2
</div>
""", unsafe_allow_html=True)

    st.markdown('<div class="sidebar-section">How to use</div>', unsafe_allow_html=True)
    st.markdown("""
<div style="font-size:0.82rem; color:#7d8590; line-height:1.7;">
    Describe symptoms, ask about conditions, medications, or treatments. 
    The bot retrieves answers from a curated medical knowledge base — not the open internet.
</div>
""", unsafe_allow_html=True)

    st.markdown('<div class="sidebar-section">Disclaimer</div>', unsafe_allow_html=True)
    st.markdown("""
<div style="font-size:0.78rem; color:#7d8590; line-height:1.6; font-family:'IBM Plex Mono',monospace;">
    General information only. Not a substitute for professional medical advice. 
    Always consult a qualified healthcare provider.
</div>
""", unsafe_allow_html=True)

    st.markdown("---")
    if st.button("🗑️ Clear chat"):
        st.session_state.chat_history = []
        st.session_state.msg_count = 0
        st.rerun()

    st.markdown('<div class="sidebar-section">Developer</div>', unsafe_allow_html=True)
    st.markdown("""
<div style="font-size:0.8rem; color:#7d8590; line-height:1.8;">
    <b style="color:#e6edf3;">Ishan Sahani</b><br>
    <a href="https://github.com/codeBreaker26" style="color:#2ea87e;">GitHub</a> · 
    <a href="https://www.linkedin.com/in/ishan-sahani/" style="color:#2ea87e;">LinkedIn</a>
</div>
""", unsafe_allow_html=True)

# ── Main ──────────────────────────────────────────────────────────────────────
# Header
st.markdown("""
<div class="medibot-header">
    <div class="medibot-cross">🩺</div>
    <div>
        <div class="medibot-title">MediBotIQ</div>
        <div class="medibot-subtitle">Medical Information Assistant</div>
    </div>
</div>
""", unsafe_allow_html=True)

# Env check
missing = validate_env()
if missing:
    st.markdown(f"""
<div class="env-error">
    <strong>⚠️ Missing configuration:</strong> 
    The following secrets are not set: <code>{"</code>, <code>".join(missing)}</code><br><br>
    <b>On Hugging Face Spaces:</b> Go to Settings → Variables and Secrets → add them there.<br>
    <b>Locally:</b> Create a <code>.env</code> file using <code>.env.example</code> as a template.
</div>
""", unsafe_allow_html=True)
    st.stop()

# Status badge
st.markdown(f"""
<div class="status-badge">
    <div class="status-dot"></div>
    {GEMINI_MODEL} · Pinecone · Online
</div>
""", unsafe_allow_html=True)

# Welcome card (shown only at start)
if not st.session_state.chat_history:
    st.markdown("""
<div class="welcome-card">
    <h3>Hello, how can I help you today?</h3>
    <p>Ask me about symptoms, medical conditions, medications, or general health questions. 
    I'll search my medical knowledge base and give you a grounded, accurate answer.</p>
    <div class="welcome-chips">
        <span class="chip">💊 Medications</span>
        <span class="chip">🤒 Symptoms</span>
        <span class="chip">🏥 Conditions</span>
        <span class="chip">🔬 Diagnostics</span>
        <span class="chip">🧬 Treatments</span>
    </div>
</div>
""", unsafe_allow_html=True)

# ── Chat history ──────────────────────────────────────────────────────────────
def render_bot_message(msg: dict):
    with st.chat_message("assistant"):
        st.markdown(msg["bot"])
        if msg.get("show_disclaimer"):
            st.markdown(
                '<div class="disclaimer">⚕ General info only — consult a healthcare professional before acting on this.</div>',
                unsafe_allow_html=True,
            )
        if msg.get("sources"):
            with st.expander(f"📄 {len(msg['sources'])} source(s) retrieved"):
                for i, doc in enumerate(msg["sources"], 1):
                    page = doc.metadata.get("page", "?")
                    st.markdown(
                        f'<div class="source-card"><strong>Source {i}</strong> · Page {page}<br>'
                        f'<span style="color:#7d8590">{doc.page_content[:280]}…</span></div>',
                        unsafe_allow_html=True,
                    )


for message in st.session_state.chat_history:
    if "user" in message:
        with st.chat_message("user"):
            st.markdown(message["user"])
    elif "bot" in message:
        render_bot_message(message)

# ── Input ─────────────────────────────────────────────────────────────────────
user_query = st.chat_input("Describe your symptoms or ask a health question…")

if user_query:
    clean = sanitize(user_query)

    with st.chat_message("user"):
        st.markdown(clean)
    st.session_state.chat_history.append({"user": clean})

    with st.chat_message("assistant"):
        with st.spinner("Searching knowledge base…"):
            answer, sources = get_answer(clean, st.session_state.chat_history)

        st.markdown(answer)
        show_disclaimer = needs_disclaimer(answer)

        if show_disclaimer:
            st.markdown(
                '<div class="disclaimer">⚕ General info only — consult a healthcare professional before acting on this.</div>',
                unsafe_allow_html=True,
            )

        if sources:
            with st.expander(f"📄 {len(sources)} source(s) retrieved"):
                for i, doc in enumerate(sources, 1):
                    page = doc.metadata.get("page", "?")
                    st.markdown(
                        f'<div class="source-card"><strong>Source {i}</strong> · Page {page}<br>'
                        f'<span style="color:#7d8590">{doc.page_content[:280]}…</span></div>',
                        unsafe_allow_html=True,
                    )

    st.session_state.chat_history.append({
        "bot": answer,
        "show_disclaimer": show_disclaimer,
        "sources": sources,
    })
    st.session_state.msg_count += 1
