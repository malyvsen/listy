import os

from groq import AsyncGroq

_ENV_VAR_NAME = "GROQ_API_KEY"
_api_key = os.environ.get(_ENV_VAR_NAME)
if not _api_key:
    raise ValueError(f"{_ENV_VAR_NAME} environment variable is not set")

groq_client = AsyncGroq(api_key=_api_key)
