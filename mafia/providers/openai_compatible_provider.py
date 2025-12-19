import os
from typing import Optional

import httpx

from .base import ProviderBase


class OpenAICompatibleProvider(ProviderBase):
    """Provider for DeepSeek and xAI compatible chat completion APIs."""

    def __init__(self, base_url: str, api_key_env: str, model: str):
        api_key = os.environ.get(api_key_env)
        if not api_key:
            raise ValueError(f"{api_key_env} is required for OpenAICompatibleProvider")
        super().__init__(name=base_url)
        self.base_url = base_url.rstrip("/")
        self.api_key = api_key
        self.model = model
        self.client = httpx.Client(base_url=self.base_url, timeout=60.0)

    def generate(self, prompt: str) -> str:
        payload = {
            "model": self.model,
            "messages": [{"role": "user", "content": prompt}],
        }
        headers = {"Authorization": f"Bearer {self.api_key}"}
        response = self.client.post("/v1/chat/completions", json=payload, headers=headers)
        response.raise_for_status()
        data = response.json()
        choices = data.get("choices", [])
        if choices:
            message = choices[0].get("message", {})
            content: Optional[str] = message.get("content")
            if content:
                return content
        return ""
