# agent/tools/calculator/tool.py
import ast
import operator as op
from typing import Dict, Any
from agent.base_tool import BaseTool
from agent.schemas import TOOL_SCHEMAS, ToolType

# Safe operators mapping for math evaluation
SAFE_OPERATORS = {
    ast.Add: op.add,
    ast.Sub: op.sub,
    ast.Mult: op.mul,
    ast.Div: op.truediv,
    ast.Pow: op.pow,
    ast.USub: op.neg,
    ast.Mod: op.mod,
}

class CalculatorTool(BaseTool):
    """Calculator tool for mathematical expressions."""
    
    def __init__(self):
        super().__init__(TOOL_SCHEMAS[ToolType.CALC])
    
    def _safe_eval(self, node):
        """Safely evaluate arithmetic expressions using AST."""
        if isinstance(node, ast.Num):  # <number>
            return node.n
        elif isinstance(node, ast.BinOp):
            return SAFE_OPERATORS[type(node.op)](self._safe_eval(node.left), self._safe_eval(node.right))
        elif isinstance(node, ast.UnaryOp):
            return SAFE_OPERATORS[type(node.op)](self._safe_eval(node.operand))
        else:
            raise ValueError("Unsupported expression")
    
    def execute(self, args: Dict[str, Any], question: str = "") -> str:
        expr = args["expr"]
        
        # Clean up expression
        e = expr.lower().replace("what is", "").strip()
        
        # Handle percentage calculations
        if "% of" in e:
            left, right = e.split("% of")
            x = float(left.strip())
            y = float(right.strip())
            return str((x / 100.0) * y)

        # Normalize common phrases
        e = e.replace("add ", "").replace("plus ", "+").replace(" to the ", " + ")

        # Parse safely using AST
        node = ast.parse(e, mode='eval').body
        return str(self._safe_eval(node))