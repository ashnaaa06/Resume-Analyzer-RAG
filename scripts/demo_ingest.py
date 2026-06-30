from pathlib import Path

from langchain_core.documents import Document

from src.ingestion.document_loader import load_resume
from src.processing.chunking import chunk_document
from src.vectorstore import create_vectorstore
from src.config import get_settings

print(get_settings().embedding_model)

resume_path = Path("data/resumes/Ashna_Mittal_Resume.pdf")

# Load resume text
text = load_resume(resume_path)

# Convert text -> LangChain Document
document = Document(
    page_content=text,
    metadata={"source": str(resume_path)},
)

# Chunk document
chunks = chunk_document(document)

# Create vector store
vectorstore = create_vectorstore(chunks)

print("Loaded document")
print(f"Created {len(chunks)} chunks")
print("Stored in ChromaDB")