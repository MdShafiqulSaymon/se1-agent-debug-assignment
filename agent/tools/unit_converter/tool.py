# agent/tools/unit_converter/tool.py
from typing import Dict, Any
from agent.base_tool import BaseTool
from agent.schemas import TOOL_SCHEMAS, ToolType

class UnitConverterTool(BaseTool):
    """Unit conversion tool."""
    
    def __init__(self):
        super().__init__(TOOL_SCHEMAS[ToolType.UNIT_CONVERTER])
    
    def execute(self, args: Dict[str, Any], question: str = "") -> str:
        celsius = float(args["celsius"])
        fahrenheit = (celsius * 9 / 5) + 32
        return f"{celsius}°C = {fahrenheit}°F"