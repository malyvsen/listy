import json

from cerebras.cloud.sdk.types.chat.chat_completion import ChatCompletionResponse
from pydantic import BaseModel

from listy.clients import cerebras_client


class MainArgument(BaseModel):
    main_argument: str


async def identify_main_argument(text: str) -> MainArgument:
    """Identify the main argument of a text using Cerebras."""
    completion = await cerebras_client.chat.completions.create(
        model="llama-3.3-70b",
        messages=[
            {
                "role": "system",
                "content": "You are a helpful assistant that identifies the main argument of a text. Extract the core thesis or central claim being made.",
            },
            {"role": "user", "content": text},
        ],
        response_format={
            "type": "json_schema",
            "json_schema": {
                "name": "main_argument_schema",
                "strict": True,
                "schema": MainArgument.model_json_schema(),
            },
        },
    )
    if not isinstance(completion, ChatCompletionResponse):
        raise TypeError(f"Unexpected response type: {type(completion)}")
    response_content = completion.choices[0].message.content
    if response_content is None:
        raise ValueError("No content in response")
    return MainArgument.model_validate(json.loads(response_content))
