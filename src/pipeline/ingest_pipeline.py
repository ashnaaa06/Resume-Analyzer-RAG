from pathlib import Path

from src.ingestion.document_loader import load_resume
from src.processing.chunking import chunk_text
from src.vectorstore.chroma_store import create_vectorstore


def ingest_resume(resume_path: str):
    """
    Load a resume, split it into chunks,
    and create a fresh Chroma vector store.
    """

    text = load_resume(Path(resume_path))

    chunks = chunk_text(
        text,
        metadata={"source": resume_path}
    )

    vectorstore = create_vectorstore(chunks)

    return vectorstore