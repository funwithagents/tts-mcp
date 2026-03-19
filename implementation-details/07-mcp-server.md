# Plan 07 — MCP Server: Implementation Details

## What was implemented

- `server.py`: `create_server(engine: TTSEngine) -> FastMCP` factory that creates a `FastMCP("tts-mcp")` app and registers the `speak` tool inside a closure, giving it access to the engine.
- `cli.py`: completed with `load_module`, `AudioPlayer`, `TTSEngine`, `create_server`, and `uvicorn.run` wiring.
- `tests/test_server.py`: 3 unit tests covering the three paths (empty input, success, TTSError).

## Deviations from spec

None. The implementation matches the plan and spec exactly.

## Non-obvious decisions

- **Tool access to engine via closure**: the `speak` function is defined inside `create_server`, capturing `engine` from the enclosing scope. This avoids global state and keeps the factory pattern clean.
- **Internal tool extraction in tests**: FastMCP doesn't expose a public method to call a registered tool directly. Tests access `mcp._tool_manager._tools` to extract the underlying function. This is an internal API but unavoidable without spinning up a full server. The approach is consistent with how the engine tests mock collaborators.
- **`asyncio_mode = "auto"`**: all test functions are plain `async def` without `@pytest.mark.asyncio` — the pytest-asyncio auto mode handles them.

## Known limitations

- The smoke test (manual: `uv run tts-mcp-server --config config.example.json`) is not automated — it requires a real ElevenLabs API key. Covered by plan 08 (E2E testing).
- `uvicorn.run` is blocking and not tested — the test suite only tests the tool logic, not the transport layer.
