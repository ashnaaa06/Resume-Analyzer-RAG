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

    print("\n========== GEMINI RAW RESPONSE ==========")
    print(repr(response))
    print("=========================================\n")

    if not response:
        raise Exception("Gemini returned an empty response.")

    response = response.strip()


    if response.startswith("```json"):
        response = response[7:]

    if response.startswith("```"):
        response = response[3:]

    if response.endswith("```"):
        response = response[:-3]

    response = response.strip()

    print("\n========== CLEANED RESPONSE ==========")
    print(response)
    print("======================================\n")

    data = json.loads(response)

    return AnalysisResult(**data)