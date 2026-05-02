"""
Hybrid RAG chatbot:
  1. Retrieves top-K chunks from local FAISS index (fast, grounded).
  2. If the LLM cannot answer from local context, falls back to live-fetching
     the most relevant page from rsmt.ac.in and answering from that.
"""
from __future__ import annotations

import os
from pathlib import Path

from dotenv import load_dotenv
from langchain_community.vectorstores import FAISS
from langchain_huggingface import HuggingFaceEmbeddings
from langchain_google_genai import ChatGoogleGenerativeAI
from langchain_core.prompts import ChatPromptTemplate
from langchain_core.output_parsers import StrOutputParser
from langchain_core.runnables import RunnablePassthrough

from live_fetch import fetch_live

load_dotenv()

VECTOR_DIR = Path(os.getenv("VECTOR_DIR", "./vectorstore"))
EMBEDDING_MODEL = os.getenv("EMBEDDING_MODEL", "sentence-transformers/all-MiniLM-L6-v2")
GEMINI_MODEL = os.getenv("GEMINI_MODEL", "gemini-2.5-flash")
TOP_K = int(os.getenv("TOP_K", "4"))

# Sentinel the local-only model returns when it cannot answer from context.
NO_ANSWER_TOKEN = "NO_LOCAL_ANSWER"

LOCAL_SYSTEM = f"""You are a helpful assistant for college students at RSMT, Varanasi.
Answer the question using ONLY the context below.
If the answer is NOT clearly present in the context, reply with EXACTLY this token and nothing else: {NO_ANSWER_TOKEN}

Context:
{{context}}
"""

LIVE_SYSTEM = """You are a helpful assistant for college students at RSMT, Varanasi.
The user's question could not be answered from local documents, so the following
content was just fetched live from the official RSMT website. Answer using ONLY
this content. Be concise and friendly. If the content does not contain the
answer, say so honestly.

Live page: {url}

Content:
{content}
"""

LOCAL_PROMPT = ChatPromptTemplate.from_messages(
    [("system", LOCAL_SYSTEM), ("human", "{question}")]
)
LIVE_PROMPT = ChatPromptTemplate.from_messages(
    [("system", LIVE_SYSTEM), ("human", "{question}")]
)


def _format_docs(docs) -> str:
    return "\n\n---\n\n".join(
        f"[Source: {Path(d.metadata.get('source', 'unknown')).name}]\n{d.page_content}"
        for d in docs
    )


def get_retriever():
    if not VECTOR_DIR.exists():
        raise RuntimeError(
            f"Vector store not found at {VECTOR_DIR}. "
            "Run `python src/ingest.py` first."
        )
    embeddings = HuggingFaceEmbeddings(model_name=EMBEDDING_MODEL)
    vectorstore = FAISS.load_local(
        str(VECTOR_DIR),
        embeddings,
        allow_dangerous_deserialization=True,
    )
    return vectorstore.as_retriever(search_kwargs={"k": TOP_K})


def _llm():
    if not os.getenv("GOOGLE_API_KEY"):
        raise RuntimeError("GOOGLE_API_KEY missing. Add it to your .env file.")
    return ChatGoogleGenerativeAI(model=GEMINI_MODEL, temperature=0.2)


def get_chain():
    """Returns (chain, retriever) for backwards compatibility (local-only RAG)."""
    retriever = get_retriever()
    chain = (
        {"context": retriever | _format_docs, "question": RunnablePassthrough()}
        | LOCAL_PROMPT
        | _llm()
        | StrOutputParser()
    )
    return chain, retriever


def hybrid_answer(question: str) -> dict:
    """Answer using local RAG; fall back to live rsmt.ac.in fetch if needed.

    Returns dict with: answer, mode ('local'|'live'|'live-failed'), sources (list),
    live_url (str|None).
    """
    retriever = get_retriever()
    docs = retriever.invoke(question)
    local_chain = LOCAL_PROMPT | _llm() | StrOutputParser()
    local_answer = local_chain.invoke(
        {"context": _format_docs(docs), "question": question}
    ).strip()

    if NO_ANSWER_TOKEN not in local_answer:
        return {
            "answer": local_answer,
            "mode": "local",
            "sources": sorted({Path(d.metadata.get("source", "unknown")).name for d in docs}),
            "live_url": None,
        }

    # Fallback: live fetch
    live = fetch_live(question)
    if not live or not live.get("text"):
        return {
            "answer": (
                "I couldn't find this in my local knowledge base, and live fetching "
                f"from the website failed ({live.get('error') if live else 'no response'}). "
                f"Please check {live['url'] if live else 'https://www.rsmt.ac.in/'} directly."
            ),
            "mode": "live-failed",
            "sources": [],
            "live_url": live["url"] if live else None,
        }

    live_chain = LIVE_PROMPT | _llm() | StrOutputParser()
    live_answer = live_chain.invoke(
        {"url": live["url"], "content": live["text"], "question": question}
    ).strip()
    return {
        "answer": live_answer,
        "mode": "live",
        "sources": [],
        "live_url": live["url"],
    }


def ask(question: str) -> dict:
    return hybrid_answer(question)


if __name__ == "__main__":
    q = input("Ask: ").strip()
    res = ask(q)
    print(f"\n[mode: {res['mode']}]")
    print("\nAnswer:\n", res["answer"])
    if res["sources"]:
        print("\nLocal sources:", ", ".join(res["sources"]))
    if res["live_url"]:
        print("Live source:", res["live_url"])
