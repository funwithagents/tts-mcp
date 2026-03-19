# Plan 06 — TTS Engine: Implementation Details

## What was implemented

`TTSEngine` in `src/tts_mcp/engine.py`: a thin async class that wires a `TTSModule` and `AudioPlayer` together behind a single `async speak(text)` method.

Four unit tests in `tests/test_engine.py` cover: correct arguments to `module.stream`, `player.drain()` called on success, `player.drain()` called on `TTSError`, and `TTSError` propagation.

## Deviations from spec

None. The spec said "do not catch here" but also required `drain()` to be called even on error — implemented with `try/finally` which satisfies both requirements exactly.

## Non-obvious decisions

- **`try/finally` for drain**: the plan listed drain-on-error as a separate requirement. Using `try/finally` is the idiomatic way to guarantee `drain()` runs regardless of outcome without catching and re-raising.
- **No logging in engine**: the engine is intentionally minimal; logging belongs in the server layer that calls `speak()`.

## Known limitations

None.
