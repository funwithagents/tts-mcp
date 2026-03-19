# Plan 04 — TTS Module Interface

## Goal

Define the `TTSModule` ABC, shared dataclasses, `TTSError`, and the module registry in `modules/base.py` and `modules/__init__.py`.

## Reference

See `specs/tts-module-interface.md`.

## Tasks

### `modules/base.py`

- [ ] Define `TTSError(Exception)`
- [ ] Define `TTSOptions` dataclass (currently empty, reserved for future per-call overrides)
- [ ] Define `TTSModule` ABC with:
  - `@abstractmethod async def stream(self, text: str, options: TTSOptions, callback: Callable[[bytes], None]) -> None`
  - Docstring matching the spec contract

### `modules/__init__.py`

- [ ] Define `REGISTRY: dict[str, type[TTSModule]] = {}` (populated by each module file via import)
- [ ] Implement `load_module(tts_config: dict) -> TTSModule`:
  - Read `tts_config["type"]`
  - Look up in `REGISTRY`; raise `ConfigError` for unknown type
  - Construct the module with `tts_config` (full dict including `type`)
  - Return the instance

### Tests (`tests/modules/test_tts_module_interface.py`)

- [ ] `load_module` with unknown `type` raises `ConfigError`
- [ ] `load_module` with a registered type constructs and returns the correct instance
- [ ] `TTSOptions` can be instantiated with no arguments
