# Plan 04 — TTS Module Interface: Implementation Notes

## What was implemented

- `modules/base.py`: `TTSError(Exception)`, `TTSOptions` (empty dataclass), `TTSModule` ABC with `stream()` abstract method.
- `modules/__init__.py`: `REGISTRY: dict[str, type[TTSModule]] = {}` and `load_module(tts_config: dict) -> TTSModule`.
- `tests/modules/test_tts_module_interface.py`: three unit tests covering unknown type, registered type, and default instantiation of `TTSOptions`.

## Deviations from spec

None. The plan and spec were consistent; both were followed exactly.

## Non-obvious decisions

- **Full config dict passed to constructor**: `load_module` passes the entire `tts_config` dict (including `"type"`) to the module constructor. The plan explicitly says "full dict including `type`". Module constructors are responsible for ignoring or extracting the fields they need.
- **`REGISTRY` starts empty**: Plan 04 defines the registry as empty; module files (e.g. `elevenlabs.py`) will populate it via `REGISTRY["elevenlabs"] = ElevenLabsModule` when imported. The `__init__.py` does not import module files — callers must import the module file to trigger registration.
- **`TTSOptions` as a dataclass**: Using `@dataclass` on an empty class enables future fields to be added without changing the constructor signature.

## Known limitations

- The registry is populated lazily by importing module files. If no module file is imported before calling `load_module`, all type lookups will raise `ConfigError`. The engine (plan 06) must import the relevant module file at startup.
