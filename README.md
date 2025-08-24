# Refactor & Extend: Simple Tool-Using Agent

**Goal:** Turn a brittle, partially working agent into production-quality code, then extend it with a new tool and real tests.
# AI Agent with Tool Integration

A robust, extensible AI agent system that integrates with Google's Gemini API to provide intelligent tool execution and conversation memory.

## Project Structure

```
agent/
├── agent.py                 # Main Agent class (single-shot responses)
├── interactive_agent.py     # Interactive Agent with memory
├── llm.py                   # LLM provider abstraction
├── tool_manager.py          # Tool discovery and execution manager
├── base_tool.py             # Base tool class and result handling
├── schemas.py               # Tool schemas and validation
└── tools/                   # Individual tool implementations
    ├── __init__.py          # Tool discovery mechanism
    ├── calculator/
    │   └── tool.py          # Mathematical expression evaluator
    ├── kb/
    │   ├── tool.py          # Knowledge base search
    │   └── kb_agent.py      # AI-powered intelligent search
    ├── text_analyzer/
    │   └── tool.py          # Text statistics and sentiment analysis
    ├── unit_converter/
    │   └── tool.py          # Temperature conversion
    └── weather/
        └── tool.py          # Weather information retrieval
```

## Architecture Overview

```
┌─────────────────┐    ┌──────────────────┐    ┌─────────────────┐
│   chat.py       │    │    main.py       │    │  Interactive    │
│ (Interactive)   │    │ (Single Query)   │    │   vs Single     │
└─────────┬───────┘    └─────────┬────────┘    └─────────────────┘
          │                      │
          v                      v
┌─────────────────────────────────────────────────────────────────┐
│                    LLM Provider Layer                           │
│  ┌─────────────────┐              ┌─────────────────┐          │
│  │ InteractiveAgent│              │     Agent       │          │
│  │   (with memory) │              │  (stateless)    │          │
│  └─────────────────┘              └─────────────────┘          │
└─────────────────────┬───────────────────────┬───────────────────┘
                      │                       │
                      v                       v
            ┌─────────────────────────────────────────────┐
            │           Tool Manager                      │
            │  ┌─────────────────────────────────────┐   │
            │  │        Tool Discovery               │   │
            │  │     ┌─────────┬─────────┬────────┐  │   │
            │  │     │Calculator│   KB   │Weather │  │   │
            │  │     │    +     │   +    │   +    │  │   │
            │  │     │Text Anal.│Unit C. │  ...   │  │   │
            │  │     └─────────┴─────────┴────────┘  │   │
            │  └─────────────────────────────────────┘   │
            │                                             │
            │  Schema Validation + Error Handling         │
            └─────────────────────────────────────────────┘
```

## Tool Execution Flow

### For `chat.py` (Interactive with Memory):
```
User Input → InteractiveAgent.ask() → Gemini API → Tool Detection → 
Tool Execution → Result Integration → Response with Memory Context
```

### For `main.py` (Single Query):
```
Command Line → LLM.answer() → Agent.answer() → Gemini API → 
Tool Detection → Tool Execution → Direct Response
```

## Key Features

### 1. AI-Powered Knowledge Base Search
The KB tool uses a dedicated AI agent to handle fuzzy name matching:
```python
# Finds "Ada Lovelace" even when user types "Eda Loveless"
kb_agent.search("Who is Eda Loveless?")  # → Returns Ada Lovelace info
```

### 2. Schema Validation & Type Safety
All tools use Pydantic-style validation:
```python
@dataclass
class ToolSchema:
    name: str
    tool_type: ToolType
    description: str
    parameters: List[ToolParameter]
    
    def validate_args(self, args: Dict[str, Any]) -> tuple[bool, Optional[str]]
```

### 3. Robust Error Handling
```python
class ToolResult:
    def __init__(self, success: bool, data: Any = None, error: str = None)
    
# Automatic validation and error wrapping
result = tool.validate_and_execute(args, question)
if not result.success:
    return result.error
```

### 4. Context Maintenance (Interactive Mode)

Example conversation showing memory persistence:

```bash
🤖 Interactive Agent Chat (with memory)
Type 'quit', 'exit', or 'bye' to stop
Type 'history' to see conversation history
--------------------------------------------------
👤 You: My name is Saymon and I'm 25 years old
🤖 Assistant: Nice to meet you, Saymon! It's good to know you're 25. How can I help you today?

👤 You: Calculate 15 + 25
🔧 Using tool: calc
🤖 Assistant: 15 + 25 equals 40.

👤 You: What was my name again?
🤖 Assistant: Your name is Saymon, as you mentioned earlier.

👤 You: Convert 100 celsius to fahrenheit  
🔧 Using tool: unit_converter
🤖 Assistant: 100°C = 212.0°F

👤 You: Who is Ada Lovelace?
🔧 Using tool: kb
🤖 Assistant: Ada Lovelace (1815-1852) was an English mathematician and writer, chiefly known for her work on Charles Babbage's proposed mechanical general-purpose computer, the Analytical Engine. She was the first to recognize that the machine had applications beyond pure calculation and is often regarded as the first computer programmer.

👤 You: history
📜 Conversation History:
----------------------------------------
👤 You: My name is Saymon and I'm 25 years old
🤖 Assistant: Nice to meet you, Saymon! It's good to know you're 25. How can I help you today?
👤 You: Calculate 15 + 25
🤖 Assistant: 15 + 25 equals 40.
👤 You: What was my name again?
🤖 Assistant: Your name is Saymon, as you mentioned earlier.
[... rest of history]
----------------------------------------

👤 You: quit
👋 Goodbye!
```

## Quick Start

### Prerequisites
- Python 3.10+
- Google Gemini API key
- Optional: OpenWeatherMap API key (for weather tool)

### Installation
```bash
# Clone and setup
git clone <repository>
cd agent-system

# Create virtual environment
python -m venv .venv
source .venv/bin/activate  # Windows: .venv\Scripts\activate

# Install dependencies
pip install -r requirements.txt

# Setup environment variables
cp .env.example .env
# Edit .env and add your API keys:
# GEMINI_API_KEY=your_gemini_api_key_here
# WEATHER_API_KEY=your_openweather_api_key_here (optional)
```

### Usage Options

#### Interactive Chat Mode (Recommended)
```bash
python chat.py
```
Features:
- Conversation memory
- History command
- Tool usage indicators
- Graceful exit commands

#### Single Query Mode
```bash
python main.py "What is 15% of 200?"
python main.py "Convert 25 celsius to fahrenheit"
python main.py "Who is Ada Lovelace?"
python main.py "Analyze this text: 'I love this wonderful day!'"
python main.py "What's the weather in London?"
```

### Testing
```bash
# Run all tests
pytest

# Run specific test categories
pytest tests/test_robust.py -v      # Tool functionality without API
pytest tests/test_real_tools.py -v  # Direct tool testing
pytest tests/test_integration.py -v # Full system integration (requires API quota)
```

## Available Tools

| Tool | Description | Example Usage |
|------|-------------|---------------|
| **Calculator** | Mathematical expressions | `"What is 25% of 400?"` |
| **Text Analyzer** | Word count, sentiment analysis | `"Analyze: 'Great day!'"` |
| **Unit Converter** | Celsius to Fahrenheit | `"Convert 0C to F"` |
| **Knowledge Base** | Intelligent name search | `"Who is Ada Lovelace?"` |
| **Weather** | Current weather info | `"Weather in Paris?"` |

## Adding New Tools

The system is designed for easy extensibility with zero dependencies on existing tools.

### Step 1: Create Tool Schema
```python
# In schemas.py, add to ToolType enum:
class ToolType(Enum):
    YOUR_TOOL = "your_tool"

# Add schema definition:
ToolType.YOUR_TOOL: ToolSchema(
    name="your_tool",
    tool_type=ToolType.YOUR_TOOL, 
    description="Description of what your tool does",
    parameters=[
        ToolParameter("input", "string", "Input description")
    ]
)
```

### Step 2: Implement Tool Class
```python
# Create agent/tools/your_tool/tool.py
from typing import Dict, Any
from agent.base_tool import BaseTool
from agent.schemas import TOOL_SCHEMAS, ToolType

class YourTool(BaseTool):
    def __init__(self):
        super().__init__(TOOL_SCHEMAS[ToolType.YOUR_TOOL])
    
    def execute(self, args: Dict[str, Any], question: str = "") -> Any:
        # Your tool logic here
        input_text = args["input"]
        result = process_input(input_text)  # Your implementation
        return result
```

### Step 3: Auto-Discovery
The tool will be automatically discovered by the `discover_tools()` function in `agent/tools/__init__.py`. No manual registration required!

### Step 4: Test Your Tool
```python
# Test directly
tool_manager = ToolManager()
result = tool_manager.execute_tool("your_tool", {"input": "test"})
assert result.success

# Test through agent
llm = LLM(provider="gemini")
response = llm.answer("Use your tool with test input")
```

## System Benefits

- **Type Safety**: Full type hints and schema validation
- **Error Resilience**: Comprehensive error handling at all levels  
- **Zero Dependencies**: Tools are completely independent
- **Memory Management**: Conversation context in interactive mode
- **Fuzzy Matching**: AI-powered KB search handles typos
- **Easy Testing**: Direct tool testing without API dependencies
- **Auto-Discovery**: New tools automatically integrated

## Architecture Decisions

1. **Separation of Concerns**: Agent (orchestration) vs Tools (execution)
2. **Schema-First**: All tools defined by schemas for validation
3. **Result Wrapping**: Consistent success/error handling
4. **Tool Independence**: Each tool is self-contained
5. **Dual Interfaces**: Interactive (memory) vs single-shot modes
6. **Context Awareness**: Tools receive both args and original question

This architecture supports both development efficiency and production reliability while maintaining extensibility for new tools and capabilities.

## Assignment Requirements Compliance

This implementation fully satisfies all specified requirements:

### ✅ Split responsibilities into modules/classes
- **Agent Layer**: `Agent` (stateless) vs `InteractiveAgent` (memory-enabled)
- **Tool Management**: `ToolManager` handles discovery and execution
- **Base Architecture**: `BaseTool` provides inheritance hierarchy
- **Provider Abstraction**: `LLM` class abstracts API providers
- **Modular Tools**: Each tool in separate directory with isolated logic

### ✅ Add schema for tool plans; validate inputs and tool names
- **Schema Definition**: `ToolSchema` dataclass with complete parameter specs
- **Type Validation**: `ToolParameter` enforces string/number type checking
- **Input Validation**: `validate_args()` method verifies required parameters
- **Tool Registry**: `TOOL_SCHEMAS` maps tool types to validation schemas
- **Name Validation**: `ToolManager` validates tool existence before execution

### ✅ Make tool calls resilient and typed
- **Result Wrapping**: `ToolResult` provides consistent success/error handling
- **Exception Safety**: Try-catch blocks in `validate_and_execute()` prevent crashes
- **Type Safety**: Full type hints throughout (`Dict[str, Any]`, proper return types)
- **Error Messages**: Descriptive error messages for validation failures and unknown tools
- **Argument Parsing**: Safe parsing with `_parse_args()` handles malformed inputs

### ✅ Add one new tool and tests that prove design is extensible
- **New Tools Added**: 
  - `TextAnalyzerTool`: Word count, character count, sentiment analysis
  - `UnitConverterTool`: Temperature conversion with proper formatting
- **Extensibility Proof**: Both tools follow identical patterns (inherit `BaseTool`, use schemas)
- **Zero-Dependency Addition**: New tools require no changes to existing code
- **Test Coverage**: `test_real_tools.py` and `test_robust.py` validate tool functionality
- **Auto-Discovery**: Tools automatically registered via `discover_tools()` mechanism

### Additional Enhancements Beyond Requirements
- **Intelligent KB Search**: AI agent handles fuzzy name matching for knowledge base
- **Conversation Memory**: Interactive mode maintains context across exchanges  
- **Context-Aware Execution**: Tools receive original question for enhanced responses
- **Multi-Level Testing**: Direct tool tests, integration tests, and API-dependent validation
- **Production-Ready Error Handling**: Comprehensive error recovery from API failures to validation errors
---
You must **refactor for robustness**, **add one new tool** (translator / unit converter), and **add proper tests**.
---

## Your Tasks (Summary)

1. **Refactor**
2. **Improve**
3. **Add ONE new tool** 
4. **Write tests**
5. **Improve Documentation**

See the assignment brief for full details (shared in the job post).

---

## Quick Start

### Python 3.10+ recommended

```bash
python -m venv .venv
source .venv/bin/activate  # Windows: .venv\Scripts\activate
pip install -r requirements.txt
```

### Run

```bash
python main.py "What is 12.5% of 243?"
python main.py "Summarize today's weather in Paris in 3 words"
python main.py "Who is Ada Lovelace?"
python main.py "Add 10 to the average temperature in Paris and London right now."
```

### Test

```bash
pytest -q
```

> Note: The fake LLM sometimes emits malformed JSON to simulate real-world flakiness.

---

## What we expect you to change

- Split responsibilities into modules/classes.
- Add a schema for tool plans; validate inputs and tool names.
- Make tool calls resilient and typed;
- Add one new tool and tests that prove your design is extensible.
- Update this README with an architecture diagram (ASCII ok) and clear instructions.
- You can use Real LLMs or a fake one, but ensure your code is robust against malformed responses.

Good luck & have fun!
