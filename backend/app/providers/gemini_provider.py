import asyncio

import google.generativeai as genai

from app.config import settings
from app.providers.base import BaseLLMProvider
from app.schemas import GenerationParams


class GeminiProvider(BaseLLMProvider):
    name = "gemini"
    label = "Google Gemini"

    def __init__(self):
        if settings.GEMINI_API_KEY:
            genai.configure(api_key=settings.GEMINI_API_KEY)

    async def generate(self, messages: list[dict], params: GenerationParams) -> str:
        model = genai.GenerativeModel("gemini-1.5-flash")
        config = genai.types.GenerationConfig(
            max_output_tokens=params.max_tokens,
            temperature=params.temperature,
            top_p=params.top_p,
            top_k=params.top_k,
        )
        prompt = "\n".join(
            f"{m['role'].capitalize()}: {m['content']}" for m in messages
        )
        response = await asyncio.to_thread(
            model.generate_content, prompt, generation_config=config
        )
        return response.text

    def is_available(self) -> bool:
        return bool(settings.GEMINI_API_KEY)
