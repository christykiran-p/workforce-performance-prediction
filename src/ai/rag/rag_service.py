from src.ai.rag.vector_store import VectorStore


class RAGService:

    def __init__(self):

        self.vector_db = VectorStore().build()

    def retrieve(self, query: str, k: int = 3):

        docs = self.vector_db.similarity_search(
            query,
            k=k,
        )

        return docs

    def retrieve_context(self, query: str, k: int = 3):

        docs = self.retrieve(query, k)

        return "\n\n".join(
            [
                doc.page_content
                for doc in docs
            ]
        )