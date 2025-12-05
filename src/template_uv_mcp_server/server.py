"""
Template MCP Server

A reusable starting point for building MCP servers.
Customize the tools, resources, and prompts for your use case.
"""

from mcp.server.fastmcp import FastMCP

# Create the MCP server instance
mcp = FastMCP("Template Server")


# Example tool
@mcp.tool()
def hello(name: str = "World") -> str:
    """Say hello to someone."""
    return f"Hello, {name}!"


# Example resource
@mcp.resource("template://info")
def get_info() -> str:
    """Get template information."""
    return "This is a template MCP server. Customize it for your needs!"


# Example prompt
@mcp.prompt()
def greeting_prompt(name: str) -> str:
    """Generate a greeting prompt."""
    return f"Please write a friendly greeting for {name}."


def main():
    """Entry point for the MCP server."""
    mcp.run()


if __name__ == "__main__":
    main()
