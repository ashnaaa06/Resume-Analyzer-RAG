import json

from src.retrieval import retrieve_relevant_chunks
from src.llm.prompt_builder import build_prompt
from src.llm.gemini_client import generate_content
from src.parser import AnalysisResult


def analyze_resume(
    vectorstore,
    job_description: str
) -> AnalysisResult:

    chunks = retrieve_relevant_chunks(
        vectorstore,
        job_description
    )

    prompt = build_prompt(
        job_description,
        chunks,
    )

    response = generate_content(prompt)

    data = json.loads(response)

    return AnalysisResult(**data)