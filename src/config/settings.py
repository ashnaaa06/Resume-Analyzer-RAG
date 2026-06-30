"""Application configuration loaded from environment variables."""

from functools import lru_cache
from pathlib import Path

from pydantic import Field, field_validator, model_validator
from pydantic_settings import BaseSettings, SettingsConfigDict

PROJECT_ROOT = Path(__file__).resolve().parent.parent.parent


class Settings(BaseSettings):
    """Central configuration for the Resume Analyzer RAG application."""

    model_config = SettingsConfigDict(
        env_file=PROJECT_ROOT / ".env",
        env_file_encoding="utf-8",
        extra="ignore",
        populate_by_name=True,
    )

    # --- API ---
    google_api_key: str = Field(
        ...,
        alias="GOOGLE_API_KEY",
        description="Google Gemini API key",
    )

    # --- Models ---
    gemini_model: str = Field(
        default="gemini-2.0-flash",
        alias="GEMINI_MODEL",
        description="Gemini model used for chat completions",
    )
    embedding_model: str = Field(
        default="text-embedding-004",
        alias="EMBEDDING_MODEL",
        description="Gemini model used for text embeddings",
    )

    # --- Chunking ---
    chunk_size: int = Field(
        default=1000,
        alias="CHUNK_SIZE",
        ge=100,
        le=8000,
        description="Maximum characters per text chunk",
    )
    chunk_overlap: int = Field(
        default=200,
        alias="CHUNK_OVERLAP",
        ge=0,
        le=1000,
        description="Overlapping characters between consecutive chunks",
    )

    # --- Retrieval ---
    retrieval_k: int = Field(
        default=4,
        alias="RETRIEVAL_K",
        ge=1,
        le=20,
        description="Number of chunks to retrieve per query",
    )

    # --- LLM ---
    llm_temperature: float = Field(
        default=0.2,
        alias="LLM_TEMPERATURE",
        ge=0.0,
        le=1.0,
        description="Sampling temperature for Gemini responses",
    )

    # --- Paths (overridable via env) ---
    data_dir: Path = Field(
        default=PROJECT_ROOT / "data",
        alias="DATA_DIR",
        description="Root directory for application data",
    )
    resumes_dir: Path = Field(
        default=PROJECT_ROOT / "data" / "resumes",
        alias="RESUMES_DIR",
        description="Directory for uploaded resume files",
    )
    chroma_dir: Path = Field(
        default=PROJECT_ROOT / "data" / "chroma_db",
        alias="CHROMA_DIR",
        description="Directory for persisted ChromaDB storage",
    )

    @field_validator("google_api_key")
    @classmethod
    def validate_api_key(cls, value: str) -> str:
        cleaned = value.strip()
        if not cleaned or cleaned == "your_api_key_here":
            raise ValueError(
                "GOOGLE_API_KEY is missing or still set to the placeholder. "
                "Copy .env.example to .env and add your key."
            )
        return cleaned

    @model_validator(mode="after")
    def validate_chunk_overlap(self) -> "Settings":
        if self.chunk_overlap >= self.chunk_size:
            raise ValueError("CHUNK_OVERLAP must be smaller than CHUNK_SIZE")
        return self

    def ensure_directories(self) -> None:
        """Create data directories if they do not exist."""
        for directory in (self.data_dir, self.resumes_dir, self.chroma_dir):
            directory.mkdir(parents=True, exist_ok=True)


@lru_cache
def get_settings() -> Settings:
    """Return a cached Settings instance."""
    instance = Settings()
    instance.ensure_directories()
    return instance


def __getattr__(name: str) -> Settings:
    if name == "settings":
        return get_settings()
    raise AttributeError(f"module {__name__!r} has no attribute {name!r}")
