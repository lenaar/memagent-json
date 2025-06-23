from typing import List, Dict
from memory import Memory, DEFAULT_MEMORY_LOCATION
from prompts.facts import init_assistant_facts, init_system_prompt
from config.commands import FACT_KEY_COMMANDS, PROCEDURE_KEY_COMMANDS

class Agent:
    def __init__(self, api_key: str, memory_location: str = DEFAULT_MEMORY_LOCATION):
        self.api_key = api_key
        self.memory = Memory(memory_location)
        self.model_name = "gpt-4.1-nano"

        for fact in init_assistant_facts:
            self.memory.add_fact(fact, "fact")

    def get_system_prompt(self) -> str:
        return init_system_prompt
    
    def get_key_command(self, message: str, list_of_commands: List[str]) -> str:
        for key_command in list_of_commands:
            if key_command in message.lower():
                return key_command
        return None
    
    def learn_fact(self, message: str, key_command: str) -> None:
        try:
            fact = message.replace(key_command, "").strip()
            self.memory.add_fact(fact, "fact")
            print(f"Learned fact: {fact}")
        except Exception as e:
            print(f"Error learning fact: {e}. Format should be: {FACT_KEY_COMMANDS[0]} <fact>")
    
    def learn_procedure(self, message: str, key_command: str) -> None:
        try:
            start, steps = message.split(":", 1)
            procedure_name = start.replace(key_command, "").strip()
            steps = [f"{i+1}. {step.strip()}" for i, step in enumerate(steps.split(","))]
            self.memory.add_procedure(procedure_name, steps, "procedure")
            print(f"Learned procedure: {procedure_name} with steps: {steps}")
        except Exception as e:
            print(f"Error learning procedure: {e}. Format should be: {PROCEDURE_KEY_COMMANDS[0]} <procedure_name>: <step1>, <step2>, <step3>, ...")
    
