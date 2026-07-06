import sys
from pathlib import Path

project_root = Path(__file__).resolve().parents[2]
sys.path.append(str(project_root))

import streamlit as st

from src.ui.components import (
    render_result_card,
    render_metric_cards,
    render_skill_chips,
    render_executive_summary,
    render_info_cards,
    render_section_title,
)

from helpers import (
    save_uploaded_file,
    create_pdf_report,
)
from src.pipeline.ingest_pipeline import ingest_resume
from src.llm.analyzer import analyze_resume
def load_css():
    css_file = (
        Path(__file__).resolve().parents[1]
        / "assets"
        / "styles.css"
    )

    with open(css_file) as f:
        st.markdown(
            f"<style>{f.read()}</style>",
            unsafe_allow_html=True
        )

st.set_page_config(
    page_title="AI Resume Analyzer",
    page_icon="🚀",
    layout="wide"
)
load_css()

st.markdown(
    """
<div style="text-align:center; padding:40px;">

<div style="font-size:60px;">🚀</div>

<h1 style="font-size:52px; font-weight:700;">
AI Resume Intelligence Platform
</h1>

<p style="font-size:20px; color:gray;">
Match your resume against any Job Description with AI-powered ATS analysis.
</p>

</div>
""",
    unsafe_allow_html=True,
)

st.markdown("""
<div class="feature-row">

<div class="feature-pill">🎯 ATS Analysis</div>

<div class="feature-pill">📊 Skill Gap Analysis</div>

<div class="feature-pill">📄 Resume Optimization</div>

<div class="feature-pill">💬 Interview Preparation</div>

</div>
""", unsafe_allow_html=True)

col1, col2 = st.columns(2)

with col1:

    st.markdown("### 📄 Upload Resume")
    st.caption("PDF or DOCX, up to 200 MB")

    resume_file = st.file_uploader(
        "",
        type=["pdf", "docx"],
        label_visibility="collapsed"
    )


with col2:

    st.markdown("### 💼 Job Description")
    st.caption("Paste the complete job description below.")

    job_description = st.text_area(
        "",
        height=220,
        placeholder="Paste the job description here...",
        label_visibility="collapsed"
    )


analyze_btn = st.button(
    "🔍 Analyze Resume",
    use_container_width=True
)
if "analysis_result" not in st.session_state:
    st.session_state.analysis_result = None

if "pdf_report" not in st.session_state:
    st.session_state.pdf_report = None

if analyze_btn or st.session_state.analysis_result is not None:

    if not resume_file:
        st.error("Please upload a resume.")
        st.stop()

    if not job_description.strip():
        st.error("Please enter a job description.")
        st.stop()

    try:

        if analyze_btn:

            with st.spinner(
                "AI is analyzing your resume. Please wait..."
            ):

                resume_path = save_uploaded_file(
                    resume_file
                )

                vectorstore = ingest_resume(
                    resume_path
                )

                result = analyze_resume(
                    vectorstore,
                    job_description
                )

                st.session_state.analysis_result = result
                st.session_state.pdf_report = create_pdf_report(result)

        else:

            result = st.session_state.analysis_result
        st.success("✅ Analysis Complete")
        st.markdown(
            """
        <div style="background:green;color:white;padding:20px;">
        DIRECT HTML TEST
        </div>
        """,
            unsafe_allow_html=True,
        )


        # ----------------------------
        # ATS Score
        # ----------------------------
        print("1")
        render_result_card(result.match_score)

        print("2")
        render_metric_cards(
            result.match_score,
            len(result.matching_skills),
            len(result.missing_skills),
        )

        print("3")
        render_executive_summary(
            result.match_score,
            result.strengths,
            result.missing_skills,
        )

        print("4")
        render_skill_chips(
            "✅ Matching Skills",
            result.matching_skills,
            "success",
        )

        print("5")
        render_skill_chips(
            "❌ Missing Skills",
            result.missing_skills,
            "danger",
        )

        print("6")
        render_info_cards(
            "⭐",
            "Strengths",
            result.strengths,
            "success",
        )

        print("7")
        render_info_cards(
            "💡",
            "Resume Suggestions",
            result.recommendations,
            "warning",
        )

        print("8")
        render_section_title(
            "🎯",
            "Interview Questions"
        )

        print("9")

        for i, question in enumerate(
            result.interview_questions,
            start=1,
        ):
            with st.expander(f"Question {i}"):

                st.write(question)
        st.markdown("<br>", unsafe_allow_html=True)

        st.download_button(
            label="📄 Download Analysis Report",
            data=st.session_state.pdf_report,
            file_name="Resume_Analysis_Report.pdf",
            mime="application/pdf",
            use_container_width=True,
        )

    except Exception as e:

        error = str(e)

        if "RESOURCE_EXHAUSTED" in error or "429" in error:
            st.error(
            "⚠️ Gemini API quota exceeded. Please try again later or update your API key."
        )

        elif "INVALID_ARGUMENT" in error:
            st.error(
            "⚠️ Invalid request sent to Gemini."
        )

        else:
            st.error(f"Analysis failed:\n\n{error}")