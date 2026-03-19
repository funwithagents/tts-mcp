"""Server entry point: parses args and wires everything together."""
import argparse
import logging

import uvicorn

from tts_mcp._logging import setup_logging
from tts_mcp.audio import AudioPlayer
from tts_mcp.config import load_config
from tts_mcp.engine import TTSEngine
from tts_mcp.modules import load_module
from tts_mcp.server import create_server

log = logging.getLogger(__name__)


def main() -> None:
    setup_logging()
    parser = argparse.ArgumentParser(
        prog="tts-mcp-server",
        description="TTS MCP server — exposes a speak tool over StreamableHTTP",
    )
    parser.add_argument("--config", required=True, metavar="PATH", help="Path to config JSON file")
    args = parser.parse_args()

    tts_cfg, audio_cfg, server_cfg = load_config(args.config)
    log.info("Config loaded: tts.type=%s host=%s port=%d", tts_cfg.type, server_cfg.host, server_cfg.port)

    module = load_module(tts_cfg.raw)
    player = AudioPlayer(device=audio_cfg.device)
    engine = TTSEngine(module, player)
    mcp_app = create_server(engine)

    uvicorn.run(
        mcp_app.streamable_http_app(),
        host=server_cfg.host,
        port=server_cfg.port,
    )
