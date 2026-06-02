from chromadb import PersistentClient
from sentence_transformers import SentenceTransformer

from config import settings


class VectorStore:

    def __init__(self):

        self.client = PersistentClient(
            path=settings.CHROMA_DB_PATH
        )

        self.collection = self.client.get_or_create_collection(
            name=settings.CHROMA_COLLECTION_NAME
        )

        self.embedding_model = SentenceTransformer(
            settings.EMBEDDING_MODEL
        )

    def add_documents(
        self,
        documents,
        metadatas,
        ids
    ):

        embeddings = self.embedding_model.encode(
            documents,
            show_progress_bar=True
        ).tolist()

        self.collection.add(
            documents=documents,
            embeddings=embeddings,
            metadatas=metadatas,
            ids=ids
        )

    def count(self):
        return self.collection.count()