import os
from pathlib import Path


DEFAULT_DATABASE_PATH = Path(__file__).resolve().parent.parent / "students.db"


def get_database_path() -> Path:
    return Path(os.getenv("STUDENT_DATABASE_PATH", DEFAULT_DATABASE_PATH))


def get_ollama_model() -> str:
    return os.getenv("OLLAMA_MODEL", "llama3.2:1b")


def get_ollama_base_url() -> str | None:
    return os.getenv("OLLAMA_BASE_URL") or None