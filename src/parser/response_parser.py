from pydantic import BaseModel, Field

class AnalysisResult(BaseModel):
    match_score: float
    matching_skills: list[str]
    missing_skills: list[str]
    strengths: list[str]
    recommendations: list[str]
    interview_questions: list[str] = Field(default_factory=list)