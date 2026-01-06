from pydantic import BaseModel, Field

from listy.structured_completion import structured_completion


async def extract_topics(text: str) -> list[str]:
    class Thread(BaseModel):
        """A single discussion thread from the text."""

        observation: str = Field(
            description="One sentence describing a specific practice, institution, or phenomenon the author discusses."
        )
        label: str = Field(
            description="1-3 word label for this specific phenomenon. Not generic words like 'people' or 'technology'."
        )

    class Topics(BaseModel):
        """Extract the main discussion threads from the text."""

        threads: list[Thread] = Field(
            description="The distinct practices, institutions, vocabulary, or phenomena the author describes. Group related examples under one thread."
        )

    topics = await structured_completion(
        response_model=Topics,
        system_prompt="Extract discussion threads. Summarize each distinct practice or phenomenon the author describes. Respond in the same language as the input text.",
        user_content=text,
    )
    return [thread.label for thread in topics.threads]
