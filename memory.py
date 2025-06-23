import json
import os
import datetime
from typing import List, Dict, Any, Optional
from dotenv import load_dotenv
from utils.json_file_utils import create_folder, load_json_file, save_to_json_file
from utils.search import search_keywords


load_dotenv()

def get_fact_content(fact: Dict[str, Any]) -> str:
    return fact["fact"]

def get_procedure_content(procedure: Dict[str, Any]) -> str:
    return f"{procedure.get('name', '')} {procedure.get('description', '')}"

def get_interaction_content(interaction: Dict[str, Any], separator: str = "") -> str:
    return f"user: {interaction['user_message']} {separator}agent: {interaction['agent_message']}"

DEFAULT_MEMORY_LOCATION = "./json_memory"

class Memory:
    # facts: list of facts, knowledge about the world, semantic memory
    # procedures: dict of procedures, smth can be done on autopilot, procedural memory
    # interactions: list of interactions, episodic memory
    # short_term_memory: fast access to latest information, working memory
    
    
    def __init__(self, location: str = DEFAULT_MEMORY_LOCATION):
        self.location = location
        create_folder(location)

        self.facts = load_json_file(location, "facts.json") or []
        self.procedures = load_json_file(location, "procedures.json") or {}
        self.interactions = load_json_file(location, "interactions.json") or []

        self.short_term_memory = []
        self.short_term_memory_size = 10

    def add_memory(self, memory: Dict[str, Any]):
        self.memory.append(memory)

    def add_fact(self, fact: str, type: str):
        self.facts.append({
            "fact": fact,
            "type": type,
            "timestamp": datetime.datetime.now().isoformat()
        })
        
        save_to_json_file(self.location, "facts.json", self.facts)

    def add_procedure(self, procedure: str, steps:List[str], description: str):
        self.procedures[procedure] = {
            "description": description,
            "name": procedure,
            "steps": steps,
            "timestamp": datetime.datetime.now().isoformat()
        }
        save_to_json_file(self.location, "procedures.json", self.procedures)
        
    def add_interaction(self, user_message: str, agent_message: str, metadata: Dict[str, Any] = None) -> None:
        self.interactions.append({
            "agent_message": agent_message,
            "user_message": user_message,
            "metadata": metadata,
            "timestamp": datetime.datetime.now().isoformat()
        })
        save_to_json_file(self.location, "interactions.json", self.interactions)
        
    def add_to_short_term_memory(self, memory: str, importance: float = 1.0) -> None:
        self.short_term_memory.append({
            "content": memory,
            "importance": importance,
            "timestamp": datetime.datetime.now().isoformat()
            })
        save_to_json_file(self.location, "short_term_memory.json", self.short_term_memory)
    
    def search_facts(self, query: str, limit: int = 3) -> List[Dict[str, Any]]:
        """Search facts using keyword matching."""
        return search_keywords(query, self.facts, fn=get_fact_content, limit=limit)
    
    def search_procedures(self, query: str, limit: int = 3) -> List[Dict[str, Any]]:
        return search_keywords(query, self.procedures.values(), fn=get_procedure_content, limit=limit)
    
    def search_interactions(self, query: str, limit: int = 3) -> List[Dict[str, Any]]:
        return search_keywords(query, self.interactions, fn=get_interaction_content, limit=limit)
    
    def search_recent_interactions(self, limit: int = 3) -> List[Dict[str, Any]]:
        return self.interactions[-limit:]
    
    def sort_short_term_memory(self) -> None:
        return sorted(self.short_term_memory, key=lambda x: (x["importance"], x["timestamp"]), reverse=True)
        
    # Generate a context string for the LLM using relevant memory.
    def get_context(self, query: str, limit: int = 3) -> str:
        recent_interactions = self.search_recent_interactions(limit=limit)
        recent_interactions_context = "\n".join([get_interaction_content(interaction, separator="\n") for interaction in recent_interactions])
        facts = self.search_facts(query, limit=limit)
        facts_context = "\n".join([f"Fact: {fact['fact']}" for fact in facts])
        procedures = self.search_procedures(query, limit=limit)
        procedures_context = "\n".join([f"Procedure {i+1}. {procedure['name']}: {procedure['description']} {chr(10)}Procedure's Steps: {chr(10).join(procedure['steps'])}" for i, procedure in enumerate(procedures)])

        print(f"Recent interactions: {recent_interactions_context}")
        print(f"Facts: {facts_context}")
        print(f"Proceduresss: {procedures}")
        print(f"Procedures: {procedures_context}")
        
        short_term_memory = self.sort_short_term_memory()
        short_term_memory_context = "\n".join([f"Short term memory: {memory['content']}" for memory in short_term_memory])

        return f"Recent interactions: {recent_interactions_context}\nFacts: {facts_context}\nProcedures: {procedures_context}\nRecent memory with current context sorted by importance and timestamp: {short_term_memory_context}".strip()


