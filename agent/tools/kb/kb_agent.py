# agent/tools/kb/kb_agent.py
import json
import google.generativeai as genai

class KBAgent:
    def __init__(self, api_key: str, kb_file_path: str = "data/kb.json"):
        """Simple KB agent for intelligent searching."""
        genai.configure(api_key=api_key)
        self.model = genai.GenerativeModel(model_name="gemini-1.5-flash")
        self.kb_file_path = kb_file_path
        self.kb_data = self._load_kb()
    
    def _load_kb(self):
        """Load knowledge base data."""
        try:
            with open(self.kb_file_path, "r") as f:
                return json.load(f)
        except Exception:
            return {"entries": []}
    
    def search(self, user_question: str) -> str:
        """Smart search in KB using AI agent."""
        try:
            # Get all KB entries as text
            kb_entries = []
            for i, entry in enumerate(self.kb_data.get("entries", [])):
                kb_entries.append(f"{i}: {entry.get('name', '')} - {entry.get('summary', '')}")
            
            if not kb_entries:
                return "Knowledge base is empty."
            
            # Create prompt for the agent
            prompt = f"""
You are a knowledge base search assistant. 

User question: "{user_question}"

Available knowledge base entries:
{chr(10).join(kb_entries)}

Task: Find the most relevant entry index number that could answer the user's question.

Rules:
1. If you find a relevant entry, respond with just the index number (0, 1, 2, etc.)
2. If no entry is relevant to the question, respond with "NO_MATCH"
3. Look for partial matches, similar names, or related concepts
4. Be flexible with name variations (e.g., "Simon" could match "Saymon")

Response format: Just the index number or "NO_MATCH"
"""
            
            # Ask the agent
            response = self.model.generate_content(prompt)
            result = response.text.strip()
            
            # Handle the response
            if result == "NO_MATCH":
                return "No entry found."
            
            # Try to get the entry by index
            try:
                index = int(result)
                if 0 <= index < len(self.kb_data["entries"]):
                    return self.kb_data["entries"][index].get("summary", "No summary available.")
                else:
                    return "No entry found."
            except ValueError:
                return "No entry found."
                
        except Exception as e:
            return f"KB search error: {str(e)}"