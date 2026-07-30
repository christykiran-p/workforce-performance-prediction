from langchain_core.documents import Document

from src.config.settings import KNOWLEDGE_BASE_PATH


class DocumentLoader:

    def __init__(self):
        self.knowledge_base_path = KNOWLEDGE_BASE_PATH

    def load(self):

        documents = []

        for file in self.knowledge_base_path.glob("*.txt"):

            text = file.read_text(encoding="utf-8")

            documents.append(
                Document(
                    page_content=text,
                    metadata={"source": file.name},
                )
            )

        return documents