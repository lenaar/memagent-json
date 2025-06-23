import sys
import os
import shutil
from unittest.mock import patch, MagicMock
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
    agent = Agent(memory_location=test_dir)

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
    agent = Agent(memory_location=test_dir)

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
    agent = Agent(memory_location=test_dir)

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
    agent = Agent(memory_location=test_dir)

    # Test learning a procedure with invalid format (no colon)
    test_message = "remember the steps for making coffee"
    key_command = "remember the steps for"
    
    # This should handle the error gracefully and not add a procedure
    agent.learn_procedure(test_message, key_command)
    
    # No procedure should be added due to the error
    assert len(agent.memory.procedures) == 0
    
    # Clean up
    shutil.rmtree(test_dir)

def test_extract_and_learn_output():
    # Create a test directory
    test_dir = "test_extract_and_learn_output"
    if os.path.exists(test_dir):
        shutil.rmtree(test_dir)
    os.makedirs(test_dir)

    # Initialize agent with test memory location
    agent = Agent(memory_location=test_dir)

    # Test fact command
    result = agent.extract_and_learn("remember that Python is great")
    assert result == "learned fact"
    
    # Test procedure command
    result = agent.extract_and_learn("remember the steps for coffee: boil, add")
    assert result == "learned procedure"
    
    # Test no command
    result = agent.extract_and_learn("What is the weather?")
    assert result == "no key command found"
    
    # Clean up
    shutil.rmtree(test_dir)

def test_process_message_orchestration():
    # Create a test directory
    test_dir = "test_process_message_orchestration"
    if os.path.exists(test_dir):
        shutil.rmtree(test_dir)
    os.makedirs(test_dir)

    # Initialize agent with test memory location
    agent = Agent(memory_location=test_dir)

    # Mock OpenAI API response
    mock_response = MagicMock()
    mock_response.choices[0].message.content = "Test response"
    
    with patch('utils.agent.OpenAI') as mock_openai:
        mock_client = MagicMock()
        mock_client.chat.completions.create.return_value = mock_response
        mock_openai.return_value = mock_client
        
        # Test the orchestration - verify all steps are called in correct order
        test_message = "What's the weather?"
        response = agent.process_message(test_message)
        
        # Verify the response is returned
        assert response == "Test response"
        
        # Verify interaction was stored (this is the key orchestration behavior)
        assert len(agent.memory.interactions) == 1
        assert agent.memory.interactions[0]["user_message"] == test_message
        assert agent.memory.interactions[0]["agent_message"] == response
    
    # Clean up
    shutil.rmtree(test_dir)

def test_process_message_no_interaction_on_api_failure():
    # Create a test directory
    test_dir = "test_process_message_api_failure"
    if os.path.exists(test_dir):
        shutil.rmtree(test_dir)
    os.makedirs(test_dir)

    # Initialize agent with test memory location
    agent = Agent(memory_location=test_dir)

    with patch('utils.agent.OpenAI') as mock_openai:
        mock_client = MagicMock()
        mock_client.chat.completions.create.side_effect = Exception("API Error")
        mock_openai.return_value = mock_client
        
        # Test that no interaction is stored when API fails
        test_message = "What's the weather?"
        response = agent.process_message(test_message)
        
        # Verify the response is None when API fails
        assert response is None
        
        # Verify no interaction was stored (key orchestration behavior)
        assert len(agent.memory.interactions) == 0
    
    # Clean up
    shutil.rmtree(test_dir)

if __name__ == "__main__":
    test_learn_fact()
    test_learn_fact_error()
    test_learn_procedure()
    test_learn_procedure_error()
    test_extract_and_learn_output()
    test_process_message_orchestration()
    test_process_message_no_interaction_on_api_failure()
