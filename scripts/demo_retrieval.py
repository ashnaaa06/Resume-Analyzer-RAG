from src.retrieval import retrieve_relevant_chunks


job_description = """
Looking for a Python Developer with
experience in Machine Learning,
SQL and Flask.
"""

results = retrieve_relevant_chunks(job_description)

print("\nRetrieved Chunks\n")

for idx, doc in enumerate(results, start=1):
    print("=" * 50)
    print(f"Chunk {idx}")
    print("=" * 50)
    print(doc.page_content[:500])
    print()