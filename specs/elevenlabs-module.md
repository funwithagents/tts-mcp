# ElevenLabs Module

## Overview

`elevenlabs` implements `TTSModule` using the ElevenLabs streaming TTS API. It requests raw PCM output so chunks can be fed directly to `AudioPlayer` without decoding.

## Config fields

All fields go under the `tts` block in `config.json` alongside `"type": "elevenlabs"`.

| Field | Type | Required | Default | Description |
|-------|------|----------|---------|-------------|
| `api_key` | string | yes | — | ElevenLabs API key. |
| `voice_id` | string | yes | — | Default voice ID used when `TTSOptions.voice_id` is `None`. |
| `model` | string | no | `"eleven_flash_v2_5"` | ElevenLabs model ID. `eleven_flash_v2_5` is recommended for low latency; `eleven_multilingual_v2` for quality. |
| `stability` | float | no | `0.5` | Voice stability (0.0–1.0). |
| `similarity_boost` | float | no | `0.75` | Similarity boost (0.0–1.0). |

## Implementation notes

### SDK vs raw HTTP

Use the official `elevenlabs` Python SDK. It provides a `generate` function (non-streaming) and a `stream` function for streaming. Use the streaming interface.

### Output format

Request `output_format="pcm_44100"` from the ElevenLabs API. This yields raw signed 16-bit PCM at 44100 Hz mono — no decoding needed, directly consumable by `AudioPlayer`.

### Streaming

The ElevenLabs SDK streaming interface yields `bytes` chunks. For each chunk, call `callback(chunk)`.

```python
async def stream(self, text, options, callback):
    for chunk in elevenlabs_client.text_to_speech.stream(
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
```

Note: the ElevenLabs SDK streaming method may be synchronous (returns an iterator, not async). Wrap the blocking iteration with `asyncio.to_thread` or run in an executor to avoid blocking the event loop.

### Error handling

- Wrap SDK exceptions in `TTSError` with a descriptive message.
- `401` / auth errors → raise `TTSError("ElevenLabs authentication failed — check api_key")`
- Network errors → raise `TTSError("ElevenLabs request failed: <original message>")`

## Module ID

Registered in `REGISTRY` as `"elevenlabs"`.
