from __future__ import annotations

import os

from .openai_provider import OpenAIProvider


class OpenRouterProvider(OpenAIProvider):
    """OpenRouter uses an OpenAI-compatible Chat Completions surface."""

    def __init__(self) -> None:
        super().__init__(
            api_key_env="OPENROUTER_API_KEY",
            base_url=os.getenv("OPENROUTER_BASE_URL", "https://openrouter.ai/api/v1"),
            default_model="openai/gpt-4o-mini", # Note: Using gpt-4o-mini for better JSON formatting stability
        )

    def chat_completion(self, messages: list[dict[str, str]], model: str | None = None, temperature: float = 0.1, **kwargs) -> str:
        """
        Overrides the base chat_completion.
        """
        return super().chat_completion(messages, model, temperature, **kwargs)
