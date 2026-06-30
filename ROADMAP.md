# Resume Analyzer RAG Chatbot — Development Roadmap

Build this project **module by module**. Each phase produces a testable unit before moving on.

---

## Project Structure

```
Resume-Analyzer-RAG/
├── app/
│   ├── __init__.py
│   ├── main.py                 # Streamlit entry point (Phase 7)
│   └── ui/
│       ├── __init__.py
│       ├── sidebar.py          # Upload & settings UI (Phase 7)
│       └── chat.py             # Chat interface (Phase 7)
│
├── src/
│   ├── __init__.py
│   ├── config/
│   │   ├── __init__.py
│   │   └── settings.py         # Env vars, paths, model config (Phase 1)
│   │
│   ├── ingestion/
│   │   ├── __init__.py
│   │   └── document_loader.py  # PDF/DOCX loading (Phase 2)
│   │
│   ├── processing/
│   │   ├── __init__.py
│   │   └── chunking.py         # Text splitting & cleaning (Phase 3)
│   │
│   ├── embeddings/
│   │   ├── __init__.py
│   │   └── embedder.py         # Gemini embeddings (Phase 4)
│   │
│   ├── vectorstore/
│   │   ├── __init__.py
│   │   └── chroma_store.py     # ChromaDB CRUD (Phase 4)
│   │
│   ├── retrieval/
│   │   ├── __init__.py
│   │   └── retriever.py        # Similarity search (Phase 5)
│   │
│   ├── llm/
│   │   ├── __init__.py
│   │   └── chain.py            # RAG chain with Gemini (Phase 6)
│   │
│   └── utils/
│       ├── __init__.py
│       └── helpers.py          # Shared utilities (as needed)
│
├── data/
│   ├── resumes/                # Uploaded resume files
│   └── chroma_db/              # Persisted vector store
│
├── tests/
│   ├── __init__.py
│   ├── test_document_loader.py
│   ├── test_chunking.py
│   ├── test_chroma_store.py
│   └── test_chain.py
│
├── .env.example
├── requirements.txt
└── ROADMAP.md
```

---

## Phase 1 — Configuration (`src/config/`)

**Goal:** Centralize all settings so every module reads from one place.

| Task | File | Details |
|------|------|---------|
| 1.1 | `settings.py` | Load `GOOGLE_API_KEY` from `.env` via `pydantic-settings` |
| 1.2 | `settings.py` | Define paths: `DATA_DIR`, `RESUMES_DIR`, `CHROMA_DIR` |
| 1.3 | `settings.py` | Model config: `GEMINI_MODEL`, `EMBEDDING_MODEL`, chunk size/overlap |
| 1.4 | `.env.example` | Template with required environment variables |

**Done when:** `from src.config.settings import settings` works and prints config without errors.

---

## Phase 2 — Document Ingestion (`src/ingestion/`)

**Goal:** Load resume files (PDF, DOCX) into LangChain `Document` objects.

| Task | File | Details |
|------|------|---------|
| 2.1 | `document_loader.py` | `load_pdf(path)` using `PyPDFLoader` |
| 2.2 | `document_loader.py` | `load_docx(path)` using `Docx2txtLoader` |
| 2.3 | `document_loader.py` | `load_resume(path)` — auto-detect format by extension |
| 2.4 | `tests/test_document_loader.py` | Unit test with a sample resume file |

**Done when:** A resume file returns a list of `Document` objects with non-empty `page_content`.

---

## Phase 3 — Text Processing (`src/processing/`)

**Goal:** Split documents into retrieval-friendly chunks.

| Task | File | Details |
|------|------|---------|
| 3.1 | `chunking.py` | `RecursiveCharacterTextSplitter` with configurable size/overlap |
| 3.2 | `chunking.py` | Attach metadata: `source`, `chunk_index`, `resume_id` |
| 3.3 | `chunking.py` | `chunk_documents(docs, resume_id)` wrapper function |
| 3.4 | `tests/test_chunking.py` | Verify chunk count and metadata |

**Done when:** 5-page resume produces ~15–30 chunks with correct metadata.

---

## Phase 4 — Embeddings & Vector Store (`src/embeddings/` + `src/vectorstore/`)

**Goal:** Embed chunks and persist them in ChromaDB.

| Task | File | Details |
|------|------|---------|
| 4.1 | `embedder.py` | `GoogleGenerativeAIEmbeddings` wrapper |
| 4.2 | `chroma_store.py` | `create_collection(resume_id)` |
| 4.3 | `chroma_store.py` | `add_documents(resume_id, chunks)` |
| 4.4 | `chroma_store.py` | `delete_collection(resume_id)` |
| 4.5 | `chroma_store.py` | `list_collections()` |
| 4.6 | `tests/test_chroma_store.py` | Add, query, delete round-trip test |

**Done when:** Chunks are stored in `data/chroma_db/` and survive app restart.

---

## Phase 5 — Retrieval (`src/retrieval/`)

**Goal:** Fetch the most relevant resume chunks for a user question.

| Task | File | Details |
|------|------|---------|
| 5.1 | `retriever.py` | `get_retriever(resume_id, k=4)` — similarity search |
| 5.2 | `retriever.py` | `retrieve_context(resume_id, query)` — returns formatted context string |
| 5.3 | — | Tune `k` and optionally add MMR for diversity |

**Done when:** Query *"What are this candidate's Python skills?"* returns relevant chunks.

---

## Phase 6 — LLM Chain (`src/llm/`)

**Goal:** Wire retrieval + Gemini into a conversational RAG chain.

| Task | File | Details |
|------|------|---------|
| 6.1 | `chain.py` | System prompt: resume analyst persona, cite sources |
| 6.2 | `chain.py` | `create_rag_chain(resume_id)` using LCEL or `RetrievalQA` |
| 6.3 | `chain.py` | `ask(resume_id, question, chat_history)` with memory |
| 6.4 | `tests/test_chain.py` | End-to-end question → answer test |

**Done when:** A question about an indexed resume returns a grounded, coherent answer.

---

## Phase 7 — Streamlit UI (`app/`)

**Goal:** User-facing chatbot interface.

| Task | File | Details |
|------|------|---------|
| 7.1 | `main.py` | App layout, session state init |
| 7.2 | `ui/sidebar.py` | Resume upload, processing status, clear/re-index |
| 7.3 | `ui/chat.py` | Chat history display, input box, streaming response |
| 7.4 | `main.py` | Wire upload → ingest → index → chat pipeline |

**Done when:** User can upload a resume, ask questions, and get answers in the browser.

---

## Phase 8 — Polish & Hardening

| Task | Details |
|------|---------|
| 8.1 | Error handling: invalid files, missing API key, empty resume |
| 8.2 | Loading spinners and user feedback in Streamlit |
| 8.3 | `.gitignore` for `data/`, `.env`, `__pycache__` |
| 8.4 | README with setup and run instructions |
| 8.5 | Optional: multi-resume support, export chat history |

---

## Build Order Summary

```
Phase 1  Config          →  settings, .env
Phase 2  Ingestion       →  load PDF/DOCX
Phase 3  Processing      →  chunk text
Phase 4  Vector Store    →  embed + ChromaDB
Phase 5  Retrieval       →  similarity search
Phase 6  LLM Chain       →  RAG with Gemini
Phase 7  Streamlit UI    →  chat interface
Phase 8  Polish          →  errors, docs, gitignore
```

---

## How to Run (after Phase 7)

```bash
# 1. Create virtual environment
python -m venv venv
venv\Scripts\activate        # Windows
# source venv/bin/activate   # macOS/Linux

# 2. Install dependencies
pip install -r requirements.txt

# 3. Configure API key
copy .env.example .env
# Edit .env and set GOOGLE_API_KEY=your_key_here

# 4. Launch app
streamlit run app/main.py
```

---

## Next Step

**Start with Phase 1 — Configuration.**  
Say *"Build Phase 1"* when you're ready and we'll implement `src/config/settings.py` and `.env.example`.
