"""Load resume files (PDF, DOCX) and extract plain text."""

from pathlib import Path

from docx import Document as DocxDocument
from langchain_community.document_loaders import PyPDFLoader
from langchain_core.documents import Document


SUPPORTED_EXTENSIONS = {".pdf", ".docx"}


class UnsupportedFileTypeError(ValueError):
    """Raised when a resume file has an unsupported extension."""


def _validate_path(path: str | Path) -> Path:
    """Ensure the path exists and points to a regular file."""
    file_path = Path(path).resolve()

    if not file_path.exists():
        raise FileNotFoundError(f"Resume file not found: {file_path}")
    if not file_path.is_file():
        raise ValueError(f"Path is not a file: {file_path}")

    return file_path


def _documents_to_text(documents: list) -> str:
    """Join LangChain Document pages into a single cleaned text string."""
    pages = [
        doc.page_content.strip()
        for doc in documents
        if doc.page_content and doc.page_content.strip()
    ]

    if not pages:
        raise ValueError("No text could be extracted from the file.")

    return "\n\n".join(pages)


def load_pdf(path: str | Path) -> str:
    """Extract text from a PDF resume file."""
    file_path = _validate_path(path)

    if file_path.suffix.lower() != ".pdf":
        raise ValueError(f"Expected a PDF file, got: {file_path.suffix}")

    documents = PyPDFLoader(str(file_path)).load()
    return _documents_to_text(documents)


def _extract_docx_text(file_path: Path) -> str:
    """Read paragraph text from a DOCX file using python-docx."""
    document = DocxDocument(file_path)
    paragraphs = [
        paragraph.text.strip()
        for paragraph in document.paragraphs
        if paragraph.text.strip()
    ]

    if not paragraphs:
        raise ValueError("No text could be extracted from the file.")

    return "\n\n".join(paragraphs)


def load_docx(path: str | Path) -> str:
    """Extract text from a DOCX resume file."""
    file_path = _validate_path(path)

    if file_path.suffix.lower() != ".docx":
        raise ValueError(f"Expected a DOCX file, got: {file_path.suffix}")

    return _extract_docx_text(file_path)

def load_resume(path: str | Path) -> str:
    """Extract text from a resume file, auto-detecting PDF or DOCX by extension."""
    file_path = _validate_path(path)
    extension = file_path.suffix.lower()

    if extension == ".pdf":
        return load_pdf(file_path)

    if extension == ".docx":
        return load_docx(file_path)

    supported = ", ".join(sorted(SUPPORTED_EXTENSIONS))
    raise UnsupportedFileTypeError(
        f"Unsupported file type '{extension}'. Supported types: {supported}"
    )