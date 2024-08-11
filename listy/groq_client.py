from groq import AsyncGroq

from .settings import settings

groq_client = AsyncGroq(api_key=settings.groq_api_key)
