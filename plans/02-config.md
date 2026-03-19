# Plan 02 — Configuration

## Goal

Implement config dataclasses, JSON loading, validation, and CLI argument parsing. After this plan, `uv run tts-mcp-server --config config.example.json` loads and validates the config without errors.

## Reference

See `specs/configuration.md` for the full schema and validation rules.

## Tasks

### `config.py`

- [ ] Define `ConfigError(Exception)`
- [ ] Define dataclasses:
  - `AudioConfig(device: str | int | None = None)`
  - `ServerConfig(host: str = "127.0.0.1", port: int = 8000)`
  - `TTSConfig(type: str, raw: dict)` — holds `type` plus the full raw dict for module-specific fields
- [ ] Implement `load_config(path: str) -> tuple[TTSConfig, AudioConfig, ServerConfig]`:
  - Read and parse JSON; raise `ConfigError` with file path on parse error
  - Validate all three top-level blocks are present
  - Validate `tts.type` is a non-empty string
  - Validate `server.port` is in range 1–65535
  - Return typed dataclass instances

### `cli.py`

- [ ] Implement `main()` with `argparse`:
  - `--config PATH` (required)
- [ ] Call `load_config(args.config)` and print a startup log line
- [ ] Call `setup_logging()` from `_logging.py` before anything else

### `_logging.py`

- [ ] Implement `setup_logging()`: configures root logger with format `%(asctime)s %(levelname)s %(name)s: %(message)s`

### Tests (`tests/test_config.py`)

- [ ] Valid config loads all three blocks with correct field values
- [ ] Missing `tts` / `audio` / `server` block raises `ConfigError`
- [ ] `tts.type` missing or empty raises `ConfigError`
- [ ] Invalid JSON raises `ConfigError` mentioning the file path
- [ ] `server.port` out of range raises `ConfigError`
- [ ] Unknown extra fields in `tts` block are preserved in `TTSConfig.raw`
