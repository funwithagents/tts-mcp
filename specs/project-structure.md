# Project Structure

## Repository layout

```
tts-mcp/
├── AGENTS.md
├── pyproject.toml
├── config.example.json
├── specs/
├── plans/
├── implementation-details/
├── src/
│   └── tts_mcp/
│       ├── __init__.py
│       ├── _logging.py          # setup_logging() for entry points
│       ├── cli.py               # argparse → wires config + engine + server
│       ├── config.py            # Config dataclasses + load_config() + ConfigError
│       ├── audio.py             # AudioPlayer (sounddevice)
│       ├── engine.py            # TTSEngine.speak()
│       ├── server.py            # FastMCP app, speak tool
│       └── modules/
│           ├── __init__.py      # REGISTRY + load_module()
│           ├── base.py          # TTSModule ABC, TTSOptions, TTSError
│           └── elevenlabs.py
├── tests/
│   ├── conftest.py
│   ├── test_config.py
│   ├── test_audio.py
│   ├── test_engine.py
│   ├── test_server.py
│   └── modules/
│       └── test_elevenlabs.py
└── tests-e2e/
    └── test_speak.py
```

## `pyproject.toml` highlights

```toml
[project]
name = "tts-mcp"
requires-python = ">=3.11"

dependencies = [
    "mcp[cli]",
    "uvicorn",
    "elevenlabs",
    "sounddevice",
    "numpy",
]

[project.scripts]
tts-mcp-server = "tts_mcp.cli:main"

[tool.pytest.ini_options]
testpaths = ["tests", "tests-e2e"]
asyncio_mode = "auto"
```

## Python version

Requires Python ≥ 3.11 (used for `str | None` union syntax, `tomllib`, and match statements).

## Key dependencies

| Package | Purpose |
|---------|---------|
| `mcp[cli]` | MCP Python SDK (FastMCP, StreamableHTTP transport) |
| `uvicorn` | ASGI server for StreamableHTTP |
| `elevenlabs` | Official ElevenLabs Python SDK |
| `sounddevice` | PortAudio bindings for PCM playback |
| `numpy` | PCM byte→array conversion for sounddevice |

## Dev dependencies

```toml
[dependency-groups]
dev = [
    "pytest",
    "pytest-asyncio",
    "pytest-mock",
]
```
