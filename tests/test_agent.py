import sys
import os
import shutil
from prompts.facts import init_assistant_facts
sys.path.append(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

from utils.agent import Agent

def test_learn_fact():
    # Create a test directory
    test_dir = "test_agent_fact"
    if os.path.exists(test_dir):
        shutil.rmtree(test_dir)
    os.makedirs(test_dir)

    # Initialize agent with test memory location
    agent = Agent(api_key="test_key", memory_location=test_dir)

    # Test learning a fact
    test_message = "remember that Python is a programming language"
    key_command = "remember that"
    
    agent.learn_fact(test_message, key_command)
    
    # Verify fact was added to memory and the init facts are still there
    expected_length = len(init_assistant_facts) + 1
    assert len(agent.memory.facts) == expected_length
    assert agent.memory.facts[-1]["fact"] == "Python is a programming language"
    
    # Clean up
    shutil.rmtree(test_dir)

def test_learn_procedure():
    # Create a test directory
    test_dir = "test_agent_procedure"
    if os.path.exists(test_dir):
        shutil.rmtree(test_dir)
    os.makedirs(test_dir)

    # Initialize agent with test memory location
    agent = Agent(api_key="test_key", memory_location=test_dir)

    # Test learning a procedure
    test_message = "remember the steps for making coffee: boil water, add coffee, stir"
    key_command = "remember the steps for"
    
    agent.learn_procedure(test_message, key_command)
    
    # Verify procedure was added to memory
    assert len(agent.memory.procedures) == 1
    expected_procedure_name = "making coffee"
    assert expected_procedure_name in agent.memory.procedures
    assert agent.memory.procedures[expected_procedure_name]["name"] == expected_procedure_name
    assert len(agent.memory.procedures[expected_procedure_name]["steps"]) == 3
    assert agent.memory.procedures[expected_procedure_name]["steps"][0] == "1. boil water"
    assert agent.memory.procedures[expected_procedure_name]["steps"][1] == "2. add coffee"
    assert agent.memory.procedures[expected_procedure_name]["steps"][2] == "3. stir"
    
    # Clean up
    shutil.rmtree(test_dir)

if __name__ == "__main__":
    test_learn_fact()
    test_learn_procedure()
