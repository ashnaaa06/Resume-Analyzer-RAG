from src.retrieval import retrieve_relevant_chunks


def test_retrieve_relevant_chunks():
    results = retrieve_relevant_chunks(
        "Python Developer"
    )

    assert len(results) > 0

    for doc in results:
        assert doc.page_content