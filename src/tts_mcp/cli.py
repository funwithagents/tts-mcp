"""Server entry point: parses args and wires everything together."""
import argparse


def main() -> None:
    parser = argparse.ArgumentParser(
        prog="tts-mcp-server",
        description="TTS MCP server — exposes a speak tool over StreamableHTTP",
    )
    parser.add_argument("--config", required=True, metavar="PATH", help="Path to config JSON file")
    parser.parse_args()
