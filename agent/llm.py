# agent/llm.py
import os
from dotenv import load_dotenv
from agent.agent import Agent

load_dotenv()

class LLM:
    def __init__(self, provider: str = "gemini"):
        """Initialize LLM handler. Currently supports only Gemini."""
        self.provider = provider.lower()
        self.api_key = None
        self.agent = None

        if self.provider == "gemini":
            self.api_key = os.getenv("GEMINI_API_KEY")
            if not self.api_key:
                raise ValueError("Error: GEMINI_API_KEY not set in .env file")
            self.agent = Agent(api_key=self.api_key)
        else:
            raise ValueError(f"Unsupported LLM provider: {self.provider}")

    def answer(self, question: str) -> str:
        """Route the question to the respective provider/agent."""
        if not self.agent:
            return "Error: No LLM agent initialized"
        return self.agent.answer(question)
