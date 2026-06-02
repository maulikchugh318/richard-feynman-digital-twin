import uuid

from chromadb import PersistentClient
from sentence_transformers import SentenceTransformer

from config import settings


class SemanticMemory:

    def __init__(self):

        self.client = PersistentClient(
            path="data/memory_chroma"
        )

        self.collection = self.client.get_or_create_collection(
            name="user_memories"
        )

        self.embedding_model = SentenceTransformer(
            settings.EMBEDDING_MODEL
        )

    def store_memory(
        self,
        memory_text: str
    ):

        embedding = self.embedding_model.encode(
            memory_text
        ).tolist()

        memory_id = str(uuid.uuid4())

        self.collection.add(
            ids=[memory_id],
            documents=[memory_text],
            embeddings=[embedding]
        )

    def retrieve_memories(
        self,
        query: str,
        top_k: int = 3
    ):

        query_embedding = self.embedding_model.encode(
            query
        ).tolist()

        results = self.collection.query(
            query_embeddings=[query_embedding],
            n_results=top_k
        )

        docs = results["documents"][0]
        distances = results["distances"][0]

        print("\nRetrieved Memories:\n")

        for doc, distance in zip(docs, distances):
            print(
                f"Distance: {distance:.4f} | {doc}"
            )

        return docs

    def retrieve_best_memory(
        self,
        query: str
    ):

        query_embedding = self.embedding_model.encode(
            query
        ).tolist()

        results = self.collection.query(
            query_embeddings=[query_embedding],
            n_results=1
        )

        return results["documents"][0][0]

    def count(self):

        return self.collection.count()