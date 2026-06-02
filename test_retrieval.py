from rag.retriever import Retriever

retriever = Retriever()

results = retriever.retrieve(
    "What is Richard Feynman famous for?"
)

print(results)