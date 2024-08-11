from pathlib import Path

from .groq_client import groq_client


async def transcribe(path: Path) -> str:
    with path.open("rb") as file:
        transcription = await groq_client.audio.transcriptions.create(
            file=file,
            model="whisper-large-v3",
            language="pl",
            temperature=0,
        )

    return transcription.text.strip()
