from unittest.mock import MagicMock, patch

from src.embeddings import (
    embed_documents,
    embed_query,
    get_embedding_model,
)


@patch("src.embeddings.gemini_embeddings.GoogleGenerativeAIEmbeddings")
def test_get_embedding_model_returns_model(mock_embeddings):
    get_embedding_model()

    mock_embeddings.assert_called_once()


@patch("src.embeddings.gemini_embeddings.get_embedding_model")
def test_embed_documents_returns_vectors(mock_get_model):
    mock_model = MagicMock()
    mock_model.embed_documents.return_value = [[0.1, 0.2], [0.3, 0.4]]

    mock_get_model.return_value = mock_model

    result = embed_documents(["resume one", "resume two"])

    assert len(result) == 2
    assert result[0] == [0.1, 0.2]

    mock_model.embed_documents.assert_called_once()


@patch("src.embeddings.gemini_embeddings.get_embedding_model")
def test_embed_query_returns_vector(mock_get_model):
    mock_model = MagicMock()
    mock_model.embed_query.return_value = [0.5, 0.6, 0.7]

    mock_get_model.return_value = mock_model

    result = embed_query("python developer")

    assert result == [0.5, 0.6, 0.7]

    mock_model.embed_query.assert_called_once_with(
        "python developer"
    )