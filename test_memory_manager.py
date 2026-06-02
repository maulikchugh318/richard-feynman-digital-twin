from memory.memory_manager import MemoryManager

memory = MemoryManager()

memory.add_user_message(
    "I am learning quantum electrodynamics."
)

memory.add_user_message(
    "I struggle with tensor calculus."
)

memory.add_user_message(
    "I am interested in relativity."
)

print("\nRelevant Memories:\n")

results = memory.get_relevant_memories(
    "What topics do I find difficult?"
)

print(results)