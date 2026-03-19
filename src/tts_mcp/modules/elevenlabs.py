"""ElevenLabs streaming TTS module."""
import asyncio

from elevenlabs import ElevenLabs
from elevenlabs.types import VoiceSettings

from tts_mcp.config import ConfigError
from tts_mcp.modules.base import TTSError, TTSModule, TTSOptions


class ElevenLabsModule(TTSModule):

    def __init__(self, config: dict) -> None:
        api_key = config.get("api_key")
        if not api_key:
            raise ConfigError("ElevenLabs module requires a non-empty 'api_key'")

        voice_id = config.get("voice_id")
        if not voice_id:
            raise ConfigError("ElevenLabs module requires a non-empty 'voice_id'")

        self._voice_id: str = voice_id
        self._model: str = config.get("model", "eleven_flash_v2_5")
        self._stability: float = config.get("stability", 0.5)
        self._similarity_boost: float = config.get("similarity_boost", 0.75)
        self._client = ElevenLabs(api_key=api_key)

    async def stream(self, text: str, options: TTSOptions, callback) -> None:
        def _blocking_stream():
            try:
                for chunk in self._client.text_to_speech.stream(
                    text=text,
                    voice_id=self._voice_id,
                    model_id=self._model,
                    output_format="pcm_44100",
                    voice_settings=VoiceSettings(
                        stability=self._stability,
                        similarity_boost=self._similarity_boost,
                    ),
                ):
                    if chunk:
                        callback(chunk)
            except Exception as exc:
                raise TTSError(f"ElevenLabs request failed: {exc}") from exc

        await asyncio.to_thread(_blocking_stream)
