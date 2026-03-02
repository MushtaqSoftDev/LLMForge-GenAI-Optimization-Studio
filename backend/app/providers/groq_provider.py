from app.config import settings
from app.providers.base import BaseLLMProvider
from app.schemas import GenerationParams


class GroqProvider(BaseLLMProvider):
    name = "groq"
    label = "Groq"

    def __init__(self):
        self._client = None

    def _get_client(self):
        if self._client is None:
            from openai import AsyncOpenAI

            self._client = AsyncOpenAI(
                api_key=settings.GROQ_API_KEY,
                base_url="https://api.groq.com/openai/v1",
            )
        return self._client

    async def generate(self, messages: list[dict], params: GenerationParams) -> str:
        response = await self._get_client().chat.completions.create(
            model="llama-3.1-8b-instant",
            messages=messages,
            max_tokens=params.max_tokens,
            temperature=params.temperature,
            top_p=params.top_p,
        )
        return response.choices[0].message.content or ""

    def is_available(self) -> bool:
        return bool(settings.GROQ_API_KEY)
