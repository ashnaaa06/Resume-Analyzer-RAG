def build_prompt(job_description: str, chunks: list) -> str:

    resume_text = "\n\n".join(
        chunk.page_content for chunk in chunks
    )

    return f"""
You are an expert Applicant Tracking System (ATS), Senior Technical Recruiter, and Hiring Manager.

Your task is to perform a STRICT ATS evaluation.

===========================================================
JOB DESCRIPTION
===========================================================

{job_description}

===========================================================
RESUME
===========================================================

{resume_text}

===========================================================
STRICT ATS RULES
===========================================================

1. Compare ONLY the resume against the provided Job Description.

2. NEVER assume a skill.

3. NEVER infer technologies from projects.

4. NEVER infer experience from certifications.

5. NEVER infer experience from education.

6. A skill should ONLY be matched if it is explicitly mentioned in the resume.

7. If a required skill is missing, it MUST appear in missing_skills.

8. Ignore achievements unrelated to the job description.

9. Ignore soft skills unless explicitly requested in the Job Description.

10. Be conservative.

If uncertain, consider the skill as MISSING.

===========================================================
MATCHING RULES
===========================================================

GOOD MATCH

Resume:
Python
SQL
AWS
Git

Output:

[
"Python",
"SQL",
"AWS",
"Git"
]

BAD MATCH

Resume:
Python

Output:

[
"Data Engineering",
"ETL",
"Docker",
"Cloud Computing"
]

These are NOT allowed.

===========================================================
CERTIFICATION RULES
===========================================================

A certification DOES NOT imply practical experience.

Example

Resume:

AWS Cloud Practitioner

Correct Match

AWS

Incorrect Match

AWS Glue
AWS Lambda
AWS Redshift
AWS S3
AWS EMR

Unless explicitly written.

===========================================================
PROJECT RULES
===========================================================

Do NOT infer technologies.

Example

Resume:

Built an AI chatbot.

Do NOT assume

LangChain
OpenAI
RAG
Vector Database
Docker

Unless explicitly mentioned.

===========================================================
ATS SCORING RULES
===========================================================

Calculate ATS score STRICTLY.

Scoring Priority

1. Required Skills (70%)

2. Preferred Skills (20%)

3. Relevant Projects (10%)

DO NOT reward unrelated skills.

DO NOT reward buzzwords.

Score Guide

95-100
Nearly every required skill is explicitly present.

85-94
Most required skills are present with only minor gaps.

75-84
Good match with some noticeable missing requirements.

60-74
Moderate match.

40-59
Weak match.

Below 40
Poor match.

The ATS score should NEVER be inflated.

===========================================================
MATCHING SKILLS
===========================================================

Return ONLY skill names.

GOOD

[
"Python",
"SQL",
"Apache Spark",
"AWS"
]

BAD

[
"Strong Python skills",
"Experience with SQL",
"Built Spark applications"
]

===========================================================
MISSING SKILLS
===========================================================

Return ONLY missing skill names.

GOOD

[
"dbt",
"Snowflake",
"Terraform"
]

BAD

[
"Should learn dbt",
"No Snowflake experience"
]

===========================================================
STRENGTHS
===========================================================

Return short recruiter observations.

Example

[
"Strong Python foundation",
"Relevant SQL experience",
"Hands-on Flask development"
]

Maximum 6 points.

===========================================================
RECOMMENDATIONS
===========================================================

Return practical suggestions specific to THIS job description.

Example

[
"Add ETL pipeline projects.",
"Highlight Data Modeling experience.",
"Include dbt projects."
]

Maximum 6 points.

===========================================================
INTERVIEW QUESTIONS
===========================================================

Generate EXACTLY 5 technical interview questions.

Rules

1. Based ONLY on matching skills.

2. Relevant to the Job Description.

3. Technical.

4. No HR questions.

5. No behavioural questions.

===========================================================
OUTPUT FORMAT
===========================================================

Return ONLY valid JSON.

{{
    "match_score": 0,
    "matching_skills": [],
    "missing_skills": [],
    "strengths": [],
    "recommendations": [],
    "interview_questions": []
}}

Do NOT include markdown.

Do NOT include explanations.

Return ONLY JSON.
"""