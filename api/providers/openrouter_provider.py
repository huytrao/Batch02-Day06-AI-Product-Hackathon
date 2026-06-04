"""OpenRouter provider (OpenAI-compatible Chat Completions surface)."""

from __future__ import annotations

import os
from typing import Any, Dict, List, Optional

from .openai_provider import OpenAIProvider


class OpenRouterProvider(OpenAIProvider):
    """OpenRouter uses an OpenAI-compatible Chat Completions surface."""

    def __init__(self) -> None:
        super().__init__(
            api_key_env="OPENROUTER_API_KEY",
            base_url=os.getenv("OPENROUTER_BASE_URL", "https://openrouter.ai/api/v1"),
            # gpt-4o-mini gives stable JSON formatting for the ReAct loop.
            default_model=os.getenv("OPENROUTER_MODEL", "openai/gpt-4o-mini"),
        )

    def chat_completion(
        self,
        messages: List[Dict[str, str]],
        model: Optional[str] = None,
        temperature: float = 0.1,
        **kwargs: Any,
    ) -> str:
        return super().chat_completion(messages, model, temperature, **kwargs)
