# tests/test_real_tools.py
import pytest
import os
import json
from agent.tools.calculator.tool import CalculatorTool
from agent.tools.text_analyzer.tool import TextAnalyzerTool
from agent.tools.unit_converter.tool import UnitConverterTool

class TestRealTools:
    """Test the actual tool implementations without mocking."""

    def test_calculator_real_math(self):
        """Test calculator with real calculations."""
        calc = CalculatorTool()
        
        # Test basic arithmetic
        result = calc.execute({"expr": "25 * 4"})
        assert result == "100"
        
        # Test percentage
        result = calc.execute({"expr": "20% of 150"})
        assert result == "30.0"

    def test_text_analyzer_real_analysis(self):
        """Test text analyzer with real text."""
        analyzer = TextAnalyzerTool()
        
        # Test basic analysis
        text = "The quick brown fox jumps over the lazy dog."
        result = analyzer.execute({"text": text})
        
        assert result["word_count"] == 9
        assert result["character_count"] == 44
        assert result["sentence_count"] == 1
        
        # Test sentiment analysis
        positive_text = "I love this amazing day!"
        result = analyzer.execute({
            "text": positive_text, 
            "analysis_type": "sentiment"
        })
        
        assert result["sentiment"] == "positive"
        assert result["positive_words_found"] > 0

    def test_unit_converter_real_conversion(self):
        """Test unit converter with real conversions."""
        converter = UnitConverterTool()
        
        # Test freezing point
        result = converter.execute({"celsius": 0})
        assert "32.0°F" in result
        
        # Test boiling point
        result = converter.execute({"celsius": 100})
        assert "212.0°F" in result

class TestKnowledgeBaseReal:
    """Test KB with real file if it exists."""
    
    def test_kb_with_real_file(self):
        """Test KB if kb.json exists."""
        kb_file = "data/kb.json"
        if not os.path.exists(kb_file):
            pytest.skip(f"KB file {kb_file} not found - create it to test KB functionality")
        
        # Only test if file exists
        with open(kb_file, 'r') as f:
            data = json.load(f)
        
        assert "entries" in data
        assert isinstance(data["entries"], list)