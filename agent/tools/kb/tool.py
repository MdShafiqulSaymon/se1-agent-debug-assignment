# agent/tools/kb/tool.py
import json
import re
import os
from typing import Dict, Any
from agent.base_tool import BaseTool
from agent.schemas import TOOL_SCHEMAS, ToolType
from .kb_agent import KBAgent

class KnowledgeBaseTool(BaseTool):
    """Knowledge base lookup tool with smart AI search."""
    
    def __init__(self):
        super().__init__(TOOL_SCHEMAS[ToolType.KB])
        # Initialize KB agent
        api_key = os.getenv("GEMINI_API_KEY")
        self.kb_agent = KBAgent(api_key) if api_key else None
    
    def execute(self, args: Dict[str, Any], question: str = "") -> str:
        query = args["q"]
        
        # First try simple keyword search (original method)
        simple_result = self._simple_search(query)
        if simple_result != "No entry found.":
            return simple_result
        
        # If simple search fails, use KB agent for smart search
        if self.kb_agent:
            return self.kb_agent.search(question or query)
        
        return "No entry found."
    
    def _simple_search(self, query: str) -> str:
        """Original simple keyword search method."""
        try:
            cleaned_query = re.sub(r'^(who is|what is)\s+', '', query.lower(), flags=re.IGNORECASE).strip()
            cleaned_query = re.sub(r'[^\w\s]', '', cleaned_query)
            
            with open("data/kb.json", "r") as f:
                data = json.load(f)
            
            for item in data.get("entries", []):
                if cleaned_query in item.get("name", "").lower():
                    return item.get("summary", "")
            
            return "No entry found."
        except Exception:
            return "No entry found."