"""Unit tests for ElevenLabsModule."""
import asyncio
from unittest.mock import MagicMock, patch

import pytest

from tts_mcp.config import ConfigError
from tts_mcp.modules.base import TTSError, TTSOptions
from tts_mcp.modules.elevenlabs import ElevenLabsModule


VALID_CONFIG = {
    "type": "elevenlabs",
    "api_key": "test-api-key",
    "voice_id": "test-voice-id",
}


def test_missing_api_key_raises():
    with pytest.raises(ConfigError, match="api_key"):
        ElevenLabsModule({"type": "elevenlabs", "voice_id": "v"})


def test_empty_api_key_raises():
    with pytest.raises(ConfigError, match="api_key"):
        ElevenLabsModule({"type": "elevenlabs", "api_key": "", "voice_id": "v"})


def test_missing_voice_id_raises():
    with pytest.raises(ConfigError, match="voice_id"):
        ElevenLabsModule({"type": "elevenlabs", "api_key": "k"})


def test_empty_voice_id_raises():
    with pytest.raises(ConfigError, match="voice_id"):
        ElevenLabsModule({"type": "elevenlabs", "api_key": "k", "voice_id": ""})


@patch("tts_mcp.modules.elevenlabs.ElevenLabs")
def test_defaults(mock_elevenlabs_cls):
    module = ElevenLabsModule(VALID_CONFIG)
    assert module._model == "eleven_flash_v2_5"
    assert module._stability == 0.5
    assert module._similarity_boost == 0.75


@patch("tts_mcp.modules.elevenlabs.ElevenLabs")
def test_custom_values(mock_elevenlabs_cls):
    config = {**VALID_CONFIG, "model": "eleven_multilingual_v2", "stability": 0.8, "similarity_boost": 0.9}
    module = ElevenLabsModule(config)
    assert module._model == "eleven_multilingual_v2"
    assert module._stability == 0.8
    assert module._similarity_boost == 0.9


@patch("tts_mcp.modules.elevenlabs.ElevenLabs")
def test_stream_calls_callback_for_each_chunk(mock_elevenlabs_cls):
    chunks = [b"chunk1", b"chunk2", b"chunk3"]
    mock_client = MagicMock()
    mock_client.text_to_speech.stream.return_value = iter(chunks)
    mock_elevenlabs_cls.return_value = mock_client

    module = ElevenLabsModule(VALID_CONFIG)
    callback = MagicMock()

    asyncio.run(module.stream("hello", TTSOptions(), callback))

    assert callback.call_count == 3
    callback.assert_any_call(b"chunk1")
    callback.assert_any_call(b"chunk2")
    callback.assert_any_call(b"chunk3")


@patch("tts_mcp.modules.elevenlabs.ElevenLabs")
def test_stream_skips_empty_chunks(mock_elevenlabs_cls):
    chunks = [b"data", b"", b"more"]
    mock_client = MagicMock()
    mock_client.text_to_speech.stream.return_value = iter(chunks)
    mock_elevenlabs_cls.return_value = mock_client

    module = ElevenLabsModule(VALID_CONFIG)
    callback = MagicMock()

    asyncio.run(module.stream("hello", TTSOptions(), callback))

    assert callback.call_count == 2
    callback.assert_any_call(b"data")
    callback.assert_any_call(b"more")


@patch("tts_mcp.modules.elevenlabs.ElevenLabs")
def test_stream_wraps_sdk_exception_in_tts_error(mock_elevenlabs_cls):
    mock_client = MagicMock()
    mock_client.text_to_speech.stream.side_effect = RuntimeError("network failure")
    mock_elevenlabs_cls.return_value = mock_client

    module = ElevenLabsModule(VALID_CONFIG)

    with pytest.raises(TTSError, match="network failure"):
        asyncio.run(module.stream("hello", TTSOptions(), MagicMock()))
