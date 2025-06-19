from memory import Memory
import os
import shutil

def test_agent_memory():
    # Create a test directory
    test_dir = "test_memory"
    if os.path.exists(test_dir):
        shutil.rmtree(test_dir)
    os.makedirs(test_dir)

    # Initialize memory
    memory = Memory(test_dir)

    # Test adding and retrieving facts
    memory.add_fact("The user's name is John", "fact")
    memory.add_fact("John likes programming", "fact")
    memory.add_fact("John's favorite language is Python", "fact")
    
    # Test adding and retrieving procedures
    memory.add_procedure("greeting", ["Say hello to the user"], "Say hello to the user")
    memory.add_procedure("farewell", ["Say goodbye to the user"], "Say goodbye to the user")
    
    # Test adding and retrieving interactions
    memory.add_interaction("Hello, how are you?", "I'm doing well, thank you!", {"mood": "sunny"})
    memory.add_interaction("What's your name?", "I'm an AI assistant", {"name": "sunny"})
    
    assert memory.facts == [
        {"fact": "The user's name is John", "type": "fact", "timestamp": memory.facts[0]["timestamp"]},
        {"fact": "John likes programming", "type": "fact", "timestamp": memory.facts[1]["timestamp"]},  
        {"fact": "John's favorite language is Python", "type": "fact", "timestamp": memory.facts[2]["timestamp"]}
    ]
    
    assert memory.procedures == {"greeting": {"description": "Say hello to the user", "name": "greeting", "steps": ["Say hello to the user"], "timestamp": memory.procedures["greeting"]["timestamp"]}, "farewell": {"description": "Say goodbye to the user", "name": "farewell", "steps": ["Say goodbye to the user"], "timestamp": memory.procedures["farewell"]["timestamp"]}}

    assert memory.interactions == [
        {"agent_message": "I'm doing well, thank you!", "user_message": "Hello, how are you?", "metadata": {"mood": "sunny"}, "timestamp": memory.interactions[0]["timestamp"]},
        {"agent_message": "I'm an AI assistant", "user_message": "What's your name?", "metadata": {"name": "sunny"}, "timestamp": memory.interactions[1]["timestamp"]}
    ]


    # Clean up
    shutil.rmtree(test_dir)

def test_search_facts():
    # Create a test directory
    test_dir = "test_memory_search"
    if os.path.exists(test_dir):
        shutil.rmtree(test_dir)
    os.makedirs(test_dir)

    # Initialize memory
    memory = Memory(test_dir)

    # Add test facts
    memory.add_fact("The user's name is John", "fact")
    memory.add_fact("John likes programming", "fact")
    memory.add_fact("Python is a programming language", "fact")

    # Test search
    results = memory.search_facts("programming")
    assert len(results) == 2
    assert any("John likes programming" in result["fact"] for result in results)
    assert any("Python is a programming language" in result["fact"] for result in results)

    # Clean up
    shutil.rmtree(test_dir)

def test_search_procedures():
    # Create a test directory
    test_dir = "test_memory_search"
    if os.path.exists(test_dir):
        shutil.rmtree(test_dir)
    os.makedirs(test_dir)

    # Initialize memory
    memory = Memory(test_dir)

    # Add test procedures
    memory.add_procedure("greeting", ["Say hello"], "Say hello to the user")
    memory.add_procedure("farewell", ["Say goodbye"], "Say goodbye to the user")

    # Test search
    results = memory.search_procedures("hello")
    assert len(results) == 1
    assert results[0]["name"] == "greeting"

    # Clean up
    shutil.rmtree(test_dir)

def test_search_interactions():
    # Create a test directory
    test_dir = "test_memory_search"
    if os.path.exists(test_dir):
        shutil.rmtree(test_dir)
    os.makedirs(test_dir)

    # Initialize memory
    memory = Memory(test_dir)

    # Add test interactions
    memory.add_interaction("Hello, how are you?", "I'm doing well, thank you!")
    memory.add_interaction("What's your name?", "I'm an AI assistant")

    # Test search
    results = memory.search_interactions("hello")
    assert len(results) == 1
    assert "Hello, how are you?" in results[0]["user_message"]

    # Clean up
    shutil.rmtree(test_dir)

if __name__ == "__main__":
    test_agent_memory()
    test_search_facts()
    test_search_procedures()
    test_search_interactions() 