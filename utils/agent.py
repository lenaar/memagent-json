from typing import List
from memory import Memory, DEFAULT_MEMORY_LOCATION
from prompts.facts import init_assistant_facts, init_system_prompt
from config.commands import FACT_KEY_COMMAND, PROCEDURE_KEY_COMMAND

class Agent:
    def __init__(self, api_key: str, memory_location: str = DEFAULT_MEMORY_LOCATION):
        self.api_key = api_key
        self.memory = Memory(memory_location)
        self.model_name = "gpt-4.1-nano"

        for fact in init_assistant_facts:
            self.memory.add_fact(fact)

    def get_system_prompt(self) -> str:
        return init_system_prompt
    
    def get_key_command(self, message: str, list_of_commands: List[str]) -> str:
        for key_command in list_of_commands:
            if key_command in message.lower():
                return key_command
        return None
    
    