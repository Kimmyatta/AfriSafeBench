import os
from dataclasses import dataclass
from functools import lru_cache
from pathlib import Path

from dotenv import load_dotenv


PROJECT_ROOT = Path(__file__).resolve().parents[3]
load_dotenv(PROJECT_ROOT / ".env")


def _parse_csv_env(value: str | None, default: list[str]) -> list[str]:
    if not value:
        return default
    return [item.strip() for item in value.split(",") if item.strip()]


@dataclass(frozen=True)
class Settings:
    project_root: Path
    groq_api_key: str
    cors_origins: list[str]
    afrisafe_frameworks_index_dir: Path


@lru_cache(maxsize=1)
def get_settings() -> Settings:
    return Settings(
        project_root=PROJECT_ROOT,
        groq_api_key=os.getenv("GROQ_API_KEY", "").strip().strip("()\"'").strip(),
        cors_origins=_parse_csv_env(
            os.getenv("CORS_ORIGINS"),
            [
                "http://127.0.0.1:5173",
                "http://localhost:5173",
                "http://127.0.0.1:5174",
                "http://localhost:5174",
            ],
        ),
        afrisafe_frameworks_index_dir=PROJECT_ROOT
        / "data"
        / "afrisafebench"
        / "frameworks"
        / "faiss_index",
    )


def require_groq_api_key() -> str:
    api_key = get_settings().groq_api_key
    if not api_key:
        raise RuntimeError("GROQ_API_KEY is missing. Add it to .env or the server environment.")
    return api_key
