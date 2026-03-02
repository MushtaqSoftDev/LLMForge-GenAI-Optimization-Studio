"""Map provider API errors to user-friendly messages."""

FRIENDLY_MESSAGES = {
    401: (
        "Invalid or expired API key. Try another provider (e.g. Groq or free HuggingFace), "
        "or check your API key in .env."
    ),
    429: (
        "Rate limit or free tier exhausted. Try another provider, or wait a moment and try again."
    ),
    500: "Provider temporarily unavailable. Try another provider or try again later.",
    502: "Provider temporarily unavailable. Try another provider or try again later.",
    503: "Provider temporarily unavailable. Try another provider or try again later.",
}


def _is_auth_error(err_text: str) -> bool:
    lower = (err_text or "").lower()
    return (
        "401" in err_text
        or "error code: 401" in lower
        or "authentication fail" in lower
        or ("invalid" in lower and ("api key" in lower or "authentication" in lower))
    )


def _is_rate_limit_error(err_text: str) -> bool:
    lower = (err_text or "").lower()
    return "429" in err_text or "rate limit" in lower or "quota" in lower


def to_user_friendly(exc: Exception, provider_name: str = "") -> str:
    """Convert a provider exception to a user-friendly message."""
    err_text = str(exc)

    # First: text-based fallback (works even if SDK types differ across versions)
    if _is_auth_error(err_text):
        return FRIENDLY_MESSAGES[401]
    if _is_rate_limit_error(err_text):
        return FRIENDLY_MESSAGES[429]

    # Try OpenAI SDK exception types (used by DeepSeek, Groq, OpenAI)
    try:
        from openai import APIStatusError, AuthenticationError, RateLimitError

        if isinstance(exc, AuthenticationError):
            return FRIENDLY_MESSAGES[401]
        if isinstance(exc, RateLimitError):
            return FRIENDLY_MESSAGES[429]
        if isinstance(exc, APIStatusError):
            code = getattr(exc, "status_code", None)
            if code in FRIENDLY_MESSAGES:
                return FRIENDLY_MESSAGES[code]
            if code and 400 <= code < 500:
                return FRIENDLY_MESSAGES[401]  # Likely auth
            if code and code >= 500:
                return FRIENDLY_MESSAGES[500]
    except ImportError:
        pass

    # Already friendly (e.g. ValueError from chat_service)
    if "Try another" in err_text or "Add its API key" in err_text:
        return err_text

    # Generic fallback
    labels = {"deepseek": "DeepSeek", "groq": "Groq", "openai": "OpenAI", "gemini": "Gemini", "huggingface": "HuggingFace"}
    label = labels.get((provider_name or "").lower(), provider_name or "the provider")
    return (
        f"Something went wrong with {label}. "
        "Try another provider (e.g. Groq or free HuggingFace) or try again later."
    )
