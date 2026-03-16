import json
from collections.abc import AsyncGenerator

import aiohttp

from app.config import settings


async def stream_chat_completion(
    request_body: dict,
) -> AsyncGenerator[str, None]:
    api_url = settings.OPENAI_API_BASE_URL
    api_key = settings.OPENAI_API_KEY

    headers = {
        "Authorization": f"Bearer {api_key}",
        "Content-Type": "application/json",
    }

    body = {**request_body, "stream": True}

    async with aiohttp.ClientSession() as session:
        async with session.post(
            f"{api_url}/chat/completions",
            headers=headers,
            json=body,
        ) as response:
            if response.status != 200:
                error_text = await response.text()
                error_data = {
                    "error": {
                        "message": f"LLM API error ({response.status}): {error_text}",
                        "type": "upstream_error",
                    }
                }
                yield f"data: {json.dumps(error_data)}\n\n"
                yield "data: [DONE]\n\n"
                return

            async for line in response.content:
                decoded = line.decode("utf-8").strip()
                if decoded.startswith("data: "):
                    yield decoded + "\n\n"
                    if decoded == "data: [DONE]":
                        return
