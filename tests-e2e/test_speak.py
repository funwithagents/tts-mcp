"""E2E tests for the speak MCP tool."""
from __future__ import annotations

from mcp import ClientSession
from mcp.client.streamable_http import streamable_http_client


async def test_speak_returns_ok(server_url):
    async with streamable_http_client(server_url) as (read, write, _):
        async with ClientSession(read, write) as session:
            await session.initialize()
            result = await session.call_tool("speak", {"text": "Hello from the TTS MCP test"})
    assert result.content[0].text == "OK"
