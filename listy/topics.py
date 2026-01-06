import json

from cerebras.cloud.sdk.types.chat.chat_completion import ChatCompletionResponse
from pydantic import BaseModel, Field

from listy.clients import cerebras_client


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

    completion = await cerebras_client.chat.completions.create(
        model="llama-3.3-70b",
        temperature=0,
        response_format={
            "type": "json_schema",
            "json_schema": {
                "name": "topics_schema",
                "strict": True,
                "schema": Topics.model_json_schema(),
            },
        },
        messages=[
            {
                "role": "system",
                "content": "Extract discussion threads. Summarize each distinct practice or phenomenon the author describes. Respond in the same language as the input text.",
            },
            {"role": "user", "content": text},
        ],
    )
    if not isinstance(completion, ChatCompletionResponse):
        raise TypeError(f"Unexpected response type: {type(completion)}")
    response_content = completion.choices[0].message.content
    if response_content is None:
        raise ValueError("No content in response")
    topics = Topics.model_validate(json.loads(response_content))
    return [thread.label for thread in topics.threads]
