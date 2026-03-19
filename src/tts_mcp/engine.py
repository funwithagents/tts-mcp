"""TTSEngine: wires module + player, exposes speak()."""
from tts_mcp.audio import AudioPlayer
from tts_mcp.modules.base import TTSModule, TTSOptions


class TTSEngine:
    def __init__(self, module: TTSModule, player: AudioPlayer) -> None:
        self._module = module
        self._player = player

    async def speak(self, text: str) -> None:
        options = TTSOptions()
        try:
            await self._module.stream(text, options, callback=self._player.feed)
        finally:
            self._player.drain()
