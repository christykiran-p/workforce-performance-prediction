"""
Ollama LLM Client
"""

from __future__ import annotations

import ollama

from src.ai.llm.base import BaseLLM
from src.config.settings import (
    OLLAMA_MODEL,
    OLLAMA_HOST,
)


class OllamaClient(BaseLLM):
    """
    Local Ollama implementation.
    """

    def __init__(self):
        self.model = OLLAMA_MODEL
        self.host = OLLAMA_HOST

        # Create a reusable Ollama client
        self.client = ollama.Client(host=self.host)

    def generate(self, prompt: str) -> str:
        """
        Generate a response using Ollama.
        """

        response = self.client.chat(
            model=self.model,
            messages=[
                {
                    "role": "user",
                    "content": prompt,
                }
            ],
        )

        return response["message"]["content"].strip()