"""Google Gemini embedding utilities."""

from langchain_google_genai import GoogleGenerativeAIEmbeddings

from src.config import get_settings


def get_embedding_model() -> GoogleGenerativeAIEmbeddings:
    """
    Create and return Gemini embedding model.
    """

    settings = get_settings()

    return GoogleGenerativeAIEmbeddings(
        model=settings.embedding_model,
        google_api_key=settings.google_api_key,
    )


def embed_documents(texts: list[str]) -> list[list[float]]:
    if not texts:
        raise ValueError("texts cannot be empty")

    embeddings = get_embedding_model()
    return embeddings.embed_documents(texts)


def embed_query(query: str) -> list[float]:
    if not query:
        raise ValueError("query cannot be empty")

    """
    Convert user query into embedding vector.
    """

    embeddings = get_embedding_model()

    return embeddings.embed_query(query)