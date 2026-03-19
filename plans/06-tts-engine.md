# Plan 06 — TTS Engine

## Goal

Implement `TTSEngine` in `engine.py`: wire a `TTSModule` and an `AudioPlayer` together behind a single async `speak()` method.

## Reference

See `specs/architecture.md` (component responsibilities, data flow).

## Tasks

### `engine.py`

- [ ] Implement `TTSEngine.__init__(module: TTSModule, player: AudioPlayer)`: store both
- [ ] Implement `async TTSEngine.speak(text: str) -> None`:
  - Build `TTSOptions()`
  - Call `await module.stream(text, options, callback=player.feed)`
    - Since `module.stream` runs the SDK iterator in a thread, `player.feed` will be called from that thread — this is acceptable given `sounddevice` stream writes are thread-safe
  - After `stream` returns, call `player.drain()`
  - Propagate `TTSError` to the caller (do not catch here)

### Tests (`tests/test_engine.py`)

- [ ] `speak()` calls `module.stream` with the correct text and a `TTSOptions` instance
- [ ] `speak()` calls `player.drain()` after `module.stream` completes
- [ ] `speak()` calls `player.drain()` even if `module.stream` raises `TTSError`
- [ ] `speak()` propagates `TTSError` after draining
