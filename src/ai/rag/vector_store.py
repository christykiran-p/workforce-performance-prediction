from langchain_community.vectorstores import FAISS
from langchain_ollama import OllamaEmbeddings

from src.ai.rag.document_loader import DocumentLoader
from src.config.settings import (
    EMBEDDING_MODEL,
    OLLAMA_HOST,
)


class VectorStore:

    _vector_db = None

    def __init__(self):

        self.loader = DocumentLoader()

        self.embeddings = OllamaEmbeddings(
            model=EMBEDDING_MODEL,
            base_url=OLLAMA_HOST,
        )

    def build(self):

        if VectorStore._vector_db is None:

            documents = self.loader.load()

            VectorStore._vector_db = FAISS.from_documents(
                documents,
                self.embeddings,
            )

        return VectorStore._vector_db