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

def test_sort_short_term_memory():
    # Create a test directory
    test_dir = "test_memory_sort"
    if os.path.exists(test_dir):
        shutil.rmtree(test_dir)
    os.makedirs(test_dir)

    # Initialize memory
    memory = Memory(test_dir)

    # Add test short term memories with different importance and timestamps
    memory.add_to_short_term_memory("Low importance memory", importance=0.3)
    memory.add_to_short_term_memory("High importance memory", importance=0.9)
    memory.add_to_short_term_memory("Medium importance memory", importance=0.6)

    # Test sorting
    sorted_memory = memory.sort_short_term_memory()
    
    # Should be sorted by importance (descending)
    assert len(sorted_memory) == 3
    assert sorted_memory[0]["content"] == "High importance memory"
    assert sorted_memory[1]["content"] == "Medium importance memory"
    assert sorted_memory[2]["content"] == "Low importance memory"
    
    # Check that importance values are correct
    assert sorted_memory[0]["importance"] == 0.9
    assert sorted_memory[1]["importance"] == 0.6
    assert sorted_memory[2]["importance"] == 0.3

    # Clean up
    shutil.rmtree(test_dir)

def test_empty_search_results():
    # Create a test directory
    test_dir = "test_memory_empty"
    if os.path.exists(test_dir):
        shutil.rmtree(test_dir)
    os.makedirs(test_dir)

    # Initialize memory
    memory = Memory(test_dir)

    # Test empty search results
    facts_results = memory.search_facts("nonexistent")
    procedures_results = memory.search_procedures("nonexistent")
    interactions_results = memory.search_interactions("nonexistent")

    assert facts_results == []
    assert procedures_results == []
    assert interactions_results == []

    # Clean up
    shutil.rmtree(test_dir)

def test_search_with_empty_query():
    # Create a test directory
    test_dir = "test_memory_empty_query"
    if os.path.exists(test_dir):
        shutil.rmtree(test_dir)
    os.makedirs(test_dir)

    # Initialize memory
    memory = Memory(test_dir)

    # Add some data
    memory.add_fact("Test fact", "fact")
    memory.add_procedure("test_proc", ["step1"], "Test procedure")
    memory.add_interaction("Hello", "Hi")

    # Test empty query
    facts_results = memory.search_facts("")
    procedures_results = memory.search_procedures("")
    interactions_results = memory.search_interactions("")

    assert facts_results == []
    assert procedures_results == []
    assert interactions_results == []

    # Test whitespace-only query
    facts_results = memory.search_facts("   ")
    procedures_results = memory.search_procedures("   ")
    interactions_results = memory.search_interactions("   ")

    assert facts_results == []
    assert procedures_results == []
    assert interactions_results == []

    # Clean up
    shutil.rmtree(test_dir)

def test_search_limit():
    # Create a test directory
    test_dir = "test_memory_limit"
    if os.path.exists(test_dir):
        shutil.rmtree(test_dir)
    os.makedirs(test_dir)

    # Initialize memory
    memory = Memory(test_dir)

    # Add multiple facts
    memory.add_fact("First fact about programming", "fact")
    memory.add_fact("Second fact about programming", "fact")
    memory.add_fact("Third fact about programming", "fact")
    memory.add_fact("Fourth fact about programming", "fact")

    # Test with limit=2
    results = memory.search_facts("programming", limit=2)
    assert len(results) == 2

    # Test with limit=1
    results = memory.search_facts("programming", limit=1)
    assert len(results) == 1

    # Clean up
    shutil.rmtree(test_dir)

def test_recent_interactions():
    # Create a test directory
    test_dir = "test_memory_recent"
    if os.path.exists(test_dir):
        shutil.rmtree(test_dir)
    os.makedirs(test_dir)

    # Initialize memory
    memory = Memory(test_dir)

    # Add multiple interactions
    memory.add_interaction("First message", "First response")
    memory.add_interaction("Second message", "Second response")
    memory.add_interaction("Third message", "Third response")
    memory.add_interaction("Fourth message", "Fourth response")

    # Test recent interactions with limit=2
    recent = memory.search_recent_interactions(limit=2)
    assert len(recent) == 2
    assert recent[-2]["user_message"] == "Third message"  # Most recent first
    assert recent[-1]["user_message"] == "Fourth message"


    # Test with default limit
    recent = memory.search_recent_interactions()
    assert len(recent) == 3  # Default limit

    # Clean up
    shutil.rmtree(test_dir)

def test_short_term_memory_persistence():
    # Create a test directory
    test_dir = "test_memory_persistence"
    if os.path.exists(test_dir):
        shutil.rmtree(test_dir)
    os.makedirs(test_dir)

    # Initialize memory
    memory = Memory(test_dir)

    # Add short term memory
    memory.add_to_short_term_memory("Important memory", importance=0.8)
    memory.add_to_short_term_memory("Less important memory", importance=0.3)

    # Check that memory was added
    assert len(memory.short_term_memory) == 2
    assert memory.short_term_memory[0]["content"] == "Important memory"
    assert memory.short_term_memory[0]["importance"] == 0.8

    # Clean up
    shutil.rmtree(test_dir)

def test_case_insensitive_search():
    # Create a test directory
    test_dir = "test_memory_case"
    if os.path.exists(test_dir):
        shutil.rmtree(test_dir)
    os.makedirs(test_dir)

    # Initialize memory
    memory = Memory(test_dir)

    # Add data with mixed case
    memory.add_fact("Python is a Programming language", "fact")
    memory.add_procedure("GREETING", ["Say HELLO"], "Say HELLO to the user")
    memory.add_interaction("HELLO there", "Hi THERE!")

    # Test case insensitive search
    facts_results = memory.search_facts("programming")
    procedures_results = memory.search_procedures("hello")
    interactions_results = memory.search_interactions("hello")

    assert len(facts_results) == 1
    assert len(procedures_results) == 1
    assert len(interactions_results) == 1

    # Clean up
    shutil.rmtree(test_dir)

def test_get_context():
    # Create a test directory
    test_dir = "test_memory_context"
    if os.path.exists(test_dir):
        shutil.rmtree(test_dir)
    os.makedirs(test_dir)

    # Initialize memory
    memory = Memory(test_dir)

    # Add test data
    memory.add_fact("User likes programming", "fact")
    memory.add_procedure("User greeting before programming", ["Say hello", "Ask how they are"], "Greet the user")
    memory.add_interaction("Hello", "Hi there!", {"mood": "friendly"})
    memory.add_to_short_term_memory("User is in a hurry", importance=0.8)

    # Test get_context
    context = memory.get_context("programming", limit=2)
    
    # Check that context contains expected sections
    assert "Recent interactions:" in context
    assert "Facts:" in context
    assert "Procedures:" in context
    assert "Recent memory with current context sorted by importance and timestamp:" in context
    
    # Check that specific content is included
    assert "User likes programming" in context
    assert "greeting" in context
    assert "User is in a hurry" in context
    
    # Check that context is properly formatted (no leading/trailing whitespace)
    assert context == context.strip()

    # Clean up
    shutil.rmtree(test_dir)

if __name__ == "__main__":
    test_agent_memory()
    test_search_facts()
    test_search_procedures()
    test_search_interactions()
    test_sort_short_term_memory()
    test_empty_search_results()
    test_search_with_empty_query()
    test_search_limit()
    test_recent_interactions()
    test_short_term_memory_persistence()
    test_case_insensitive_search()
    test_get_context() 