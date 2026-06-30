# scripts/check_embedding.py

from src.embeddings import embed_query

print("Testing embedding...")

vector = embed_query("Python Developer")

print("Embedding generated successfully!")
print("Vector length:", len(vector))