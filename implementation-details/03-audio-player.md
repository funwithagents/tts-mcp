# Plan 03 — Audio Player: Implementation Details

## What was implemented

`AudioPlayer` in `src/tts_mcp/audio.py`:
- `__init__(device=None)`: stores the device reference, does not open the stream.
- `feed(chunk: bytes)`: skips empty chunks, lazily opens a `sounddevice.OutputStream` on the first non-empty call, converts bytes to a `numpy.int16` array via `np.frombuffer`, and writes it with `stream.write()` (blocking).
- `drain()`: calls `stream.stop()` then `stream.close()` if a stream is open, then resets the reference to `None`. Idempotent.

4 unit tests in `tests/test_audio.py` covering all plan tasks. `sounddevice.OutputStream` is mocked via `pytest-mock` to avoid requiring audio hardware.

## Deviations from spec

- The spec mentions a queue-based approach as an alternative to blocking writes. The simpler blocking-write path was chosen: `stream.write()` fills the PortAudio buffer and returns quickly; no async bridging is needed since `feed` is a sync callback.
- `asyncio.to_thread` wrapping was not added — the plan note says the blocking write is acceptable since it just fills a buffer.

## Non-obvious decisions

- `stream.start()` must be called explicitly after constructing `sd.OutputStream` (the stream does not auto-start in the default configuration).
- `np.frombuffer` returns a read-only view; `sounddevice.write()` accepts it without copying.

## Known limitations

- No backpressure: if the TTS provider produces chunks faster than the audio device can consume them, the queue inside PortAudio may overflow. Acceptable for the current use case (real-time TTS at normal speech rates).
