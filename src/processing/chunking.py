"""Split resume text into retrieval-friendly chunks."""

from langchain_core.documents import Document
from langchain_text_splitters import RecursiveCharacterTextSplitter

from src.config.settings import Settings, get_settings


def _get_splitter(settings: Settings | None = None) -> RecursiveCharacterTextSplitter:
    """Build a text splitter using chunk size and overlap from settings."""
    config = settings if settings is not None else get_settings()

    return RecursiveCharacterTextSplitter(
        chunk_size=config.chunk_size,
        chunk_overlap=config.chunk_overlap,
        length_function=len,
    )


def _attach_chunk_index(chunks: list[Document]) -> list[Document]:
    """Add a sequential chunk_index to each document's metadata."""
    return [
        Document(
            page_content=chunk.page_content,
            metadata={**chunk.metadata, "chunk_index": index},
        )
        for index, chunk in enumerate(chunks)
    ]


def chunk_text(
    text: str,
    *,
    metadata: dict | None = None,
    settings: Settings | None = None,
) -> list[Document]:
    """Split plain text into LangChain Document chunks."""
    cleaned = text.strip()
    if not cleaned:
        raise ValueError("Cannot chunk empty text.")

    splitter = _get_splitter(settings)
    texts = splitter.split_text(cleaned)
    base_metadata = metadata or {}

    documents = [
        Document(page_content=chunk, metadata=dict(base_metadata))
        for chunk in texts
    ]
    return _attach_chunk_index(documents)


def chunk_document(
    document: Document,
    *,
    settings: Settings | None = None,
) -> list[Document]:
    """Split a LangChain Document into smaller Document chunks."""
    if not document.page_content or not document.page_content.strip():
        raise ValueError("Cannot chunk empty document.")

    splitter = _get_splitter(settings)
    chunks = splitter.split_documents([document])
    return _attach_chunk_index(chunks)
