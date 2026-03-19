# Plan 07 — MCP Server

## Goal

Implement the MCP server in `server.py` with a single `speak` tool, wire everything together in `cli.py`, and verify the server starts and accepts tool calls.

## Reference

See `specs/mcp-server.md` and `specs/architecture.md`.

## Tasks

### `server.py`

- [ ] Create a `FastMCP("tts-mcp")` app
- [ ] Implement `speak` tool:
  ```python
  @mcp.tool()
  async def speak(text: str) -> str:
  ```
  - Return an error string if `text` is empty
  - Call `await engine.speak(text)`
  - Return `"OK"` on success
  - Catch `TTSError` and return `f"TTS error: {e}"` (do not raise)
- [ ] Expose a factory function `create_server(engine: TTSEngine) -> FastMCP` that wires the engine into the tool and returns the app

### `cli.py`

- [ ] Parse `--config PATH` with `argparse`
- [ ] Call `setup_logging()`
- [ ] Call `load_config(path)` → `tts_cfg, audio_cfg, server_cfg`
- [ ] Call `load_module(tts_cfg.raw)` → `module`
- [ ] Construct `AudioPlayer(device=audio_cfg.device)`
- [ ] Construct `TTSEngine(module, player)`
- [ ] Call `create_server(engine)` → `mcp_app`
- [ ] Run via StreamableHTTP transport:
  ```python
  uvicorn.run(
      mcp_app.streamable_http_app(),
      host=server_cfg.host,
      port=server_cfg.port,
  )
  ```

### Tests (`tests/test_server.py`)

- [ ] `speak("")` returns an error string (does not call engine)
- [ ] `speak("hello")` calls `engine.speak("hello")` and returns `"OK"`
- [ ] `speak("hello")` catches `TTSError` and returns an error string containing the message

### Smoke test

- [ ] `uv run tts-mcp-server --config config.example.json` starts without crashing (manual test; requires a valid API key or mock)
