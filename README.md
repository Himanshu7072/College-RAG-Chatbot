# College RAG Chatbot

A Retrieval-Augmented Generation (RAG) chatbot that answers questions about your
college using its own documents (prospectus, syllabus, FAQs, fee structure, etc.).

## Architecture

```
PDFs / TXT  ──►  Chunker  ──►  Embeddings (MiniLM)  ──►  FAISS
                                                              │
User question  ──►  Embed  ──►  Top-K Retrieval  ──►  Gemini LLM  ──►  Answer + Sources
```

## Tech Stack
- **LLM:** Google Gemini 2.0 Flash (free tier)
- **Embeddings:** sentence-transformers/all-MiniLM-L6-v2 (local, free)
- **Vector DB:** FAISS (local, persistent)
- **Framework:** LangChain
- **UI:** Streamlit

## Setup

1. Create & activate a virtual environment:
   ```powershell
   python -m venv .venv
   .\.venv\Scripts\Activate.ps1
   ```

2. Install dependencies:
   ```powershell
   pip install -r requirements.txt
   ```

3. Get a free Gemini API key from https://aistudio.google.com/apikey

4. Copy `.env.example` to `.env` and paste your key:
   ```powershell
   copy .env.example .env
   ```

5. Drop your college PDFs / TXT files inside the `data/` folder.

6. Build the vector store (one-time, re-run when data changes):
   ```powershell
   python src/ingest.py
   ```

7. Run the chatbot:
   ```powershell
   streamlit run app.py
   ```

## Project Structure
```
college-rag-chatbot/
├── data/                # Your college PDFs / text files
├── src/
│   ├── ingest.py        # Loads, chunks, embeds & stores documents
│   └── chatbot.py       # RAG pipeline (retriever + LLM)
├── vectorstore/         # FAISS persistent storage (auto-created)
├── app.py               # Streamlit chat UI
├── requirements.txt
├── .env.example
└── README.md
```

## Week 1 Checklist
- [x] Project skeleton created
- [x] Virtual environment ready
- [x] Dependencies installed
- [ ] Gemini API key added to `.env`
- [ ] College documents added to `data/`
- [ ] First successful ingestion run
