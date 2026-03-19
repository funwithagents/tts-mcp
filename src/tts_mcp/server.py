"""MCP server: speak tool, StreamableHTTP transport."""
import logging

from mcp.server.fastmcp import FastMCP

from tts_mcp.engine import TTSEngine
from tts_mcp.modules.base import TTSError

log = logging.getLogger(__name__)


def create_server(engine: TTSEngine) -> FastMCP:
    mcp = FastMCP("tts-mcp")

    @mcp.tool()
    async def speak(text: str) -> str:
        """Synthesize text and play it via the configured TTS engine."""
        if not text:
            return "TTS error: text must not be empty"
        try:
            await engine.speak(text)
            return "OK"
        except TTSError as e:
            log.error("TTS error: %s", e)
            return f"TTS error: {e}"

    return mcp
