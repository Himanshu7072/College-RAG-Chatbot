"""
Streamlit chat UI for the Hybrid College RAG Chatbot.
Run with:  streamlit run app.py
"""
from __future__ import annotations

import sys
from pathlib import Path

import streamlit as st

# Make src/ importable
sys.path.insert(0, str(Path(__file__).parent / "src"))
from chatbot import hybrid_answer, get_retriever  # noqa: E402

st.set_page_config(page_title="College RAG Chatbot", page_icon="🎓", layout="wide")
st.title("🎓 College RAG Chatbot — Hybrid Mode")
st.caption("Local docs first, live fetch from rsmt.ac.in when needed.")


@st.cache_resource(show_spinner="Loading model & vector store...")
def warmup():
    # Warm up retriever / embeddings.
    return get_retriever()


try:
    warmup()
except Exception as e:
    st.error(str(e))
    st.stop()

if "messages" not in st.session_state:
    st.session_state.messages = []

for msg in st.session_state.messages:
    with st.chat_message(msg["role"]):
        st.markdown(msg["content"])
        if msg.get("badge"):
            st.caption(msg["badge"])
        if msg.get("sources"):
            with st.expander("Sources"):
                for s in msg["sources"]:
                    st.markdown(f"- `{s}`")
        if msg.get("live_url"):
            st.markdown(f"🌐 Live source: [{msg['live_url']}]({msg['live_url']})")


def _badge(mode: str) -> str:
    return {
        "local": "📚 Answered from local knowledge base",
        "live": "🌐 Answered from live rsmt.ac.in fetch",
        "live-failed": "⚠️ Live fetch failed",
    }.get(mode, mode)


if prompt := st.chat_input("Ask anything about RSMT..."):
    st.session_state.messages.append({"role": "user", "content": prompt})
    with st.chat_message("user"):
        st.markdown(prompt)

    with st.chat_message("assistant"):
        with st.spinner("Thinking..."):
            res = hybrid_answer(prompt)
        st.markdown(res["answer"])
        st.caption(_badge(res["mode"]))
        if res["sources"]:
            with st.expander("Sources"):
                for s in res["sources"]:
                    st.markdown(f"- `{s}`")
        if res["live_url"]:
            st.markdown(f"🌐 Live source: [{res['live_url']}]({res['live_url']})")

    st.session_state.messages.append(
        {
            "role": "assistant",
            "content": res["answer"],
            "badge": _badge(res["mode"]),
            "sources": res["sources"],
            "live_url": res["live_url"],
        }
    )

with st.sidebar:
    st.header("How it works")
    st.markdown(
        "**Hybrid retrieval:**\n\n"
        "1. Search local FAISS index (PDFs in `data/`)\n"
        "2. If Gemini cannot answer from local context, fall back to a "
        "live fetch from rsmt.ac.in\n"
        "3. Answer is generated from whichever source has the info\n"
    )
    st.divider()
    if st.button("Clear chat"):
        st.session_state.messages = []
        st.rerun()
