# agent/tools/__init__.py
"""
Auto-discovery system for tools.
This module automatically imports all tool classes from subdirectories.
"""

import os
import importlib
from typing import List, Type
from agent.base_tool import BaseTool

def discover_tools() -> List[Type[BaseTool]]:
    """
    Automatically discover all tool classes in subdirectories.
    Each tool directory should have tool.py with a class ending in 'Tool'.
    """
    tools = []
    current_dir = os.path.dirname(__file__)
    
    # Get all subdirectories in tools/
    for item in os.listdir(current_dir):
        item_path = os.path.join(current_dir, item)
        
        # Skip files and __pycache__
        if not os.path.isdir(item_path) or item.startswith('__'):
            continue
            
        try:
            # Import the tool module
            module = importlib.import_module(f'agent.tools.{item}.tool')
            
            # Find all classes that end with 'Tool' and inherit from BaseTool
            for attr_name in dir(module):
                attr = getattr(module, attr_name)
                
                if (isinstance(attr, type) and 
                    issubclass(attr, BaseTool) and 
                    attr != BaseTool and
                    attr_name.endswith('Tool')):
                    tools.append(attr)
                    
        except (ImportError, AttributeError) as e:
            print(f"Warning: Could not load tool from {item}: {e}")
            continue
    
    return tools

# Auto-discover and expose all tools
__all__ = []
_discovered_tools = discover_tools()

# Export tool classes
for tool_class in _discovered_tools:
    globals()[tool_class.__name__] = tool_class
    __all__.append(tool_class.__name__)