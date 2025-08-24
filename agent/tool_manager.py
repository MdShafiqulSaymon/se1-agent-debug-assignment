# agent/tool_manager.py (Updated)
from typing import Dict, Optional
from agent.base_tool import BaseTool, ToolResult
from agent.tools import discover_tools

class ToolManager:
    """Manages all available tools and their execution."""
    
    def __init__(self):
        self.tools: Dict[str, BaseTool] = {}
        self._register_discovered_tools()
    
    def _register_discovered_tools(self):
        """Auto-register all discovered tools."""
        tool_classes = discover_tools()
        
        for tool_class in tool_classes:
            try:
                tool_instance = tool_class()
                self.register_tool(tool_instance)
                print(f"✅ Registered tool: {tool_instance.name}")
            except Exception as e:
                print(f"❌ Failed to register {tool_class.__name__}: {e}")
    
    def register_tool(self, tool: BaseTool):
        """Register a new tool."""
        self.tools[tool.name] = tool
    
    def get_tool(self, name: str) -> Optional[BaseTool]:
        """Get a tool by name."""
        return self.tools.get(name)
    
    def execute_tool(self, name: str, args: Dict, question: str = "") -> ToolResult:
        """Execute a tool with the given arguments and question context."""
        tool = self.get_tool(name)
        if not tool:
            return ToolResult(success=False, error=f"Unknown tool: {name}")
        
        return tool.validate_and_execute(args, question)
    
    def list_tools(self) -> Dict[str, str]:
        """List all available tools and their descriptions."""
        return {name: tool.schema.description for name, tool in self.tools.items()}
    
    def get_tool_schemas_for_gemini(self):
        """Get tool schemas formatted for Gemini function declarations."""
        from google.generativeai.types import FunctionDeclaration
        
        declarations = []
        for tool in self.tools.values():
            schema = tool.schema
            properties = {}
            required = []
            
            for param in schema.parameters:
                properties[param.name] = {
                    "type": param.param_type,
                    "description": param.description
                }
                if param.required:
                    required.append(param.name)
            
            declarations.append(FunctionDeclaration(
                name=schema.name,
                description=schema.description,
                parameters={
                    "type": "object",
                    "properties": properties,
                    "required": required
                }
            ))
        
        return declarations