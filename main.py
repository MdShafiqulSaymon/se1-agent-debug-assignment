# main.py
import sys
from agent.llm import LLM

def main():
    if len(sys.argv) < 2:
        print("Usage: python main.py \"your question here\"")
        sys.exit(1)

    question = " ".join(sys.argv[1:])

    # Initialize with Gemini
    llm = LLM(provider="gemini")
    response = llm.answer(question)
    print(response)

if __name__ == "__main__":
    main()