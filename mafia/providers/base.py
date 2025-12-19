from abc import ABC, abstractmethod


class ProviderBase(ABC):
    """Abstract provider for text generation."""

    def __init__(self, name: str):
        self.name = name

    @abstractmethod
    def generate(self, prompt: str) -> str:
        """Generate a response for the given prompt and return raw text."""
        raise NotImplementedError
