from memory.memory_manager import MemoryManager

memory = MemoryManager()

memory.add_user_message(
    "I am learning CNNs"
)

memory.add_user_message(
    "I want to understand Transformers"
)

print(
    memory.get_long_term_memories()
)