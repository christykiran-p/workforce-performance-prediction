from src.ai.rag.vector_store import VectorStore

store = VectorStore()

db = store.build()

print(f"Documents Indexed: {db.index.ntotal}")