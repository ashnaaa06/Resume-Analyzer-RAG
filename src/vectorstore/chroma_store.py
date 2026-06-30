"""ChromaDB vector store utilities."""

from langchain_chroma import Chroma
from langchain_core.documents import Document

from src.config import get_settings
from src.embeddings import get_embedding_model


COLLECTION_NAME = "resume_chunks"


def create_vectorstore(documents: list[Document]) -> Chroma:
    settings = get_settings()

    settings.ensure_directories()   # ADD THIS

    vectorstore = Chroma.from_documents(
        documents=documents,
        embedding=get_embedding_model(),
        persist_directory=str(settings.chroma_dir),
        collection_name=COLLECTION_NAME,
    )

    return vectorstore


def load_vectorstore() -> Chroma:
    settings = get_settings()

    settings.ensure_directories()   # ADD THIS

    return Chroma(
        persist_directory=str(settings.chroma_dir),
        embedding_function=get_embedding_model(),
        collection_name=COLLECTION_NAME,
    )


def add_documents(
    vectorstore: Chroma,
    documents: list[Document],
) -> None:
    """
    Add additional documents to existing vector store.
    """

    vectorstore.add_documents(documents)