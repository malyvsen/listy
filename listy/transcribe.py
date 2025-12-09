from pathlib import Path

from .clients import groq_client


async def transcribe(path: Path, language: str) -> str:
    with path.open("rb") as file:
        transcription = await groq_client.audio.transcriptions.create(
            file=file,
            model="whisper-large-v3",
            language=language,
            temperature=0,
        )

    return transcription.text.strip()
