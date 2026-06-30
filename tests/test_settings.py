"""Tests for application configuration."""

import os
from pathlib import Path

import pytest

from src.config.settings import PROJECT_ROOT, Settings, get_settings


@pytest.fixture(autouse=True)
def clear_settings_cache():
    """Ensure each test gets a fresh Settings instance."""
    get_settings.cache_clear()
    yield
    get_settings.cache_clear()


def test_project_root_points_to_repo_root():
    assert PROJECT_ROOT == Path(__file__).resolve().parent.parent
    assert (PROJECT_ROOT / "src" / "config" / "settings.py").exists()


def test_settings_loads_from_env(monkeypatch, tmp_path):
    monkeypatch.setenv("GOOGLE_API_KEY", "test-api-key-12345")
    monkeypatch.setenv("CHUNK_SIZE", "500")
    monkeypatch.setenv("CHUNK_OVERLAP", "50")
    monkeypatch.setenv("RETRIEVAL_K", "6")

    config = Settings()

    assert config.google_api_key == "test-api-key-12345"
    assert config.gemini_model == "gemini-2.0-flash"
    assert config.embedding_model == "models/embedding-001"
    assert config.chunk_size == 500
    assert config.chunk_overlap == 50
    assert config.retrieval_k == 6
    assert config.llm_temperature == 0.2


def test_settings_paths_default_to_project_data_dirs():
    config = Settings(google_api_key="test-api-key-12345")

    assert config.data_dir == PROJECT_ROOT / "data"
    assert config.resumes_dir == PROJECT_ROOT / "data" / "resumes"
    assert config.chroma_dir == PROJECT_ROOT / "data" / "chroma_db"


def test_settings_rejects_placeholder_api_key():
    with pytest.raises(ValueError, match="GOOGLE_API_KEY"):
        Settings(google_api_key="your_api_key_here")


def test_settings_rejects_overlap_gte_chunk_size():
    with pytest.raises(ValueError, match="CHUNK_OVERLAP"):
        Settings(
            google_api_key="test-api-key-12345",
            chunk_size=500,
            chunk_overlap=500,
        )


def test_ensure_directories_creates_paths(tmp_path, monkeypatch):
    data_dir = tmp_path / "data"
    resumes_dir = data_dir / "resumes"
    chroma_dir = data_dir / "chroma_db"

    config = Settings(
        google_api_key="test-api-key-12345",
        data_dir=data_dir,
        resumes_dir=resumes_dir,
        chroma_dir=chroma_dir,
    )

    config.ensure_directories()

    assert data_dir.is_dir()
    assert resumes_dir.is_dir()
    assert chroma_dir.is_dir()


def test_get_settings_is_cached(monkeypatch):
    monkeypatch.setenv("GOOGLE_API_KEY", "test-api-key-12345")

    first = get_settings()
    second = get_settings()

    assert first is second
