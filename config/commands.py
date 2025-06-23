# Single source of truth for command formats
# This file defines all command formats that both agent.py and prompts can reference
# 
# IMPORTANT: When modifying these commands, ensure:
# 1. Update both the command arrays AND the format descriptions
# 2. Run tests/test_consistency.py to verify consistency
# 3. Update any examples that reference these commands

FACT_KEY_COMMAND = [
    "remember that", 
    "remember this", 
    "remember this fact", 
    "remember this knowledge", 
    "remember this information", 
    "remember this detail"
]

PROCEDURE_KEY_COMMAND = [
    "remember the procedure",
    "remember the steps for", 
    "remember the steps"
]

# Format templates for prompts
FACT_FORMAT_EXAMPLES = [
    "Remember that Python is a programming language",
    "Remember this fact: The user's name is John",
    "Remember this knowledge: Machine learning uses algorithms"
]

PROCEDURE_FORMAT_EXAMPLES = [
    "Remember the procedure making coffee: boil water, add coffee grounds, stir, wait 5 minutes",
    "Remember the steps for greeting: say hello, ask how they are, wait for response",
    "Remember the steps troubleshooting: identify problem, check common causes, test solution"
]

# Format descriptions for prompts
FACT_FORMAT_DESCRIPTION = """
To teach me a new fact, use one of these formats:
- "Remember that [fact]"
- "Remember this [fact]"
- "Remember this fact [fact]"
- "Remember this knowledge [fact]"
- "Remember this information [fact]"
- "Remember this detail [fact]"
"""

PROCEDURE_FORMAT_DESCRIPTION = """
To teach me a new procedure, use one of these formats:
- "Remember the procedure [procedure_name]: [step1], [step2], [step3]"
- "Remember the steps for [procedure_name]: [step1], [step2], [step3]"
- "Remember the steps [procedure_name]: [step1], [step2], [step3]"
""" 