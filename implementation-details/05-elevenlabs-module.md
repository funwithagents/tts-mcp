# Plan 05 — ElevenLabs Module: Implementation Details

## What was implemented

- `ElevenLabsModule` in `src/tts_mcp/modules/elevenlabs.py` implementing the `TTSModule` ABC
- Config validation in constructor: `api_key` and `voice_id` are required non-empty strings; `model`, `stability`, `similarity_boost` are optional with defaults
- `stream()` requests `output_format="mp3_44100_128"` from ElevenLabs, decodes MP3 chunks to signed 16-bit PCM mono via `miniaudio.stream_any`, and calls `callback(pcm_chunk.tobytes())` for each decoded chunk; the entire loop runs in `asyncio.to_thread`; empty ElevenLabs chunks are skipped before being passed to miniaudio; all exceptions are wrapped in `TTSError`
- `ElevenLabsModule` registered as `REGISTRY["elevenlabs"]` in `modules/__init__.py`
- Unit tests in `tests/modules/test_elevenlabs.py` — all mocked (no real API calls, no real MP3 decoding)

## Deviations from original spec

- **MP3 instead of PCM from ElevenLabs**: the free ElevenLabs tier does not support `pcm_44100` output. The module requests `mp3_44100_128` instead and decodes to PCM in-process using `miniaudio`. The `AudioPlayer` contract (receives raw signed 16-bit PCM) is unchanged; decoding is fully encapsulated in the module.

## Non-obvious decisions

- **`miniaudio.stream_any` for streaming decode**: accepts a source generator yielding arbitrary byte chunks of MP3 and yields decoded PCM `array.array` incrementally — a natural fit for the streaming callback model.
- **Single `_blocking_stream` closure in `asyncio.to_thread`**: the entire encode-decode loop (ElevenLabs iterator + miniaudio decode + callback calls + try/except) lives inside one closure passed to `asyncio.to_thread`, keeping async wrapping simple.
- **Exception wrapping catches all `Exception`**: a single `except Exception` covers both ElevenLabs SDK exceptions and miniaudio decode errors; auth-specific messages can be added in a later iteration.
- **`VoiceSettings` import**: imported from `elevenlabs.types` (the SDK's public types module).

## Known limitations

- Auth-specific error messages (e.g. for 401s) are not implemented; all exceptions produce a generic `"ElevenLabs request failed: <message>"`.
- `TTSOptions` is currently empty; per-call voice overrides are not yet wired — the module always uses the config's `voice_id`.
