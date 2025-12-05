"""
Tests for the template MCP server.

Tests tools, resources, and prompts using in-memory transport
for fast, isolated testing without network overhead.

Note: Each test creates its own client session to avoid event loop
issues with async fixtures.
"""

import pytest
from mcp.shared.memory import create_connected_server_and_client_session
from mcp.types import TextContent

from template_uv_mcp_server.server import mcp


class TestTools:
    """Tests for MCP tools."""

    @pytest.mark.asyncio
    async def test_list_tools(self) -> None:
        """Test that tools are properly registered and listable."""
        async with create_connected_server_and_client_session(
            mcp, raise_exceptions=True
        ) as session:
            result = await session.list_tools()

            tool_names = [tool.name for tool in result.tools]
            assert "hello" in tool_names

    @pytest.mark.asyncio
    async def test_hello_tool_default(self) -> None:
        """Test hello tool with default parameter."""
        async with create_connected_server_and_client_session(
            mcp, raise_exceptions=True
        ) as session:
            result = await session.call_tool("hello", arguments={})

            assert len(result.content) == 1
            assert isinstance(result.content[0], TextContent)
            assert result.content[0].text == "Hello, World!"

    @pytest.mark.asyncio
    async def test_hello_tool_with_name(self) -> None:
        """Test hello tool with custom name parameter."""
        async with create_connected_server_and_client_session(
            mcp, raise_exceptions=True
        ) as session:
            result = await session.call_tool("hello", arguments={"name": "Claude"})

            assert len(result.content) == 1
            assert isinstance(result.content[0], TextContent)
            assert result.content[0].text == "Hello, Claude!"

    @pytest.mark.asyncio
    async def test_hello_tool_description(self) -> None:
        """Test that hello tool has proper description from docstring."""
        async with create_connected_server_and_client_session(
            mcp, raise_exceptions=True
        ) as session:
            result = await session.list_tools()

            hello_tool = next(t for t in result.tools if t.name == "hello")
            assert hello_tool.description == "Say hello to someone."


class TestResources:
    """Tests for MCP resources."""

    @pytest.mark.asyncio
    async def test_list_resources(self) -> None:
        """Test that resources are properly registered and listable."""
        async with create_connected_server_and_client_session(
            mcp, raise_exceptions=True
        ) as session:
            result = await session.list_resources()

            # Compare using string representation since uri is AnyUrl
            resource_uris = [str(r.uri) for r in result.resources]
            assert "template://info" in resource_uris

    @pytest.mark.asyncio
    async def test_read_info_resource(self) -> None:
        """Test reading the info resource."""
        async with create_connected_server_and_client_session(
            mcp, raise_exceptions=True
        ) as session:
            result = await session.read_resource("template://info")

            assert len(result.contents) == 1
            content = result.contents[0]
            assert content.text == "This is a template MCP server. Customize it for your needs!"

    @pytest.mark.asyncio
    async def test_info_resource_description(self) -> None:
        """Test that info resource has proper description from docstring."""
        async with create_connected_server_and_client_session(
            mcp, raise_exceptions=True
        ) as session:
            result = await session.list_resources()

            info_resource = next(
                r for r in result.resources if str(r.uri) == "template://info"
            )
            assert info_resource.description == "Get template information."


class TestPrompts:
    """Tests for MCP prompts."""

    @pytest.mark.asyncio
    async def test_list_prompts(self) -> None:
        """Test that prompts are properly registered and listable."""
        async with create_connected_server_and_client_session(
            mcp, raise_exceptions=True
        ) as session:
            result = await session.list_prompts()

            prompt_names = [p.name for p in result.prompts]
            assert "greeting_prompt" in prompt_names

    @pytest.mark.asyncio
    async def test_get_greeting_prompt(self) -> None:
        """Test getting the greeting prompt with a name parameter."""
        async with create_connected_server_and_client_session(
            mcp, raise_exceptions=True
        ) as session:
            result = await session.get_prompt(
                "greeting_prompt", arguments={"name": "Alice"}
            )

            assert len(result.messages) == 1
            message = result.messages[0]
            assert message.role == "user"

            content = message.content
            assert isinstance(content, TextContent)
            assert content.text == "Please write a friendly greeting for Alice."

    @pytest.mark.asyncio
    async def test_greeting_prompt_description(self) -> None:
        """Test that greeting prompt has proper description from docstring."""
        async with create_connected_server_and_client_session(
            mcp, raise_exceptions=True
        ) as session:
            result = await session.list_prompts()

            greeting_prompt = next(
                p for p in result.prompts if p.name == "greeting_prompt"
            )
            assert greeting_prompt.description == "Generate a greeting prompt."

    @pytest.mark.asyncio
    async def test_greeting_prompt_arguments(self) -> None:
        """Test that greeting prompt has correct argument definition."""
        async with create_connected_server_and_client_session(
            mcp, raise_exceptions=True
        ) as session:
            result = await session.list_prompts()

            greeting_prompt = next(
                p for p in result.prompts if p.name == "greeting_prompt"
            )
            assert greeting_prompt.arguments is not None
            assert len(greeting_prompt.arguments) == 1
            assert greeting_prompt.arguments[0].name == "name"
            assert greeting_prompt.arguments[0].required is True


class TestServerCapabilities:
    """Tests for server capabilities and initialization."""

    @pytest.mark.asyncio
    async def test_server_has_tools_capability(self) -> None:
        """Test that server advertises tools capability."""
        async with create_connected_server_and_client_session(
            mcp, raise_exceptions=True
        ) as session:
            result = await session.list_tools()
            assert result.tools is not None

    @pytest.mark.asyncio
    async def test_server_has_resources_capability(self) -> None:
        """Test that server advertises resources capability."""
        async with create_connected_server_and_client_session(
            mcp, raise_exceptions=True
        ) as session:
            result = await session.list_resources()
            assert result.resources is not None

    @pytest.mark.asyncio
    async def test_server_has_prompts_capability(self) -> None:
        """Test that server advertises prompts capability."""
        async with create_connected_server_and_client_session(
            mcp, raise_exceptions=True
        ) as session:
            result = await session.list_prompts()
            assert result.prompts is not None
