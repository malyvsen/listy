import json

from cerebras.cloud.sdk.types.chat.chat_completion import ChatCompletionResponse
from pydantic import BaseModel

from listy.clients import cerebras_client


async def extract_main_argument(text: str) -> str:
    class MainArgument(BaseModel):
        """The author's main argument, stated concisely with key supporting points."""

        main_argument: str

    completion = await cerebras_client.chat.completions.create(
        model="llama-3.3-70b",
        temperature=0,
        response_format={
            "type": "json_schema",
            "json_schema": {
                "name": "main_argument_schema",
                "strict": True,
                "schema": MainArgument.model_json_schema(),
            },
        },
        messages=[
            {
                "role": "system",
                "content": "Find where the author sums up their view and state it in first person. Include their exact wording. Add a few supporting points. No third-person. Input language only.",
            },
            {"role": "user", "content": text},
        ],
    )
    if not isinstance(completion, ChatCompletionResponse):
        raise TypeError(f"Unexpected response type: {type(completion)}")
    response_content = completion.choices[0].message.content
    if response_content is None:
        raise ValueError("No content in response")
    return MainArgument.model_validate(json.loads(response_content)).main_argument
