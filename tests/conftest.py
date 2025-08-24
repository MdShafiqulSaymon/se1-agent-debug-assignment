# tests/conftest.py
import pytest
import os
import sys
from dotenv import load_dotenv

# Add the project root to Python path
sys.path.insert(0, os.path.join(os.path.dirname(__file__), '..'))

# Load environment variables from .env file
load_dotenv()

@pytest.fixture(autouse=True)
def setup_test_env():
    """Setup test environment - preserve real API keys from .env file."""
    # Don't override if real keys exist
    if not os.getenv("GEMINI_API_KEY"):
        os.environ["GEMINI_API_KEY"] = "test_key_123"
    if not os.getenv("WEATHER_API_KEY"):
        os.environ["WEATHER_API_KEY"] = "test_weather_key"
    yield