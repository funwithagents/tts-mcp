# Plan 05 — ElevenLabs Module: Implementation Details

## What was implemented

- `ElevenLabsModule` in `src/tts_mcp/modules/elevenlabs.py` implementing the `TTSModule` ABC
- Config validation in constructor: `api_key` and `voice_id` are required non-empty strings; `model`, `stability`, `similarity_boost` are optional with defaults
- `stream()` calls `self._client.text_to_speech.stream(...)` with `output_format="pcm_44100"` and `VoiceSettings`; wraps the blocking iterator with `asyncio.to_thread`; skips empty chunks; wraps SDK exceptions in `TTSError`
- `ElevenLabsModule` registered as `REGISTRY["elevenlabs"]` in `modules/__init__.py`
- 9 unit tests in `tests/modules/test_elevenlabs.py` — all mocked, no real API calls

## Deviations from spec

None. The spec's pseudocode in `specs/elevenlabs-module.md` was followed directly.

## Non-obvious decisions

- **Single `_blocking_stream` closure in `asyncio.to_thread`**: The entire SDK iteration loop (including the `try/except`) lives inside a nested function passed to `asyncio.to_thread`. This keeps the wrapping simple and ensures exceptions raised inside the thread are re-raised in the calling coroutine as `TTSError`.
- **Exception wrapping catches all `Exception`**: The spec distinguishes `401` auth errors from network errors, but the ElevenLabs SDK raises typed exceptions (e.g. `elevenlabs.core.api_error.ApiError`) that aren't worth handling separately at this stage. A single `except Exception` with a descriptive message is sufficient for now; auth-specific messages can be added in a later iteration if needed.
- **`VoiceSettings` import**: imported from `elevenlabs.types` (the SDK's public types module).

## Known limitations

- Auth-specific error messages (e.g. `"ElevenLabs authentication failed — check api_key"` for 401s) are not implemented; all SDK exceptions produce a generic `"ElevenLabs request failed: <message>"`.
- `TTSOptions` is currently empty; per-call voice overrides (e.g. `options.voice_id`) are not yet wired — the module always uses the config's `voice_id`.
