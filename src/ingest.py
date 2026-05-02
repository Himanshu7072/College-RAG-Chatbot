"""
Ingestion pipeline: loads documents from ./data, splits them into chunks,
creates embeddings, and persists them in a Chroma vector store.

Run once after adding/updating files in ./data:
    python src/ingest.py
"""
from __future__ import annotations

import os
import shutil
from pathlib import Path

from dotenv import load_dotenv
from langchain_community.document_loaders import (
    DirectoryLoader,
    PyPDFLoader,
    TextLoader,
)
from langchain_text_splitters import RecursiveCharacterTextSplitter
from langchain_huggingface import HuggingFaceEmbeddings
from langchain_community.vectorstores import FAISS

load_dotenv()

DATA_DIR = Path(os.getenv("DATA_DIR", "./data"))
VECTOR_DIR = Path(os.getenv("VECTOR_DIR", "./vectorstore"))
EMBEDDING_MODEL = os.getenv("EMBEDDING_MODEL", "sentence-transformers/all-MiniLM-L6-v2")
CHUNK_SIZE = int(os.getenv("CHUNK_SIZE", "800"))
CHUNK_OVERLAP = int(os.getenv("CHUNK_OVERLAP", "100"))


def load_documents() -> list:
    """Load every PDF and TXT file under DATA_DIR."""
    if not DATA_DIR.exists():
        DATA_DIR.mkdir(parents=True, exist_ok=True)
        print(f"[!] Created empty data folder at {DATA_DIR}. Add files and re-run.")
        return []

    pdf_loader = DirectoryLoader(
        str(DATA_DIR), glob="**/*.pdf", loader_cls=PyPDFLoader, show_progress=True
    )
    txt_loader = DirectoryLoader(
        str(DATA_DIR),
        glob="**/*.txt",
        loader_cls=TextLoader,
        loader_kwargs={"encoding": "utf-8"},
        show_progress=True,
    )

    docs = pdf_loader.load() + txt_loader.load()
    print(f"[+] Loaded {len(docs)} document pages from {DATA_DIR}")
    return docs


def chunk_documents(docs: list) -> list:
    splitter = RecursiveCharacterTextSplitter(
        chunk_size=CHUNK_SIZE,
        chunk_overlap=CHUNK_OVERLAP,
        separators=["\n\n", "\n", ". ", " ", ""],
    )
    chunks = splitter.split_documents(docs)
    print(f"[+] Split into {len(chunks)} chunks "
          f"(size={CHUNK_SIZE}, overlap={CHUNK_OVERLAP})")
    return chunks


def build_vectorstore(chunks: list) -> None:
    if VECTOR_DIR.exists():
        print(f"[i] Removing old vector store at {VECTOR_DIR}")
        shutil.rmtree(VECTOR_DIR)

    embeddings = HuggingFaceEmbeddings(model_name=EMBEDDING_MODEL)
    vectorstore = FAISS.from_documents(documents=chunks, embedding=embeddings)
    VECTOR_DIR.mkdir(parents=True, exist_ok=True)
    vectorstore.save_local(str(VECTOR_DIR))
    print(f"[\u2713] Vector store saved to {VECTOR_DIR}")


def main() -> None:
    docs = load_documents()
    if not docs:
        print("[!] No documents found. Drop PDFs/TXT files into ./data and re-run.")
        return
    chunks = chunk_documents(docs)
    build_vectorstore(chunks)
    print("[\u2713] Ingestion complete. You can now run: streamlit run app.py")


if __name__ == "__main__":
    main()
