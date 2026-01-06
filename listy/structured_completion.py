import json
from typing import TypeVar

from cerebras.cloud.sdk.types.chat.chat_completion import ChatCompletionResponse
from pydantic import BaseModel

from listy.clients import cerebras_client

T = TypeVar("T", bound=BaseModel)


async def structured_completion(
    response_model: type[T],
    system_prompt: str,
    user_content: str,
) -> T:
    """Make a structured LLM completion that returns a validated Pydantic model."""
    completion = await cerebras_client.chat.completions.create(
        model="llama-3.3-70b",
        temperature=0,
        response_format={
            "type": "json_schema",
            "json_schema": {
                "name": f"{response_model.__name__.lower()}_schema",
                "strict": True,
                "schema": response_model.model_json_schema(),
            },
        },
        messages=[
            {"role": "system", "content": system_prompt},
            {"role": "user", "content": user_content},
        ],
    )
    if not isinstance(completion, ChatCompletionResponse):
        raise TypeError(f"Unexpected response type: {type(completion)}")
    response_content = completion.choices[0].message.content
    if response_content is None:
        raise ValueError("No content in response")
    return response_model.model_validate(json.loads(response_content))
