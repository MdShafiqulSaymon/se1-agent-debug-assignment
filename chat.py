# chat.py - Interactive chat with memory
import os
from dotenv import load_dotenv
from agent.interactive_agent import InteractiveAgent

load_dotenv()

def main():
    print("🤖 Interactive Agent Chat (with memory)")
    print("Type 'quit', 'exit', or 'bye' to stop")
    print("Type 'history' to see conversation history")
    print("-" * 50)
    
    # Initialize agent
    api_key = os.getenv("GEMINI_API_KEY")
    if not api_key:
        print("Error: GEMINI_API_KEY not set in .env file")
        return
    
    agent = InteractiveAgent(api_key)
    # Add this to chat.py after creating agent
    print("Available tools:", agent.tool_manager.list_tools())
    while True:
        try:
            # Get user input
            question = input("\n👤 You: ").strip()
            
            # Check for exit commands
            if question.lower() in ['quit', 'exit', 'bye', 'q']:
                print("👋 Goodbye!")
                break
            
            # Show history command
            if question.lower() == 'history':
                agent.show_history()
                continue
            
            # Skip empty input
            if not question:
                continue
            
            # Get response
            print("🤖 Assistant: ", end="", flush=True)
            response = agent.ask(question)
            print(response)
            
        except KeyboardInterrupt:
            print("\n👋 Goodbye!")
            break
        except Exception as e:
            print(f"Error: {e}")

if __name__ == "__main__":
    main()