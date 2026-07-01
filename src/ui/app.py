import sys
from pathlib import Path

project_root = Path(__file__).resolve().parents[2]
sys.path.append(str(project_root))

import streamlit as st
from helpers import save_uploaded_file
from src.pipeline.ingest_pipeline import ingest_resume
from src.llm.analyzer import analyze_resume

st.set_page_config(
    page_title="AI Resume Analyzer",
    page_icon="🚀",
    layout="wide"
)

st.markdown("""
<h1 style='text-align:center;'>
🚀 AI Resume Analyzer
</h1>

<p style='text-align:center; font-size:18px;'>
Upload your resume and compare it against any Job Description using AI-powered ATS analysis.
</p>
""", unsafe_allow_html=True)

st.divider()

col1, col2 = st.columns(2)

with col1:
    st.subheader("📄 Upload Resume")

    resume_file = st.file_uploader(
        "Choose Resume",
        type=["pdf", "docx"]
    )

with col2:
    st.subheader("💼 Job Description")

    job_description = st.text_area(
        "Paste Job Description",
        height=250
    )

st.divider()

analyze_btn = st.button(
    "🔍 Analyze Resume",
    use_container_width=True
)

if analyze_btn:

    if not resume_file:
        st.error("Please upload a resume.")
        st.stop()

    if not job_description.strip():
        st.error("Please enter a job description.")
        st.stop()

    try:

        with st.spinner(
          " AI is analyzing your resume. Please wait..."
        ):

            # Save uploaded resume
            resume_path = save_uploaded_file(
                resume_file
            )

            # Build vector store from uploaded resume
            vectorstore = ingest_resume(
                resume_path
            )

            # Analyze against uploaded resume
            result = analyze_resume(
                vectorstore,
                job_description
            )

        st.success("✅ Analysis Complete")

        # ----------------------------
        # ATS Score
        # ----------------------------
        st.subheader("📊 ATS Score")

        st.progress(result.match_score / 100)

        if result.match_score >= 80:
            st.success("🟢 Excellent Match")
        elif result.match_score >= 60:
            st.warning("🟡 Moderate Match")
        else:
            st.error("🔴 Low Match")

        st.divider()

        # ----------------------------
        # Dashboard Metrics
        # ----------------------------
        col1, col2, col3 = st.columns(3)

        with col1:
            st.metric(
                "ATS Score",
                f"{result.match_score}%"
            )

        with col2:
            st.metric(
                "Matched Skills",
                len(result.matching_skills)
            )

        with col3:
            st.metric(
                "Missing Skills",
                len(result.missing_skills)
            )

        st.divider()

        # ----------------------------
        # Matching Skills
        # ----------------------------
        st.subheader("✅ Matching Skills")

        for skill in result.matching_skills:
            st.success(skill)

        # ----------------------------
        # Missing Skills
        # ----------------------------
        st.subheader("❌ Missing Skills")

        for skill in result.missing_skills:
            st.error(skill)

        # ----------------------------
        # Strengths
        # ----------------------------
        st.subheader("⭐ Strengths")

        for strength in result.strengths:
            st.write(f"• {strength}")

        # ----------------------------
        # Recommendations
        # ----------------------------
        st.subheader("💡 Resume Suggestions")

        for recommendation in result.recommendations:
            st.write(f"• {recommendation}")

        # ----------------------------
        # Interview Questions
        # ----------------------------
        st.subheader("🎯 Interview Questions")

        for i, question in enumerate(
            result.interview_questions,
            start=1
        ):
            st.write(f"{i}. {question}")

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