# agent/tools/text_analyzer/tool.py
from typing import Dict, Any
from agent.base_tool import BaseTool
from agent.schemas import TOOL_SCHEMAS, ToolType

class TextAnalyzerTool(BaseTool):
    """Text analyzer for basic text statistics and sentiment analysis."""
    
    def __init__(self):
        super().__init__(TOOL_SCHEMAS[ToolType.TEXT_ANALYZER])
    
    def execute(self, args: Dict[str, Any], question: str = "") -> Dict[str, Any]:
        text = args["text"]
        analysis_type = args.get("analysis_type", "basic")
        
        # Basic analysis
        word_count = len(text.split())
        char_count = len(text)
        char_count_no_spaces = len(text.replace(" ", ""))
        sentence_count = len([s for s in text.split('.') if s.strip()])
        
        result = {
            "word_count": word_count,
            "character_count": char_count,
            "character_count_no_spaces": char_count_no_spaces,
            "sentence_count": sentence_count,
            "analysis_type": analysis_type
        }
        
        # Simple sentiment analysis if requested
        if analysis_type == "sentiment":
            positive_words = ["good", "great", "excellent", "amazing", "wonderful", "fantastic", "love", "like", "happy", "joy"]
            negative_words = ["bad", "terrible", "awful", "horrible", "hate", "dislike", "sad", "angry", "disappointed"]
            
            text_lower = text.lower()
            positive_count = sum(1 for word in positive_words if word in text_lower)
            negative_count = sum(1 for word in negative_words if word in text_lower)
            
            if positive_count > negative_count:
                sentiment = "positive"
            elif negative_count > positive_count:
                sentiment = "negative"
            else:
                sentiment = "neutral"
            
            result.update({
                "sentiment": sentiment,
                "positive_words_found": positive_count,
                "negative_words_found": negative_count
            })
        
        return result