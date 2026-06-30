"""Tests for resume text chunking."""

import pytest
from langchain_core.documents import Document

from src.config.settings import Settings
from src.processing.chunking import chunk_document, chunk_text


@pytest.fixture
def chunk_settings() -> Settings:
    """Settings tuned for predictable chunking in tests."""
    return Settings(
        google_api_key="test-api-key-12345",
        chunk_size=100,
        chunk_overlap=20,
    )


@pytest.fixture
def long_resume_text() -> str:
    """Generate resume-like text that exceeds the test chunk size."""
    sections = [
        "Jane Doe | Software Engineer | jane@example.com",
        "Summary: Backend engineer with 5 years of experience in Python and cloud systems.",
        "Experience: Built RAG pipelines using LangChain, ChromaDB, and Gemini APIs.",
        "Skills: Python, FastAPI, Docker, Kubernetes, PostgreSQL, Redis, and CI/CD.",
        "Education: B.S. Computer Science, State University, 2018.",
    ]
    return "\n\n".join(sections * 4)


def test_chunk_text_returns_langchain_documents(chunk_settings: Settings, long_resume_text: str):
    chunks = chunk_text(long_resume_text, settings=chunk_settings)

    assert len(chunks) > 1
    assert all(isinstance(chunk, Document) for chunk in chunks)
    assert all(chunk.page_content.strip() for chunk in chunks)


def test_chunk_text_respects_chunk_size(chunk_settings: Settings):
    text = "word " * 200  # 1000 characters with trailing space pattern

    chunks = chunk_text(text, settings=chunk_settings)

    assert len(chunks) > 1
    assert all(len(chunk.page_content) <= chunk_settings.chunk_size for chunk in chunks)


def test_chunk_text_applies_overlap(chunk_settings: Settings):
    text = "abcdefghijklmnopqrstuvwxyz " * 20

    chunks = chunk_text(text, settings=chunk_settings)

    assert len(chunks) >= 2
    assert chunks[0].page_content[-chunk_settings.chunk_overlap :] in chunks[1].page_content


def test_chunk_text_adds_chunk_index_metadata(chunk_settings: Settings, long_resume_text: str):
    chunks = chunk_text(long_resume_text, settings=chunk_settings)

    assert [chunk.metadata["chunk_index"] for chunk in chunks] == list(range(len(chunks)))


def test_chunk_text_preserves_custom_metadata(chunk_settings: Settings, long_resume_text: str):
    metadata = {"source": "resume.pdf", "resume_id": "resume-123"}

    chunks = chunk_text(long_resume_text, metadata=metadata, settings=chunk_settings)

    assert all(chunk.metadata["source"] == "resume.pdf" for chunk in chunks)
    assert all(chunk.metadata["resume_id"] == "resume-123" for chunk in chunks)
    assert chunks[0].metadata["chunk_index"] == 0


def test_chunk_text_returns_single_chunk_for_short_text(chunk_settings: Settings):
    text = "Short resume summary with only a few words."

    chunks = chunk_text(text, settings=chunk_settings)

    assert len(chunks) == 1
    assert chunks[0].page_content == text


def test_chunk_text_rejects_empty_text(chunk_settings: Settings):
    with pytest.raises(ValueError, match="Cannot chunk empty text"):
        chunk_text("   ", settings=chunk_settings)


def test_chunk_document_splits_langchain_document(chunk_settings: Settings, long_resume_text: str):
    document = Document(
        page_content=long_resume_text,
        metadata={"source": "resume.docx", "resume_id": "resume-456"},
    )

    chunks = chunk_document(document, settings=chunk_settings)

    assert len(chunks) > 1
    assert all(isinstance(chunk, Document) for chunk in chunks)


def test_chunk_document_preserves_metadata(chunk_settings: Settings, long_resume_text: str):
    document = Document(
        page_content=long_resume_text,
        metadata={"source": "resume.docx", "resume_id": "resume-456"},
    )

    chunks = chunk_document(document, settings=chunk_settings)

    assert all(chunk.metadata["source"] == "resume.docx" for chunk in chunks)
    assert all(chunk.metadata["resume_id"] == "resume-456" for chunk in chunks)


def test_chunk_document_adds_chunk_index(chunk_settings: Settings, long_resume_text: str):
    document = Document(page_content=long_resume_text, metadata={"source": "resume.pdf"})

    chunks = chunk_document(document, settings=chunk_settings)

    assert [chunk.metadata["chunk_index"] for chunk in chunks] == list(range(len(chunks)))


def test_chunk_document_rejects_empty_document(chunk_settings: Settings):
    document = Document(page_content="  ", metadata={"source": "empty.pdf"})

    with pytest.raises(ValueError, match="Cannot chunk empty document"):
        chunk_document(document, settings=chunk_settings)


def test_smaller_chunk_size_produces_more_chunks(monkeypatch, long_resume_text: str):
    monkeypatch.setenv("GOOGLE_API_KEY", "test-api-key-12345")

    large_chunks = chunk_text(
        long_resume_text,
        settings=Settings(
            google_api_key="test-api-key-12345",
            chunk_size=300,
            chunk_overlap=30,
        ),
    )
    small_chunks = chunk_text(
        long_resume_text,
        settings=Settings(
            google_api_key="test-api-key-12345",
            chunk_size=100,
            chunk_overlap=20,
        ),
    )

    assert len(small_chunks) > len(large_chunks)


def test_chunk_text_uses_settings_object_for_splitter():
    settings = Settings(
        google_api_key="test-api-key-12345",
        chunk_size=120,
        chunk_overlap=15,
    )
    text = "section " * 80

    chunks = chunk_text(text, settings=settings)

    assert len(chunks) > 1
    assert all(len(chunk.page_content) <= settings.chunk_size for chunk in chunks)
