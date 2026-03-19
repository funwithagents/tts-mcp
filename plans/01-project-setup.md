# Plan 01 — Project Setup

## Goal

Initialise the `uv` project, declare all dependencies, create the source tree skeleton, and wire up the entry point so `uv run tts-mcp-server --help` works.

## Tasks

### Project initialisation

- [ ] Run `uv init --name tts-mcp --package` in the repo root
- [ ] Set `requires-python = ">=3.11"` in `pyproject.toml`

### Dependencies

- [ ] Add runtime dependencies:
  - `mcp[cli]`
  - `uvicorn`
  - `elevenlabs`
  - `sounddevice`
  - `numpy`
- [ ] Add dev dependencies:
  - `pytest`
  - `pytest-asyncio`
  - `pytest-mock`

### Entry point

- [ ] Declare `tts-mcp-server = "tts_mcp.cli:main"` under `[project.scripts]`

### pytest config

- [ ] Add to `pyproject.toml`:
  ```toml
  [tool.pytest.ini_options]
  testpaths = ["tests", "tests-e2e"]
  asyncio_mode = "auto"
  ```

### Source tree skeleton

Create empty files (just module-level docstrings or `pass`) for:

- [ ] `src/tts_mcp/__init__.py`
- [ ] `src/tts_mcp/_logging.py`
- [ ] `src/tts_mcp/cli.py`
- [ ] `src/tts_mcp/config.py`
- [ ] `src/tts_mcp/audio.py`
- [ ] `src/tts_mcp/engine.py`
- [ ] `src/tts_mcp/server.py`
- [ ] `src/tts_mcp/modules/__init__.py`
- [ ] `src/tts_mcp/modules/base.py`
- [ ] `src/tts_mcp/modules/elevenlabs_v1.py`

### Test tree skeleton

- [ ] `tests/__init__.py`
- [ ] `tests/conftest.py`
- [ ] `tests/modules/__init__.py`
- [ ] `tests-e2e/__init__.py`

### Config example

- [ ] Write `config.example.json` matching the schema in `specs/configuration.md`

### Smoke test

- [ ] `uv run tts-mcp-server --help` exits 0 and prints usage
- [ ] `uv run pytest tests/` collects 0 tests and exits 0
