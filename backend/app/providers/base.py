from abc import ABC, abstractmethod

from app.schemas import GenerationParams


class BaseLLMProvider(ABC):
    name: str = ""
    label: str = ""

    @abstractmethod
    async def generate(self, messages: list[dict], params: GenerationParams) -> str:
        ...

    @abstractmethod
    def is_available(self) -> bool:
        ...
