from src.ai.rag.rag_service import RAGService

rag = RAGService()

context = rag.retrieve_context(
    "High performer promotion leadership"
)

print(context)