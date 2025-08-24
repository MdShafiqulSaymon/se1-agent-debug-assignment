# tests/test_integration.py
import pytest
import os
from agent.llm import LLM
from agent.interactive_agent import InteractiveAgent

class TestRealSystem:
    def setup_method(self):
        """Check if API key is available."""
        self.api_key = os.getenv("GEMINI_API_KEY")
        if not self.api_key:
            pytest.skip("GEMINI_API_KEY not set - skipping integration tests")

    def test_calculator_tool_real(self):
        """Test calculator with real Gemini API."""
        llm = LLM(provider="gemini")
        response = llm.answer("What is 15 + 25?")
        
        # Should contain the answer 40
        assert "40" in response

    def test_unit_converter_real(self):
        """Test unit converter with real system."""
        llm = LLM(provider="gemini")
        response = llm.answer("Convert 100 celsius to fahrenheit")
        
        # Should contain the converted value
        assert "212" in response or "fahrenheit" in response.lower()

    def test_text_analyzer_real(self):
        """Test text analyzer with real system."""
        llm = LLM(provider="gemini")
        response = llm.answer("Analyze this text: 'Hello world test'")
        
        # Should contain word count information
        assert any(word in response.lower() for word in ["word", "count", "3"])

class TestInteractiveAgent:
    def setup_method(self):
        """Setup interactive agent if API key available."""
        self.api_key = os.getenv("GEMINI_API_KEY")
        if not self.api_key:
            pytest.skip("GEMINI_API_KEY not set - skipping interactive tests")
        
        self.agent = InteractiveAgent(self.api_key)

    def test_simple_conversation(self):
        """Test basic conversation with memory."""
        response = self.agent.ask("My name is Saymon")
        assert response  # Should get some response
        
        # Ask about the name - should remember from context
        response2 = self.agent.ask("What's my name?")
        # The agent should remember the name from conversation history
        assert response2

    def test_tool_usage_in_conversation(self):
        """Test tool usage within conversation."""
        response = self.agent.ask("Calculate 10 + 5")
        
        # Should use calculator tool and return result
        assert "15" in response