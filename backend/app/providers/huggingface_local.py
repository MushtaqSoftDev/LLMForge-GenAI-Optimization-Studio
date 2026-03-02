import asyncio

from app.config import settings
from app.providers.base import BaseLLMProvider
from app.schemas import GenerationParams


class HuggingFaceLocalProvider(BaseLLMProvider):
    name = "huggingface"
    label = "HuggingFace Local (Free / CPU)"

    def __init__(self):
        self._pipeline = None

    def _load(self):
        if self._pipeline is not None:
            return
        from transformers import pipeline

        self._pipeline = pipeline(
            "text2text-generation",
            model=settings.HF_MODEL_NAME,
            device=-1,
        )

    async def generate(self, messages: list[dict], params: GenerationParams) -> str:
        self._load()

        # FLAN-T5 is instruction-focused: format as a single prompt for text2text
        if not messages:
            return ""
        last = messages[-1]
        if last["role"] != "user":
            return ""
        user_input = last["content"]
        lower = user_input.lower()
        # FLAN-T5 responds better to task-prefixed prompts; use "sentiment:" for classification
        is_sentiment = any(w in lower for w in ["sentiment", "positive", "negative", "neutral"]) and (
            "classify" in lower or "sentence" in lower
        )
        if is_sentiment:
            # For few-shot "A" → X "B" → Y "C" → extract LAST quoted text (the one to classify)
            import re
            all_quoted = re.findall(r'"([^"]+)"', user_input)
            text = all_quoted[-1] if all_quoted else user_input.split(":")[-1].strip().strip('"')
            prompt = f"sentiment: {text}"
        elif len(messages) > 1:
            context = " ".join(
                m["content"] for m in messages[:-1] if m["role"] == "user"
            )
            prompt = f"Context: {context}\n\nQuestion: {user_input}\n\nAnswer:"
        else:
            prompt = f"Question: {user_input}\n\nAnswer:"

        # Temp=0 + very low top_k often cause repetitive loops; use a small temp floor when temp is 0.
        temperature = max(params.temperature, 0.1) if params.temperature <= 0 else params.temperature
        # For classification/sentiment, cap tokens to force short answers
        max_tokens = min(params.max_tokens, 15) if is_sentiment else params.max_tokens
        result = await asyncio.to_thread(
            self._pipeline,
            prompt,
            max_new_tokens=max_tokens,
            temperature=temperature,
            top_p=params.top_p,
            top_k=params.top_k,
            do_sample=True,
            num_return_sequences=1,
            repetition_penalty=1.5,
            no_repeat_ngram_size=3,
        )
        return (result[0].get("generated_text") or "").strip()

    def is_available(self) -> bool:
        return True
