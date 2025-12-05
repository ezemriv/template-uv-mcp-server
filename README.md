# template-uv-mcp-server

A reusable template for building MCP (Model Context Protocol) servers using the Python SDK with `uv`.

## Quick Start

```bash
# Clone the repository
git clone https://github.com/ezemriv/template-uv-mcp-server.git
cd template-uv-mcp-server

# Install dependencies
uv sync

# Test with MCP Inspector
uv run mcp dev src/template_uv_mcp_server/server.py

# Run directly
uv run template-uv-mcp-server
```

## Adding to Claude Desktop

### Option 1: Automatic Installation

```bash
uv run mcp install src/template_uv_mcp_server/server.py --name "Template Server"
```

### Option 2: Manual Configuration

Edit your Claude Desktop config file:

- **macOS**: `~/Library/Application Support/Claude/claude_desktop_config.json`
- **Windows**: `%APPDATA%\Claude\claude_desktop_config.json`

Add the following to the `mcpServers` section:

```json
{
  "mcpServers": {
    "template-server": {
      "command": "uv",
      "args": [
        "--directory",
        "/ABSOLUTE/PATH/TO/template-uv-mcp-server",
        "run",
        "template-uv-mcp-server"
      ]
    }
  }
}
```

**Important:** Replace `/ABSOLUTE/PATH/TO/template-uv-mcp-server` with the actual path where you cloned the repository.

### Option 3: Using uvx (for published packages)

If you publish your server to PyPI:

```json
{
  "mcpServers": {
    "template-server": {
      "command": "uvx",
      "args": ["template-uv-mcp-server"]
    }
  }
}
```

## After Configuration

1. Restart Claude Desktop
2. Look for the MCP server icon (hammer 🔨) in the chat input area
3. Your server's tools, resources, and prompts will be available

## Project Structure

```
template-uv-mcp-server/
├── pyproject.toml
├── src/
│   └── template_uv_mcp_server/
│       ├── __init__.py
│       ├── __main__.py
│       └── server.py
└── PLAN.md
```

## Customization

Edit `src/template_uv_mcp_server/server.py` to add your own:

- **Tools**: Functions the LLM can call (`@mcp.tool()`)
- **Resources**: Data the LLM can read (`@mcp.resource()`)
- **Prompts**: Reusable templates (`@mcp.prompt()`)

## References

- [MCP Python SDK](https://github.com/modelcontextprotocol/python-sdk)
- [MCP Documentation](https://modelcontextprotocol.io)
- [uv Documentation](https://docs.astral.sh/uv/)
