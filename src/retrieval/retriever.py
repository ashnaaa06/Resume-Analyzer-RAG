from langchain_core.documents import Document
from langchain_chroma import Chroma

from src.config import get_settings


def retrieve_relevant_chunks(
    vectorstore: Chroma,
    query: str,
) -> list[Document]:
    """
    Retrieve the most relevant resume chunks
    from the uploaded resume.
    """

    settings = get_settings()

    results = vectorstore.similarity_search(
        query=query,
        k=settings.retrieval_k,
    )

    return results