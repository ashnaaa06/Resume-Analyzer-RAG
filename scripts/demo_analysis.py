from src.llm.analyzer import analyze_resume

job_description = """
We are looking for a Python Developer with:

- Python
- Flask
- SQL
- Docker
- AWS
- Kubernetes
- CI/CD
- Microservices
- Unit Testing

Preferred:
- Redis
- Kafka
"""

result = analyze_resume(job_description)

print("\nATS Score:", result.match_score)

print("\nMatching Skills:")
for skill in result.matching_skills:
    print("-", skill)

print("\nMissing Skills:")
for skill in result.missing_skills:
    print("-", skill)

print("\nRecommendations:")
for rec in result.recommendations:
    print("-", rec)
print("\nStrengths:")
for strength in result.strengths:
    print("-", strength)

print("\nInterview Questions:")
for question in result.interview_questions:
    print("-", question)