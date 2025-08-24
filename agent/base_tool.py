# agent/base_tool.py
from abc import ABC, abstractmethod
from typing import Dict, Any, Union
from agent.schemas import ToolSchema, ToolType

class ToolResult:
    """Represents the result of a tool execution."""
    def __init__(self, success: bool, data: Any = None, error: str = None):
        self.success = success
        self.data = data
        self.error = error
    
    def __str__(self):
        if self.success:
            return str(self.data)
        return f"Error: {self.error}"

class BaseTool(ABC):
    """Base class for all tools."""
    
    def __init__(self, schema: ToolSchema):
        self.schema = schema
        self.name = schema.name
        self.tool_type = schema.tool_type
    
    def validate_and_execute(self, args: Dict[str, Any], question: str = "") -> ToolResult:
        """Validate arguments and execute the tool."""
        # Validate arguments
        valid, error = self.schema.validate_args(args)
        if not valid:
            return ToolResult(success=False, error=error)
        
        try:
            result = self.execute(args, question)
            return ToolResult(success=True, data=result)
        except Exception as e:
            return ToolResult(success=False, error=str(e))
    
    @abstractmethod
    def execute(self, args: Dict[str, Any], question: str = "") -> Any:
        """Execute the tool with validated arguments and question context."""
        pass