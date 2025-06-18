from memory import Memory

memory = Memory()

memory.add_fact("The sky is blue", "semantic")
memory.add_procedure("Cooking", ["1. Get ingredients", "2. Cook", "3. Serve"], "Cooking a meal")
memory.add_interaction("Hello, how are you?", "I'm good, thank you!", {"weather": "sunny"})
memory.add_to_short_term_memory("I'm going to the store")

print(memory.facts)
print(memory.procedures)
print(memory.interactions)