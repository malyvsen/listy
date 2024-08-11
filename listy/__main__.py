from pathlib import Path

import asyncclick as aclick
from groq import AsyncGroq

from .settings import settings


@aclick.command()
@aclick.argument("path", type=aclick.Path(exists=True, dir_okay=False, path_type=Path))
async def transcribe(path: Path):
    groq = AsyncGroq(api_key=settings.groq_api_key)

    with path.open("rb") as file:
        print(f"Transcribing {path.as_posix()}")
        transcription = await groq.audio.transcriptions.create(
            file=file,
            model="whisper-large-v3",
            language="pl",
            temperature=0,
        )

    print(transcription.text.strip())


transcribe()
