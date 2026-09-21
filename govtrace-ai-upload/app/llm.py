from langchain_google_genai import ChatGoogleGenerativeAI

from app.config import (
    GEMINI_MODEL,
    require_environment_variables,
)


def get_llm() -> ChatGoogleGenerativeAI:
    require_environment_variables(
        "GOOGLE_API_KEY"
    )

    return ChatGoogleGenerativeAI(
        model=GEMINI_MODEL,
        max_retries=2,
    )