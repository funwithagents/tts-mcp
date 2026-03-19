"""TTS module registry and load_module()."""
from tts_mcp.config import ConfigError
from tts_mcp.modules.base import TTSModule

REGISTRY: dict[str, type[TTSModule]] = {}


def load_module(tts_config: dict) -> TTSModule:
    module_type = tts_config.get("type")
    if module_type not in REGISTRY:
        raise ConfigError(f"Unknown TTS module type: {module_type!r}")
    cls = REGISTRY[module_type]
    return cls(tts_config)
