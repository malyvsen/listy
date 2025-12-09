from pathlib import Path

import asyncclick as aclick
from tqdm import tqdm

from .transcribe import transcribe


@aclick.command()
@aclick.argument(
    "paths",
    type=aclick.Path(exists=True, dir_okay=False, path_type=Path),
    nargs=-1,
    required=True,
)
@aclick.option("--language", default="pl")
async def main(paths: tuple[Path, ...], language: str):
    """Transcribe audio files, printing to the console."""

    transcriptions = [
        await transcribe(path, language) for path in tqdm(paths, desc="Transcribing")
    ]

    joined_text = "\n\n".join(transcriptions)
    print(joined_text)


main()
