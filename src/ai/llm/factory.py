"""
LLM Factory
"""

from __future__ import annotations

from src.ai.llm.ollama_client import OllamaClient


class LLMFactory:
    """
    Factory for creating LLM clients.
    """

    @staticmethod
    def create(provider: str = "ollama"):

        provider = provider.lower()

        if provider == "ollama":
            return OllamaClient()

        raise ValueError(
            f"Unsupported LLM provider: {provider}"
        )