import os
import requests
from typing import List, Dict, Any, Optional

class OpenAIProvider:
    """Base provider for OpenAI-compatible Chat Completions endpoints."""

    def __init__(self, api_key_env: str = "OPENAI_API_KEY", base_url: str = "https://api.openai.com/v1", default_model: str = "gpt-3.5-turbo") -> None:
        self.api_key_env = api_key_env
        self.api_key = os.getenv(api_key_env, "")
        self.base_url = base_url
        self.default_model = default_model

    def chat_completion(self, messages: List[Dict[str, str]], model: Optional[str] = None, temperature: float = 0.1, **kwargs) -> str:
        """
        Sends a request to the chat completion endpoint and returns the text response.
        """
        if not self.api_key:
            raise ValueError(f"Missing API key: Environment variable '{self.api_key_env}' is not set.")

        headers = {
            "Authorization": f"Bearer {self.api_key}",
            "Content-Type": "application/json"
        }
        
        # Inject any extra headers provided by child classes
        if "extra_headers" in kwargs:
            headers.update(kwargs["extra_headers"])

        payload = {
            "model": model or self.default_model,
            "messages": messages,
            "temperature": temperature
        }

        response = requests.post(
            f"{self.base_url}/chat/completions",
            headers=headers,
            json=payload
        )
        
        if response.status_code != 200:
            raise Exception(f"API Error {response.status_code}: {response.text}")
            
        return response.json()["choices"][0]["message"]["content"]
