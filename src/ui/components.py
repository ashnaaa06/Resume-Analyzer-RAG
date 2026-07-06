from pathlib import Path
print("Loaded components from:", Path(__file__).resolve())
import streamlit as st
from textwrap import dedent



def render_result_card(match_score: float):

    if match_score >= 80:
        status = "Excellent Match"
        status_color = "#16A34A"

    elif match_score >= 60:
        status = "Moderate Match"
        status_color = "#F59E0B"

    else:
        status = "Low Match"
        status_color = "#DC2626"

    st.markdown(
        f"""
            <div class="result-card">

            <div class="result-title">
            Resume Analysis Complete
            </div>

            <div class="result-score">
            {match_score:.1f}%
            </div>

            <div class="result-status" style="color:{status_color};">
            ● {status}
            </div>

            </div>
            """,
                    unsafe_allow_html=True,
            )

def render_metric_cards(match_score: float, matched_skills: int, missing_skills: int):

    col1, col2, col3 = st.columns(3)

    with col1:
        st.markdown(
            f"""<div class="metric-card">
<div class="metric-value">{match_score:.1f}%</div>
<div class="metric-title">ATS Score</div>
</div>""",
            unsafe_allow_html=True,
        )

    with col2:
        st.markdown(
            f"""<div class="metric-card">
<div class="metric-value">{matched_skills}</div>
<div class="metric-title">Matched Skills</div>
</div>""",
            unsafe_allow_html=True,
        )

    with col3:
        st.markdown(
            f"""<div class="metric-card">
<div class="metric-value">{missing_skills}</div>
<div class="metric-title">Missing Skills</div>
</div>""",
            unsafe_allow_html=True,
        )

def render_skill_chips(title: str, skills: list[str], chip_type: str = "success"):

    icon = title.split()[0]
    heading = " ".join(title.split()[1:])

    render_section_title(icon, heading)

    if not skills:
        st.info("No skills found.")
        return

    css_class = "skill-chip-success" if chip_type == "success" else "skill-chip-danger"

    chips = "".join(
        f'<span class="{css_class}">{skill}</span>'
        for skill in skills
    )

    st.markdown(
        f"""<div class="skill-chip-container">
{chips}
</div>""",
        unsafe_allow_html=True,
    )
    
    
    
def render_section_title(icon: str, title: str):

    st.markdown(
        f"""<div class="section-title">
<span class="section-icon">{icon}</span>
<span>{title}</span>
</div>""",
        unsafe_allow_html=True,
    )
    
    
    
def render_info_cards(
    icon: str,
    title: str,
    items: list[str],
    card_type: str = "default",
):

    render_section_title(icon, title)

    if not items:
        st.info("No information available.")
        return

    css_class = f"info-card {card_type}"

    for item in items:
        st.markdown(
            f"""<div class="{css_class}">
<div class="info-icon">{icon}</div>
<div class="info-text">{item}</div>
</div>""",
            unsafe_allow_html=True,
        )
    
def render_executive_summary(
    match_score: float,
    strengths: list[str],
    missing_skills: list[str],
):

    if match_score >= 80:
        intro = (
            "Your resume demonstrates a strong alignment with the job description "
            "and is likely to perform well in Applicant Tracking Systems."
        )
    elif match_score >= 60:
        intro = (
            "Your resume shows a moderate match with the job description. "
            "A few targeted improvements can significantly increase your ATS score."
        )
    else:
        intro = (
            "Your resume requires improvement to better align with the job description. "
            "Focus on adding missing skills and improving keyword relevance."
        )

    top_strengths = ", ".join(strengths[:3]) if strengths else "your technical profile"
    missing = ", ".join(missing_skills[:5]) if missing_skills else "None"

    st.markdown(
        f"""<div class="summary-card">
<div class="summary-title">✨ Executive Summary</div>

<div class="summary-text">
{intro}

<br><br>

<b>Key Strengths:</b> {top_strengths}

<br><br>

<b>Primary Missing Skills:</b> {missing}
</div>

</div>""",
        unsafe_allow_html=True,
    )