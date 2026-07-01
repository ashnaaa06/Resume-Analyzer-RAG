def build_prompt(job_description: str, chunks: list) -> str:

    resume_text = "\n\n".join(
        chunk.page_content for chunk in chunks
    )

    return f"""
You are an expert ATS (Applicant Tracking System) and Senior Technical Recruiter.

Evaluate the resume STRICTLY against the provided Job Description.

=========================
JOB DESCRIPTION
=========================
{job_description}

=========================
RESUME
=========================
{resume_text}

RULES

1. Compare ONLY against the Job Description.
2. Never assume any skill.
3. A skill matches ONLY if explicitly written in BOTH the resume and Job Description.
4. Certifications DO NOT imply practical experience.
5. Projects DO NOT imply technologies unless explicitly mentioned.
6. Ignore unrelated achievements.
7. Ignore soft skills unless explicitly required.
8. If unsure, mark the skill as missing.
9. Never inflate ATS scores.

ATS SCORE

Weightage

• Required Skills = 70%
• Preferred Skills = 20%
• Relevant Projects / Experience = 10%

Scoring Guide

95-100 : Excellent Match

85-94 : Strong Match

75-84 : Good Match

60-74 : Moderate Match

Below 60 : Weak Match

OUTPUT RULES

matching_skills

• Return ONLY skill names.
• No explanations.
• No sentences.

Example

[
"Python",
"SQL",
"AWS",
"Git"
]

missing_skills

• Return ONLY missing skill names.

Example

[
"Docker",
"Snowflake",
"Apache Spark"
]

strengths

• Maximum 5 short recruiter observations.

recommendations

• Maximum 5 practical resume improvements.

interview_questions

Generate EXACTLY 5 technical interview questions.

Rules

• Based ONLY on matching skills.
• Relevant to the Job Description.
• No HR questions.
• No behavioural questions.

Return ONLY valid JSON.

{{
    "match_score": 0,
    "matching_skills": [],
    "missing_skills": [],
    "strengths": [],
    "recommendations": [],
    "interview_questions": []
}}

Return ONLY JSON.
"""