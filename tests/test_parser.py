from src.parser import AnalysisResult


def test_analysis_result():

    result = AnalysisResult(
        match_score=80,
        matching_skills=["Python"],
        missing_skills=["Docker"],
        strengths=["Good Python skills"],
        recommendations=["Learn Docker"]
    )

    assert result.match_score == 80