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

def get_interaction_content(interaction: Dict[str, Any]) -> str:
    return f"user: {interaction['user_message']} agent: {interaction['agent_message']}"

class Memory:
    # facts: list of facts, knowledge about the world, semantic memory
    # procedures: dict of procedures, smth can be done on autopilot, procedural memory
    # interactions: list of interactions, episodic memory
    # short_term_memory: fast access to latest information, working memory
    
    
    def __init__(self, location: str = "./json_memory"):
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
    