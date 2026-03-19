# Implementation Details — 01 Project Setup

## What was implemented

- `uv init --name tts-mcp --package` initialised the project with a `.venv` and `pyproject.toml`.
- All runtime deps (`mcp[cli]`, `uvicorn`, `elevenlabs`, `sounddevice`, `numpy`) and dev deps (`pytest`, `pytest-asyncio`, `pytest-mock`) declared and installed.
- Entry point `tts-mcp-server = "tts_mcp.cli:main"` declared; `cli.py` implements `main()` with argparse (`--config PATH` required).
- Full source skeleton under `src/tts_mcp/` and test skeleton under `tests/` and `tests-e2e/` — each file contains only a module docstring.
- `config.example.json` written to match the configuration spec.

## Deviations from spec

- `uv init` generated `requires-python = ">=3.13"` (matching the local interpreter); updated to `>=3.11` as specified.
- `uv init` placed a stub `main()` in `__init__.py` and wired the script there; moved `main()` to `cli.py` and updated the entry point accordingly.

## Non-obvious decisions

- `cli.py` currently only parses `--config` and does nothing else — subsequent plans will add the real wiring (config load → engine → server).
- `pytest tests/` exits with code 5 ("no tests collected") rather than 0. This is standard pytest behaviour and harmless at this stage; it will resolve once test files are added in later plans.

## Known limitations

- No actual functionality yet — all modules are docstring-only stubs.
