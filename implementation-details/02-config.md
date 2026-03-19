# Implementation Details — Plan 02: Configuration

## What was implemented

- `_logging.py`: `setup_logging()` calls `logging.basicConfig` with the specified format at INFO level.
- `config.py`: `ConfigError`, three dataclasses (`TTSConfig`, `AudioConfig`, `ServerConfig`), and `load_config()` which reads JSON, validates required blocks, validates `tts.type` and `server.port`, and returns typed instances.
- `cli.py`: `main()` calls `setup_logging()` first, parses `--config PATH`, calls `load_config()`, and logs a startup line.
- `tests/test_config.py`: 10 unit tests covering all required scenarios.

## Deviations from spec

None. The spec says `tts.type` must match a registered module key, but the plan scopes validation to "non-empty string" only — registry validation is deferred to the engine (plan 06).

## Non-obvious decisions

- `TTSConfig.raw` stores a copy of the entire `tts` dict (including `type`), so the module constructor receives all fields without special-casing.
- `server.port` validation rejects non-int values (e.g. a string `"8000"`) in addition to out-of-range ints, since JSON could technically provide either.

## Known limitations

- `tts.type` is not validated against the module registry here; unknown type strings only raise `ConfigError` when `load_module()` is called in the engine.
