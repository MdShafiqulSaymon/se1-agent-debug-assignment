# agent/interactive_agent.py
import google.generativeai as genai
from google.generativeai.types import Tool
from google.protobuf.json_format import MessageToDict
from agent.tool_manager import ToolManager

class InteractiveAgent:
    def __init__(self, api_key: str):
        """Initialize agent with conversation memory."""
        genai.configure(api_key=api_key)
        self.tool_manager = ToolManager()
        self.chat_history = []  # Store conversation history
        
        # Initialize model with tools
        self.model = genai.GenerativeModel(
            model_name="gemini-1.5-flash",
            tools=[Tool(function_declarations=self.tool_manager.get_tool_schemas_for_gemini())]
        )
        
        # Start chat session
        self.chat = self.model.start_chat(history=[])

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
        print(f"🔧 Using tool: {tool_name}")
        
        result = self.tool_manager.execute_tool(tool_name, args)
        
        if not result.success:
            return result.error
        
        # Special handling for weather tool
        if tool_name == "weather" and result.success:
            try:
                weather_data = result.data
                return f"The temperature in {weather_data['city'].title()} is {weather_data['temp']}°C with {weather_data['description']}."
            except Exception:
                return str(result.data)
        
        # Special handling for unit converter
        if tool_name == "unit_converter":
            celsius = args.get("celsius")
            return f"{celsius}°C = {result.data}°F"
        
        return str(result.data)

    def ask(self, question: str) -> str:
        """Ask a question and get response with memory."""
        try:
            # Send message to chat (maintains history automatically)
            response = self.chat.send_message(question)
            
            # Check if tools were called
            if response.candidates and response.candidates[0].content.parts:
                for part in response.candidates[0].content.parts:
                    if getattr(part, "function_call", None):
                        tool_name = part.function_call.name
                        args = self._parse_args(part.function_call.args)
                        tool_result = self._handle_tool_call(tool_name, args, question)
                        
                        # Send tool result back to continue conversation
                        response = self.chat.send_message(f"Tool result: {tool_result}")
                        return getattr(response, "text", tool_result)
            
            return getattr(response, "text", "Sorry, I couldn't process that request.")
            
        except Exception as e:
            return f"Error: {str(e)}"
    
    def show_history(self):
        """Show conversation history."""
        if not self.chat.history:
            print("No conversation history yet.")
            return
        
        print("\n📜 Conversation History:")
        print("-" * 40)
        for i, message in enumerate(self.chat.history):
            role = "🤖 Assistant" if message.role == "model" else "👤 You"
            content = message.parts[0].text if message.parts else "[No text content]"
            print(f"{role}: {content}")
        print("-" * 40 + "\n")