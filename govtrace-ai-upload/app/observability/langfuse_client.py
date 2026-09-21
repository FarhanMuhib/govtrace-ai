from langfuse import Langfuse

from app.config import (
    LANGFUSE_PUBLIC_KEY,
    LANGFUSE_SECRET_KEY,
    LANGFUSE_BASE_URL,
)


def get_langfuse():

    return Langfuse(
        public_key=LANGFUSE_PUBLIC_KEY,
        secret_key=LANGFUSE_SECRET_KEY,
        base_url=LANGFUSE_BASE_URL,
    )