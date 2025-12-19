import os
from openai import OpenAI

from .base import ProviderBase


class OpenAIProvider(ProviderBase):
    """Provider using OpenAI Responses API."""

    def __init__(self, model: str = "gpt-4o-mini"):
        api_key = os.environ.get("OPENAI_API_KEY")
        if not api_key:
            raise ValueError("OPENAI_API_KEY is required for OpenAIProvider")
        super().__init__(name="OpenAI")
        self.client = OpenAI(api_key=api_key)
        self.model = model

    def generate(self, prompt: str) -> str:
        response = self.client.responses.create(
            model=self.model,
            input=prompt,
        )
        # Responses API returns output as a list; pick first text segment
        for item in response.output:
            if item.type == "message" and item.content:
                return "".join(part.text for part in item.content if hasattr(part, "text"))
            if item.type == "output_text":
                return getattr(item, "text", "")
        return ""
