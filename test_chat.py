from rag.retriever import Retriever
from services.gemini_service import GeminiService

retriever = Retriever()
gemini = GeminiService()

question = "Why is Richard Feynman famous?"

results = retriever.retrieve(question)

context = "\n\n".join(
    results["documents"][0]
)

answer = gemini.generate_response(
    question,
    context
)

print("\n")
print(answer)