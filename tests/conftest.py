"""Shared pytest fixtures."""

from pathlib import Path

import pytest

SAMPLE_RESUME_TEXT = (
    "Jane Doe\n"
    "Software Engineer\n"
    "Skills: Python, LangChain, ChromaDB"
)


def _build_minimal_pdf(lines: list[str]) -> bytes:
    """Build a minimal valid PDF with Helvetica text lines."""
    y_position = 720
    stream_parts = ["BT", "/F1 12 Tf"]

    for line in lines:
        escaped = line.replace("\\", "\\\\").replace("(", "\\(").replace(")", "\\)")
        stream_parts.append(f"72 {y_position} Td ({escaped}) Tj")
        y_position -= 18

    stream_parts.append("ET")
    stream = "\n".join(stream_parts) + "\n"
    stream_bytes = stream.encode("latin-1")

    objects = [
        b"1 0 obj\n<< /Type /Catalog /Pages 2 0 R >>\nendobj\n",
        b"2 0 obj\n<< /Type /Pages /Kids [3 0 R] /Count 1 >>\nendobj\n",
        (
            b"3 0 obj\n<< /Type /Page /Parent 2 0 R "
            b"/MediaBox [0 0 612 792] /Contents 4 0 R "
            b"/Resources << /Font << /F1 5 0 R >> >> >>\nendobj\n"
        ),
        (
            f"4 0 obj\n<< /Length {len(stream_bytes)} >>\nstream\n".encode("ascii")
            + stream_bytes
            + b"endstream\nendobj\n"
        ),
        b"5 0 obj\n<< /Type /Font /Subtype /Type1 /BaseFont /Helvetica >>\nendobj\n",
    ]

    pdf = bytearray(b"%PDF-1.4\n")
    offsets = [0]
    for obj in objects:
        offsets.append(len(pdf))
        pdf.extend(obj)

    xref_start = len(pdf)
    pdf.extend(f"xref\n0 {len(objects) + 1}\n".encode("ascii"))
    pdf.extend(b"0000000000 65535 f \n")
    for offset in offsets[1:]:
        pdf.extend(f"{offset:010d} 00000 n \n".encode("ascii"))

    pdf.extend(
        (
            f"trailer\n<< /Size {len(objects) + 1} /Root 1 0 R >>\n"
            f"startxref\n{xref_start}\n%%EOF\n"
        ).encode("ascii")
    )
    return bytes(pdf)


@pytest.fixture
def sample_pdf(tmp_path: Path) -> Path:
    """Create a minimal PDF containing resume text."""
    pdf_path = tmp_path / "sample_resume.pdf"
    pdf_path.write_bytes(_build_minimal_pdf(SAMPLE_RESUME_TEXT.splitlines()))
    return pdf_path


@pytest.fixture
def sample_docx(tmp_path: Path) -> Path:
    """Create a DOCX file containing resume text."""
    from docx import Document as DocxDocument

    docx_path = tmp_path / "sample_resume.docx"
    document = DocxDocument()
    for line in SAMPLE_RESUME_TEXT.splitlines():
        document.add_paragraph(line)
    document.save(docx_path)
    return docx_path
