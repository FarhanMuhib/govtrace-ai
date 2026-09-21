import os
from pathlib import Path

from dotenv import load_dotenv


ROOT_DIR = Path(__file__).resolve().parent.parent

load_dotenv(ROOT_DIR / ".env")


# Gemini Configuration

GOOGLE_API_KEY = os.getenv(
    "GOOGLE_API_KEY"
)

GEMINI_MODEL = os.getenv(
    "GEMINI_MODEL",
    "gemini-3.5-flash-lite"
)


# Langfuse Configuration  <-- ADD HERE

LANGFUSE_PUBLIC_KEY = os.getenv(
    "LANGFUSE_PUBLIC_KEY"
)

LANGFUSE_SECRET_KEY = os.getenv(
    "LANGFUSE_SECRET_KEY"
)

LANGFUSE_BASE_URL = os.getenv(
    "LANGFUSE_BASE_URL",
    "https://us.cloud.langfuse.com"
)


# Project Paths

KNOWLEDGE_DIR = (
    ROOT_DIR /
    "data" /
    "knowledge"
)

CHROMA_DIR = (
    ROOT_DIR /
    "data" /
    "chroma"
)


def require_environment_variables(*names: str):

    missing = [
        name
        for name in names
        if not os.getenv(name)
    ]

    if missing:
        raise RuntimeError(
            "Missing environment variables: "
            + ", ".join(missing)
        )