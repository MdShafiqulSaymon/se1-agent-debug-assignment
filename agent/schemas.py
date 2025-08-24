# agent/schemas.py
from typing import Dict, Any, Optional, List
from dataclasses import dataclass
from enum import Enum

class ToolType(Enum):
    CALC = "calc"
    WEATHER = "weather"
    KB = "kb"
    UNIT_CONVERTER = "unit_converter"
    TEXT_ANALYZER = "text_analyzer"  # New tool

@dataclass
class ToolParameter:
    name: str
    param_type: str
    description: str
    required: bool = True
    default: Any = None

@dataclass
class ToolSchema:
    name: str
    tool_type: ToolType
    description: str
    parameters: List[ToolParameter]
    
    def validate_args(self, args: Dict[str, Any]) -> tuple[bool, Optional[str]]:
        """Validate arguments against schema."""
        for param in self.parameters:
            if param.required and param.name not in args:
                return False, f"Missing required parameter: {param.name}"
            
            if param.name in args:
                value = args[param.name]
                if param.param_type == "string" and not isinstance(value, str):
                    return False, f"Parameter {param.name} must be a string"
                elif param.param_type == "number" and not isinstance(value, (int, float)):
                    return False, f"Parameter {param.name} must be a number"
        
        return True, None

# Tool schema definitions
TOOL_SCHEMAS = {
    ToolType.CALC: ToolSchema(
        name="calc",
        tool_type=ToolType.CALC,
        description="Evaluate a mathematical expression",
        parameters=[
            ToolParameter("expr", "string", "Mathematical expression to evaluate")
        ]
    ),
    ToolType.WEATHER: ToolSchema(
        name="weather",
        tool_type=ToolType.WEATHER,
        description="Get weather information for a city",
        parameters=[
            ToolParameter("city", "string", "City name")
        ]
    ),
    ToolType.KB: ToolSchema(
        name="kb",
        tool_type=ToolType.KB,
        description="Look up information in knowledge base",
        parameters=[
            ToolParameter("q", "string", "Query string")
        ]
    ),
    ToolType.UNIT_CONVERTER: ToolSchema(
        name="unit_converter",
        tool_type=ToolType.UNIT_CONVERTER,
        description="Convert Celsius to Fahrenheit",
        parameters=[
            ToolParameter("celsius", "number", "Temperature in Celsius")
        ]
    ),
    ToolType.TEXT_ANALYZER: ToolSchema(
        name="text_analyzer",
        tool_type=ToolType.TEXT_ANALYZER,
        description="Analyze text for word count, character count, and sentiment",
        parameters=[
            ToolParameter("text", "string", "Text to analyze"),
            ToolParameter("analysis_type", "string", "Type of analysis: 'basic' or 'sentiment'", False, "basic")
        ]
    )
}