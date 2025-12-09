import os

from cerebras.cloud.sdk import AsyncCerebras
from groq import AsyncGroq


def read_env_var(name: str) -> str:
    value = os.environ.get(name)
    if not value:
        raise ValueError(f"{name} environment variable is not set")
    return value


groq_client = AsyncGroq(api_key=read_env_var("GROQ_API_KEY"))
cerebras_client = AsyncCerebras(api_key=read_env_var("CEREBRAS_API_KEY"))
