from pathlib import Path

import asyncclick as aclick
from tqdm import tqdm

from .transcribe import transcribe


@aclick.command()
@aclick.argument(
    "paths", type=aclick.Path(exists=True, dir_okay=False, path_type=Path), nargs=-1
)
async def main(paths: tuple[Path, ...]):
    transcriptions = [
        await transcribe(path) for path in tqdm(paths, desc="Transcribing")
    ]

    joined_text = "\n\n".join(transcriptions)
    print(joined_text)


main()
