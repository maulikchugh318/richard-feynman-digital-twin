from memory.short_term import ShortTermMemory
from memory.long_term import LongTermMemory
from memory.semantic_memory import SemanticMemory


class MemoryManager:

    def __init__(self):

        self.short_term = ShortTermMemory()

        self.long_term = LongTermMemory()

        self.semantic_memory = SemanticMemory()

    def add_user_message(
        self,
        message
    ):

        # Short-term memory
        self.short_term.add_message(
            "user",
            message
        )

        # SQLite memory
        self.long_term.store_memory(
            f"User: {message}"
        )

        # Semantic memory
        self.semantic_memory.store_memory(
            f"User: {message}"
        )

    def add_assistant_message(
        self,
        message
    ):

        self.short_term.add_message(
            "assistant",
            message
        )

    def get_chat_history(self):

        return self.short_term.get_history()

    def get_long_term_memories(self):

        return self.long_term.get_memories()

    def get_relevant_memories(
        self,
        query,
        top_k=3
    ):

        return self.semantic_memory.retrieve_memories(
            query,
            top_k
        )