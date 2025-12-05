"""
Pytest configuration for MCP server testing.

Uses in-memory transport via create_connected_server_and_client_session
for fast, isolated tests without network overhead.
"""

import pytest


@pytest.fixture
def anyio_backend() -> str:
    """Specify the async backend for anyio."""
    return "asyncio"
