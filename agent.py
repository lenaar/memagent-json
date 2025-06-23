from typing import List, Dict
from memory import Memory, DEFAULT_MEMORY_LOCATION
from prompts.facts import init_assistant_facts, init_system_prompt
from config.commands import FACT_KEY_COMMANDS, PROCEDURE_KEY_COMMANDS
from openai import OpenAI
from dotenv import load_dotenv

load_dotenv()

class Agent:
    def __init__(self, memory_location: str = DEFAULT_MEMORY_LOCATION):
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
            if fact: 
                self.memory.add_fact(fact, "fact")
                print(f"Learned fact: {fact}")
            else:
                print(f"No fact found in message: {message}.")
        except Exception as e:
            print(f"Error learning fact: {e}. Format should be: {FACT_KEY_COMMANDS[0]} <fact>")
    
    def learn_procedure(self, message: str, key_command: str) -> None:
        try:
            start, steps = message.split(":", 1)
            procedure_name = start.replace(key_command, "").strip()
            steps = [f"{i+1}. {step.strip()}" for i, step in enumerate(steps.split(","))]
            if len(steps) > 0: 
                self.memory.add_procedure(procedure_name, steps, "procedure")
                print(f"Learned procedure: {procedure_name} with steps: {steps}")
            else:
                print(f"No steps found in message: {message}.")
        except Exception as e:
            print(f"Error learning procedure: {e}. Format should be: {PROCEDURE_KEY_COMMANDS[0]} <procedure_name>: <step1>, <step2>, <step3>, ...")
    
    def extract_and_learn(self, message: str) -> str:
        learn_fact_key_command = self.get_key_command(message, FACT_KEY_COMMANDS)
        learn_procedure_key_command = self.get_key_command(message, PROCEDURE_KEY_COMMANDS)

        if learn_fact_key_command:
            self.learn_fact(message, learn_fact_key_command)
            return "learned fact"
        elif learn_procedure_key_command:
            self.learn_procedure(message, learn_procedure_key_command)
            return "learned procedure"
        else:
            print(f"No key command found in message: {message}. Proceed to create a context for the user's question.")
            return "no key command found"

    def build_messages(self, message: str) -> List[Dict[str, str]]:
        context = self.memory.get_context(message)
        messages = [
            {"role": "system", "content": self.get_system_prompt()},
            {"role": "system", "content": f"Context: {context}"},
            {"role": "user", "content": message}
        ]
        return messages

    def call_openai_api(self, messages: List[Dict[str, str]]) -> str:
        try:
            client = OpenAI()
            response = client.chat.completions.create(model=self.model_name, messages=messages, temperature=0.5, max_tokens=1000)
            content = response.choices[0].message.content
            print(f"Response from OpenAI: {content}")
            return content
        except Exception as e:
            print(f"Error getting response from OpenAI: {e}")
            return None

    
    def process_message(self, message: str) -> str:
        self.extract_and_learn(message)
        messages = self.build_messages(message)
        response = self.call_openai_api(messages)
        if response: 
            self.memory.add_interaction(message, response)
        
        return response