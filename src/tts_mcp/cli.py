"""Server entry point: parses args and wires everything together."""
import argparse
import logging

from tts_mcp._logging import setup_logging
from tts_mcp.config import load_config

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
