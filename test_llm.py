from src.ai.llm.factory import LLMFactory

llm = LLMFactory.create()

response = llm.generate(
    "Say hello in one sentence."
)

print(response)