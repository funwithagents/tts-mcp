# Plan 08 — E2E Testing: Implementation Details

## What was implemented

- `tests-e2e/helpers.py`: shared utilities — `load_config()`, `find_free_port()`, `_wait_for_port()`, `start_mcp_server()`, `stop_mcp_server()`
- `tests-e2e/conftest.py`: `server_url` async fixture — skips if `config.json` absent, starts the subprocess, yields the MCP URL, stops after the test
- `tests-e2e/test_speak.py`: two tests — `test_speak_returns_ok` and `test_speak_empty_text_returns_error`

## Deviations from original plan

- **Subprocess instead of in-process**: the original plan called for starting `uvicorn` in a background thread. Switched to a real subprocess (`uv run tts-mcp-server --config <tmpconfig>`) for better isolation and to exercise the actual CLI entry point.
- **No sounddevice patching**: the original plan suggested patching `sounddevice.OutputStream` to a no-op for CI. This is not feasible when the server runs in a subprocess. E2E tests now require real audio hardware (or a PulseAudio null sink). Documented in the plan's note.
- **`test_speak_empty_text_returns_error` not in the plan tasks**: it was in the original plan but was dropped from the rewritten tasks section. Implemented anyway as it requires no API call and passes immediately.

## Non-obvious decisions

- **`sys.path.insert` in `conftest.py`**: `conftest.py` files don't support relative imports in pytest, and the directory name `tests-e2e` (with a hyphen) is not a valid Python package name. Inserting the directory into `sys.path` at the top of `conftest.py` is the simplest workaround.
- **`find_free_port()` via `socket.bind(0)`**: binding to port 0 lets the OS assign a free port; the port is released before the subprocess starts, so there is a small TOCTOU window, but in practice it is negligible for local testing.
- **`streamable_http_client` (underscore)**: the MCP SDK originally exported `streamablehttp_client`; the current version uses `streamable_http_client`. Using the latter avoids a deprecation warning.
- **TCP readiness poll**: `_wait_for_port` polls a raw TCP connection (not an HTTP request) to detect when uvicorn is accepting connections. This is simpler and more reliable than polling `/mcp`.

## Known limitations

- E2E tests require audio hardware; there is no fallback for CI machines without a sound device.
- Only `test_speak_returns_ok` exercises the full ElevenLabs → miniaudio → sounddevice pipeline; more scenarios (e.g. long text, invalid voice ID) are not covered.
