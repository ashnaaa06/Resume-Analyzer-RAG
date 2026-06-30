"""Tests for resume document ingestion."""

from pathlib import Path

import pytest

from src.ingestion.document_loader import (
    UnsupportedFileTypeError,
    load_docx,
    load_pdf,
    load_resume,
)
from tests.conftest import SAMPLE_RESUME_TEXT


def test_load_pdf_extracts_text(sample_pdf: Path):
    text = load_pdf(sample_pdf)

    assert "Jane Doe" in text
    assert "Software Engineer" in text
    assert "Python" in text


def test_load_docx_extracts_text(sample_docx: Path):
    text = load_docx(sample_docx)

    assert "Jane Doe" in text
    assert "Software Engineer" in text
    assert "ChromaDB" in text


def test_load_resume_auto_detects_pdf(sample_pdf: Path):
    text = load_resume(sample_pdf)

    assert "Jane Doe" in text
    assert "LangChain" in text


def test_load_resume_auto_detects_docx(sample_docx: Path):
    text = load_resume(sample_docx)

    assert "Jane Doe" in text
    assert "ChromaDB" in text


def test_load_resume_rejects_unsupported_extension(tmp_path: Path):
    txt_path = tmp_path / "resume.txt"
    txt_path.write_text(SAMPLE_RESUME_TEXT, encoding="utf-8")

    with pytest.raises(UnsupportedFileTypeError, match="Unsupported file type"):
        load_resume(txt_path)


def test_load_pdf_rejects_wrong_extension(sample_docx: Path):
    with pytest.raises(ValueError, match="Expected a PDF file"):
        load_pdf(sample_docx)


def test_load_docx_rejects_wrong_extension(sample_pdf: Path):
    with pytest.raises(ValueError, match="Expected a DOCX file"):
        load_docx(sample_pdf)


def test_load_resume_raises_for_missing_file(tmp_path: Path):
    missing_path = tmp_path / "missing.pdf"

    with pytest.raises(FileNotFoundError, match="Resume file not found"):
        load_resume(missing_path)
