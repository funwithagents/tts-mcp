"""Config dataclasses + load_config() + ConfigError."""
import json
from dataclasses import dataclass
from typing import Any


class ConfigError(Exception):
    pass


@dataclass
class AudioConfig:
    device: str | int | None = None


@dataclass
class ServerConfig:
    host: str = "127.0.0.1"
    port: int = 8000


@dataclass
class TTSConfig:
    type: str
    raw: dict[str, Any]


def load_config(path: str) -> tuple[TTSConfig, AudioConfig, ServerConfig]:
    try:
        with open(path) as f:
            data = json.load(f)
    except json.JSONDecodeError as e:
        raise ConfigError(f"Invalid JSON in {path}: {e}") from e

    for block in ("tts", "audio", "server"):
        if block not in data:
            raise ConfigError(f"Missing required config block: '{block}'")

    tts_raw = data["tts"]
    tts_type = tts_raw.get("type")
    if not tts_type or not isinstance(tts_type, str):
        raise ConfigError("'tts.type' must be a non-empty string")

    server_raw = data["server"]
    port = server_raw.get("port", 8000)
    if not isinstance(port, int) or not (1 <= port <= 65535):
        raise ConfigError(f"'server.port' must be an integer in range 1–65535, got {port!r}")

    tts_cfg = TTSConfig(type=tts_type, raw=dict(tts_raw))
    audio_cfg = AudioConfig(device=data["audio"].get("device", None))
    server_cfg = ServerConfig(
        host=server_raw.get("host", "127.0.0.1"),
        port=port,
    )
    return tts_cfg, audio_cfg, server_cfg
