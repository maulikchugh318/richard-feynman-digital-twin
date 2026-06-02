from memory.semantic_memory import SemanticMemory

memory = SemanticMemory()

memory.store_memory(
    "User is learning quantum electrodynamics."
)

memory.store_memory(
    "User is interested in relativity."
)

memory.store_memory(
    "User struggles with tensor calculus."
)

results = memory.retrieve_memories(
    "Which topics do I find difficult?"
)

print(results)