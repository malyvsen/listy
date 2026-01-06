from pydantic import BaseModel

from listy.structured_completion import structured_completion


async def extract_main_argument(text: str) -> str:
    class MainArgument(BaseModel):
        """The author's main argument, stated concisely with key supporting points."""

        main_argument: str

    result = await structured_completion(
        response_model=MainArgument,
        system_prompt="Find where the author sums up their view and state it in first person. Include their exact wording. Add a few supporting points. No third-person. Input language only.",
        user_content=text,
    )
    return result.main_argument
