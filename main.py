#!/usr/bin/env python3
"""
MemAgent Simple Chat - Command Line Interface
A simple chat interface for an AI agent that remembers everything.
"""

import os
import sys
from dotenv import load_dotenv

# Load environment variables
load_dotenv()

# Import our agent
from agent import Agent

def main():
    """Simple chat interface for MemAgent."""
    
    print("🧠 MemAgent Simple Chat")
    print("=" * 40)
    print("Chat with an AI that remembers everything!")
    print("Type 'exit' to quit.")
    print("-" * 40)
    
    # Initialize the agent
    try:
        print("🚀 Initializing agent...")
        agent = Agent()
        print("✅ Agent ready! Start chatting below.")
        print()
    except Exception as e:
        print(f"❌ Error initializing agent: {e}")
        print("💡 Make sure you have set your OPENAI_API_KEY environment variable.")
        sys.exit(1)
    
    # Simple conversation loop
    while True:
        try:
            user_input = input("👤 You: ")
            
            if user_input.lower() in ["exit", "quit", "bye"]:
                print("👋 Goodbye! Your agent will remember everything you taught it.")
                break
            
            if not user_input.strip():
                continue
            
            print("🤔 Thinking...")
            response = agent.process_message(user_input)
            
            if response:
                print(f"🤖 Assistant: {response}")
            else:
                print("❌ No response received.")
                
        except KeyboardInterrupt:
            print("\n👋 Goodbye!")
            break
        except Exception as e:
            print(f"❌ Error: {e}")


if __name__ == "__main__":
    main()