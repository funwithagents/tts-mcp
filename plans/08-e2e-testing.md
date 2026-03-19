# Plan 08 — E2E Testing

## Goal

Write an end-to-end test that starts the MCP server in-process, calls the `speak` tool via an MCP client, and asserts the call succeeds with no error. No audio output verification.

## Reference

See `specs/` — specifically `mcp-server.md` and `architecture.md`.

## Requirements

- A valid `config.json` with a real ElevenLabs API key must be present at the repo root (gitignored).
- `libportaudio2` must be installed (`sudo apt-get install libportaudio2`).

## Tasks

### `tests-e2e/test_speak.py`

- [ ] Fixture: load `config.json` from repo root; skip the test if it does not exist
- [ ] Fixture: build `TTSEngine` from config (same wiring as `cli.py`)
- [ ] Fixture: start `uvicorn` in a background thread with the FastMCP StreamableHTTP app; wait for it to be ready (poll `/mcp` or use a startup event); yield the server URL; stop after the test
- [ ] Test `test_speak_returns_ok`:
  - Connect an MCP client to the server URL
  - Call the `speak` tool with `{"text": "Hello from the TTS MCP test"}`
  - Assert the result content is `"OK"` (no error string)
- [ ] Test `test_speak_empty_text_returns_error`:
  - Call the `speak` tool with `{"text": ""}`
  - Assert the result contains an error message (not `"OK"`)

### Note on audio during e2e tests

The `AudioPlayer` will attempt to open a real `sounddevice` stream. On a CI machine without audio hardware, this may fail. Two options:
1. Patch `sounddevice.OutputStream` in the e2e fixture to be a no-op (preferred for CI)
2. Document that e2e tests require audio hardware

For now, patch `sounddevice.OutputStream` so the test is runnable without speakers.
