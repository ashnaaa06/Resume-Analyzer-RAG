from unittest.mock import MagicMock, patch

from langchain_core.documents import Document

from src.vectorstore import (
    add_documents,
    create_vectorstore,
    load_vectorstore,
)


@patch("src.vectorstore.chroma_store.Chroma")
@patch("src.vectorstore.chroma_store.get_embedding_model")
def test_load_vectorstore(
    mock_embeddings,
    mock_chroma,
):
    load_vectorstore()

    mock_chroma.assert_called_once()


@patch("src.vectorstore.chroma_store.Chroma")
@patch("src.vectorstore.chroma_store.get_embedding_model")
def test_create_vectorstore(
    mock_embeddings,
    mock_chroma,
):
    docs = [
        Document(page_content="resume text")
    ]

    create_vectorstore(docs)

    mock_chroma.from_documents.assert_called_once()


def test_add_documents():
    mock_store = MagicMock()

    docs = [
        Document(page_content="new resume")
    ]

    add_documents(mock_store, docs)

    mock_store.add_documents.assert_called_once_with(
        docs
    )