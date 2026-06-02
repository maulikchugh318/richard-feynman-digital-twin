from rag.retriever import Retriever
from services.gemini_service import GeminiService
from memory.memory_manager import MemoryManager


retriever = Retriever()
gemini = GeminiService()
memory = MemoryManager()


memory.add_user_message(
    "I am learning quantum electrodynamics."
)

memory.add_user_message(
    "I struggle with tensor calculus."
)

question = "Can you explain QED in a simple way for me?"

rag_results = retriever.retrieve(question)

context = "\n\n".join(
    rag_results["documents"][0]
)

relevant_memories = memory.get_relevant_memories(
    question,
    top_k=3
)

answer = gemini.generate_response(
    question=question,
    context=context,
    memories=relevant_memories,
    max_words=125
)

memory.add_assistant_message(answer)

print("\nFeynman Twin Answer:\n")
print(answer)