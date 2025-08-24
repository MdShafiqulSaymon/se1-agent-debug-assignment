# agent/agent.py (Refactored)
import google.generativeai as genai
from google.generativeai.types import Tool
from google.protobuf.json_format import MessageToDict

from agent.tool_manager import ToolManager


class Agent:
    def __init__(self, api_key: str):
        """Initialize the agent with Gemini API key and tool manager."""
        genai.configure(api_key=api_key)
        self.tool_manager = ToolManager()
        
        # Initialize model with tools from tool manager
        self.model = genai.GenerativeModel(
            model_name="gemini-1.5-flash",
            tools=[Tool(function_declarations=self.tool_manager.get_tool_schemas_for_gemini())]
        )

    def _parse_args(self, raw_args):
        """Safely parse function call arguments."""
        try:
            if hasattr(raw_args, 'fields'):
                return MessageToDict(raw_args)
            return dict(raw_args)
        except Exception as e:
            print(f"DEBUG: Error parsing function_call.args: {str(e)}")
            return {}

    def _handle_tool_call(self, tool_name: str, args: dict, question: str) -> str:
        """Handle execution of a tool call."""
        print(f"DEBUG: Tool called: {tool_name}, Args: {args}")
        
        # Pass user question to tool for context-aware responses
        result = self.tool_manager.execute_tool(tool_name, args, question)
        
        if not result.success:
            return result.error
        
        return str(result.data)

    def answer(self, question: str) -> str:
        """Generate an answer for the given question, using tools if needed."""
        try:
            response = self.model.generate_content(question)

            if response.candidates and response.candidates[0].content.parts:
                for part in response.candidates[0].content.parts:
                    if getattr(part, "function_call", None):
                        tool_name = part.function_call.name
                        args = self._parse_args(part.function_call.args)
                        return self._handle_tool_call(tool_name, args, question)

            return getattr(response, "text", None) or "Sorry, I couldn't process that request."
        except Exception as e:
            return f"Error: {str(e)}"

    def list_available_tools(self) -> str:
        """List all available tools."""
        tools = self.tool_manager.list_tools()
        tool_list = []
        for name, description in tools.items():
            tool_list.append(f"- {name}: {description}")
        return "Available tools:\n" + "\n".join(tool_list)