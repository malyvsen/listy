from pydantic_settings import BaseSettings


class Settings(BaseSettings):
    groq_api_key: str


settings: Settings
settings = Settings(_env_file=".env")  # type: ignore
