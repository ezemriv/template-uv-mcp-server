# CLAUDE.md

This file provides guidance to Claude Code (claude.ai/code) when working with code in this repository.

## Project Overview

This is a reusable template for building MCP (Model Context Protocol) servers using Python 3.11+ with `uv` as the dependency manager. It uses the FastMCP framework from the official MCP Python SDK to provide tools, resources, and prompts to Claude Desktop and other MCP clients.

## Key Commands

### Running the Server

```bash
# Run using the console script entry point
uv run template-uv-mcp-server

# Run as a Python module
uv run python -m template_uv_mcp_server

# Run with MCP Inspector for development/testing
uv run mcp dev src/template_uv_mcp_server/server.py
```

### Development

```bash
# Install/sync dependencies
uv sync

# Add new dependencies
uv add <package>          # Runtime dependency
uv add --dev <package>    # Development dependency

# Install server in Claude Desktop
uv run mcp install src/template_uv_mcp_server/server.py --name "Template Server"
```

## Architecture

### Core Structure

The project follows a src-layout package structure:

- **`src/template_uv_mcp_server/server.py`**: Main server implementation using FastMCP
  - Creates a `FastMCP` instance with server name
  - Defines tools with `@mcp.tool()` decorator
  - Defines resources with `@mcp.resource()` decorator
  - Defines prompts with `@mcp.prompt()` decorator
  - Exports `main()` function that calls `mcp.run()`

- **`src/template_uv_mcp_server/__init__.py`**: Package initialization
  - Exports `main` function and `__version__`
  - Entry point for the console script

- **`src/template_uv_mcp_server/__main__.py`**: Module execution support
  - Enables `python -m template_uv_mcp_server` invocation

### MCP Primitives

**Tools**: Functions decorated with `@mcp.tool()` that perform actions
- Must have type hints and clear docstrings (used as tool descriptions)
- Can perform side effects (like POST endpoints)
- Optional `Context` parameter provides logging and MCP capabilities

**Resources**: Functions decorated with `@mcp.resource()` that expose data
- Should not perform heavy computation
- Use URI templates for dynamic resources (e.g., `"myapp://document/{id}"`)
- Like GET endpoints - read-only data access

**Prompts**: Functions decorated with `@mcp.prompt()` that provide reusable templates
- Return strings or lists of messages for LLM interactions
- Help standardize common interaction patterns

### Configuration

- **`pyproject.toml`**: Defines project metadata, dependencies, and console script entry point
- **`.python-version`**: Pins Python version to 3.11 for uv
- **`uv.lock`**: Generated lock file for reproducible dependency resolution

## Claude Desktop Integration

The server is configured to run in Claude Desktop using `uv --directory` pattern:

```json
{
  "mcpServers": {
    "template-server": {
      "command": "uv",
      "args": [
        "--directory",
        "/absolute/path/to/template-uv-mcp-server",
        "run",
        "template-uv-mcp-server"
      ]
    }
  }
}
```

## Development Patterns

### Adding New Tools

Tools should have clear type hints and docstrings:

```python
@mcp.tool()
def my_tool(param: str, optional_param: int = 10) -> dict:
    """Clear description of what this tool does."""
    return {"result": f"processed {param}"}
```

### Using Context for Logging

```python
from mcp.server.fastmcp import Context

@mcp.tool()
async def advanced_tool(param: str, ctx: Context) -> str:
    """Tool with logging."""
    await ctx.info(f"Processing: {param}")
    return result
```

### Structured Output with Pydantic

```python
from pydantic import BaseModel

class Result(BaseModel):
    status: str
    value: float

@mcp.tool()
def analyze(data: str) -> Result:
    """Return validated structured data."""
    return Result(status="success", value=1.0)
```

### Lifespan Management

For setup/teardown of resources like database connections:

```python
from contextlib import asynccontextmanager
from collections.abc import AsyncIterator

@asynccontextmanager
async def app_lifespan(server: FastMCP) -> AsyncIterator[dict]:
    # Setup phase
    db = await Database.connect()
    try:
        yield {"db": db}
    finally:
        # Cleanup phase
        await db.disconnect()

mcp = FastMCP("My App", lifespan=app_lifespan)
```

## Testing

### Running Tests

```bash
# Run all tests
uv run pytest

# Run with verbose output
uv run pytest -v

# Run specific test file
uv run pytest tests/test_server.py

# Run specific test class or function
uv run pytest tests/test_server.py::TestTools::test_hello_tool_default
```

### Testing Pattern

Tests use in-memory transport via `create_connected_server_and_client_session` from `mcp.shared.memory`:

```python
import pytest
from mcp.shared.memory import create_connected_server_and_client_session
from template_uv_mcp_server.server import mcp

@pytest.mark.asyncio
async def test_my_tool():
    async with create_connected_server_and_client_session(
        mcp, raise_exceptions=True
    ) as session:
        result = await session.call_tool("my_tool", arguments={"param": "value"})
        assert result.content[0].text == "expected"
```

Key points:
- Each test creates its own session (avoids event loop issues with fixtures)
- Use `raise_exceptions=True` to surface server errors in tests
- Test tools via `session.call_tool()`
- Test resources via `session.read_resource()` and `session.list_resources()`
- Test prompts via `session.get_prompt()` and `session.list_prompts()`

## Transport Options

- **stdio** (default): Used by Claude Desktop and most clients
- **streamable-http**: For web deployments: `mcp.run(transport="streamable-http")`
- **sse** (legacy): Server-Sent Events transport

## Important Notes

- Python 3.11+ required (specified in `.python-version` and `pyproject.toml`)
- Uses `uv` for dependency management - NOT pip or poetry
- FastMCP handles MCP protocol details - just define decorated functions
- Docstrings are critical - they become tool descriptions shown to Claude
- Type hints are required for all tool parameters and return values
