from pathlib import Path
import io

from reportlab.lib.styles import getSampleStyleSheet
from reportlab.platypus import (
    SimpleDocTemplate,
    Paragraph,
)

def save_uploaded_file(uploaded_file):
    upload_dir = Path("data/resumes")
    upload_dir.mkdir(parents=True, exist_ok=True)

    file_path = upload_dir / uploaded_file.name

    with open(file_path, "wb") as f:
        f.write(uploaded_file.getbuffer())

    return str(file_path)

def create_pdf_report(result):
    """
    Generate a PDF report of the resume analysis.
    """

    buffer = io.BytesIO()

    doc = SimpleDocTemplate(buffer)

    styles = getSampleStyleSheet()

    story = []

    story.append(
        Paragraph(
            "<b>AI Resume Analysis Report</b>",
            styles["Heading1"],
        )
    )

    story.append(
        Paragraph(
            f"<b>ATS Score:</b> {result.match_score:.1f}%",
            styles["BodyText"],
        )
    )

    story.append(
        Paragraph(
            "<br/><b>Executive Summary</b>",
            styles["Heading2"],
        )
    )

    summary = (
        f"<b>Strengths:</b> {', '.join(result.strengths[:3])}<br/><br/>"
        f"<b>Missing Skills:</b> {', '.join(result.missing_skills[:5])}"
    )

    story.append(
        Paragraph(summary, styles["BodyText"])
    )

    story.append(
        Paragraph(
            "<br/><b>Matching Skills</b>",
            styles["Heading2"],
        )
    )

    for skill in result.matching_skills:
        story.append(
            Paragraph(f"• {skill}", styles["BodyText"])
        )

    story.append(
        Paragraph(
            "<br/><b>Missing Skills</b>",
            styles["Heading2"],
        )
    )

    for skill in result.missing_skills:
        story.append(
            Paragraph(f"• {skill}", styles["BodyText"])
        )

    story.append(
        Paragraph(
            "<br/><b>Strengths</b>",
            styles["Heading2"],
        )
    )

    for item in result.strengths:
        story.append(
            Paragraph(f"• {item}", styles["BodyText"])
        )

    story.append(
        Paragraph(
            "<br/><b>Resume Suggestions</b>",
            styles["Heading2"],
        )
    )

    for item in result.recommendations:
        story.append(
            Paragraph(f"• {item}", styles["BodyText"])
        )

    story.append(
        Paragraph(
            "<br/><b>Interview Questions</b>",
            styles["Heading2"],
        )
    )

    for i, question in enumerate(
        result.interview_questions,
        start=1,
    ):
        story.append(
            Paragraph(
                f"{i}. {question}",
                styles["BodyText"],
            )
        )

    doc.build(story)

    buffer.seek(0)

    return buffer

