from chromadb import PersistentClient
from sentence_transformers import SentenceTransformer

from config import settings


class Retriever:

    def __init__(self):

        self.client = PersistentClient(
            path=settings.CHROMA_DB_PATH
        )

        self.collection = self.client.get_collection(
            settings.CHROMA_COLLECTION_NAME
        )

        self.embedding_model = SentenceTransformer(
            settings.EMBEDDING_MODEL
        )

    def retrieve(
        self,
        query: str,
        top_k: int = 5
    ):

        query_embedding = self.embedding_model.encode(
            query
        ).tolist()

        results = self.collection.query(
            query_embeddings=[query_embedding],
            n_results=top_k
        )

        return results