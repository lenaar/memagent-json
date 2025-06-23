import sys
import os
import shutil
sys.path.append(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

from utils.agent import Agent
from prompts.facts import init_assistant_facts

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
    
    # Verify fact was added to memory (accounting for initial facts)
    expected_length = len(init_assistant_facts) + 1
    assert len(agent.memory.facts) == expected_length
    assert agent.memory.facts[-1]["fact"] == "Python is a programming language"
    
    # Clean up
    shutil.rmtree(test_dir)

def test_learn_fact_error():
    # Create a test directory
    test_dir = "test_agent_fact_error"
    if os.path.exists(test_dir):
        shutil.rmtree(test_dir)
    os.makedirs(test_dir)

    # Initialize agent with test memory location
    agent = Agent(api_key="test_key", memory_location=test_dir)

    # Test learning a fact with invalid format (empty fact)
    test_message = "remember that"
    key_command = "remember that"
    
    agent.learn_fact(test_message, key_command)
    
    # Should not add empty fact due to the if fact: check
    # Should only have the initial facts
    assert len(agent.memory.facts) == len(init_assistant_facts)
    
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
    
    # Test the format of steps - should be numbered
    steps = agent.memory.procedures[expected_procedure_name]["steps"]
    assert steps[0] == "1. boil water"
    assert steps[1] == "2. add coffee"
    assert steps[2] == "3. stir"
    
    # Clean up
    shutil.rmtree(test_dir)

def test_learn_procedure_error():
    # Create a test directory
    test_dir = "test_agent_procedure_error"
    if os.path.exists(test_dir):
        shutil.rmtree(test_dir)
    os.makedirs(test_dir)

    # Initialize agent with test memory location
    agent = Agent(api_key="test_key", memory_location=test_dir)

    # Test learning a procedure with invalid format (no colon)
    test_message = "remember the steps for making coffee"
    key_command = "remember the steps for"
    
    # This should handle the error gracefully and not add a procedure
    agent.learn_procedure(test_message, key_command)
    
    # No procedure should be added due to the error
    assert len(agent.memory.procedures) == 0
    
    # Clean up
    shutil.rmtree(test_dir)

if __name__ == "__main__":
    test_learn_fact()
    test_learn_fact_error()
    test_learn_procedure()
    test_learn_procedure_error()
