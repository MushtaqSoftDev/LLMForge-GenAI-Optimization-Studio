from app.providers.base import BaseLLMProvider
from app.providers.deepseek import DeepSeekProvider
from app.providers.gemini_provider import GeminiProvider
from app.providers.groq_provider import GroqProvider
from app.providers.huggingface_local import HuggingFaceLocalProvider
from app.providers.openai_provider import OpenAIProvider
from app.schemas import GenerationParams

_providers: dict[str, BaseLLMProvider] = {}


def _init_providers() -> dict[str, BaseLLMProvider]:
    if _providers:
        return _providers
    for cls in [
        OpenAIProvider,
        DeepSeekProvider,
        GroqProvider,
        GeminiProvider,
        HuggingFaceLocalProvider,
    ]:
        instance = cls()
        _providers[instance.name] = instance
    return _providers


def get_all_providers() -> list[BaseLLMProvider]:
    return list(_init_providers().values())


async def generate_reply(
    provider_name: str,
    messages: list[dict],
    params: GenerationParams,
) -> str:
    providers = _init_providers()
    provider = providers.get(provider_name)
    if not provider:
        raise ValueError(f"Unknown provider: {provider_name}")
    if not provider.is_available():
        raise ValueError(
            f"Provider '{provider.label}' is not configured. "
            "Add its API key to .env or use the free HuggingFace provider."
        )
    return await provider.generate(messages, params)
