# AGENTS.md — TTS MCP Project

## What this project is

An MCP server that exposes text-to-speech capabilities via a `speak` tool. It accepts text input, synthesizes speech through a pluggable TTS module (ElevenLabs first), and plays the audio in real-time on the server machine using streaming playback.

- **Language**: Python, project managed with `uv`
- **MCP SDK**: official Python SDK (`modelcontextprotocol/python-sdk`)
- **Transport**: StreamableHTTP — enables remote access on a local network
- **One active module**: a single TTS module is loaded at startup, selected via `tts.type` in config

## Key design decisions

- **Streaming playback**: audio is streamed from the TTS provider and fed to the audio device chunk-by-chunk, minimising latency before sound starts.
- **Callback-based streaming**: the module layer accepts a `callback: Callable[[bytes], None]` for each audio chunk — this decouples the module from the playback mechanism and makes the engine testable without audio hardware.
- **PCM output from ElevenLabs**: the ElevenLabs module requests raw PCM output (no decoding step needed); `sounddevice` consumes it directly.
- **`speak` tool only (v1)**: no `synthesize`/file output, no `list_voices`, no MCP resources.
- **Pluggable modules**: the `tts` config block uses `type` to select the module; all other fields under `tts` are module-specific. Only one module is active at a time.
- **`sounddevice` for playback**: wraps PortAudio, best choice on Ubuntu; device is configurable via `audio.device` (`null` = system default).

## Repository layout

```
tts-mcp/
├── AGENTS.md                    # This file
├── pyproject.toml               # uv project: deps, entry points, pytest config
├── config.example.json          # Config template (no secrets)
├── specs/                       # Full project specifications
│   ├── specs.md                 # Index — start here
│   ├── overview.md
│   ├── architecture.md
│   ├── configuration.md
│   ├── mcp-server.md
│   ├── tts-module-interface.md
│   ├── elevenlabs-module.md
│   ├── audio-player.md
│   └── project-structure.md
├── plans/                       # Phased implementation plans with checkboxes
│   ├── plans.md                 # Index
│   ├── 01-project-setup.md
│   ├── 02-config.md
│   ├── 03-audio-player.md
│   ├── 04-tts-module-interface.md
│   ├── 05-elevenlabs-module.md
│   ├── 06-tts-engine.md
│   ├── 07-mcp-server.md
│   └── 08-e2e-testing.md
├── implementation-details/      # Post-implementation notes (written after each plan is done)
│   ├── implem.md                # Index
│   └── ...                      # One file per plan, added as implementation progresses
├── src/
│   └── tts_mcp/
│       ├── cli.py               # Server entry point (argparse → wires everything)
│       ├── config.py            # Config dataclasses + load/validate
│       ├── audio.py             # AudioPlayer: sounddevice-based streaming playback
│       ├── engine.py            # TTSEngine: wires module + player, exposes speak()
│       ├── server.py            # MCP server: speak tool, StreamableHTTP
│       └── modules/
│           ├── __init__.py      # REGISTRY + load_module()
│           ├── base.py          # TTSModule ABC, TTSOptions, VoiceInfo dataclasses
│           └── elevenlabs.py # ElevenLabs streaming module
├── tests/                       # Unit tests (fast, no external services)
│   ├── conftest.py
│   ├── test_config.py
│   ├── test_audio.py
│   ├── test_engine.py
│   ├── test_server.py
│   └── modules/
│       └── test_elevenlabs.py
└── tests-e2e/                   # End-to-end tests (hit real ElevenLabs API, require config.json + audio hw)
    ├── helpers.py               # Subprocess start/stop, free-port, TCP readiness helpers
    ├── conftest.py              # server_url fixture (starts subprocess, yields MCP URL)
    └── test_speak.py            # speak tool → ElevenLabs → AudioPlayer (no audio verification)
```

## Entry points

```bash
uv run tts-mcp-server --config config.json   # Start the MCP server
uv run pytest                                # Run all tests (unit + e2e)
uv run pytest tests/                         # Unit tests only (no API key needed)
uv run pytest tests-e2e/                     # E2E tests (requires config.json with valid API key)
```

## Config structure

```json
{
  "tts": {
    "type": "elevenlabs",
    "api_key": "...",
    "voice_id": "JBFqnCBsd6RMkjVDRZzb",
    "model": "eleven_flash_v2_5",
    "stability": 0.5,
    "similarity_boost": 0.75
  },
  "audio": {
    "device": null
  },
  "server": {
    "host": "127.0.0.1",
    "port": 8000
  }
}
```

`tts.type` selects the module; all other `tts` fields are module-specific. `audio.device` is `null` for the system default or a device name/index for explicit selection.

## Data flow

```
MCP client
  → speak tool call (text, voice?, ...)
    → TTSEngine.speak(text, options)
      → TTSModule.stream(text, options, callback=AudioPlayer.feed)
        → ElevenLabs API (streaming PCM)
          → AudioPlayer.feed(chunk) on each chunk
            → sounddevice output stream
```

## Tests

| Suite | Location | What it covers | External deps |
|-------|----------|----------------|---------------|
| Unit tests | `tests/` | Config, AudioPlayer, TTSEngine, MCP server, ElevenLabs module — all in-process, no network | None |
| E2E tests | `tests-e2e/test_speak.py` | Full pipeline: MCP `speak` tool → ElevenLabs API → miniaudio decode → AudioPlayer — server runs as subprocess; asserts no error | Real ElevenLabs API key in `config.json`; audio hardware |

E2E tests do **not** verify audio content or playback quality — they assert that the call succeeds and that audio bytes were produced by the module.

## System dependencies

`sounddevice` requires PortAudio:

```bash
sudo apt-get install libportaudio2
```

## Unit testing strategy

Write tests that verify **observable behavior**, not implementation details.

**Rules:**

1. **Test scenarios, not fields.** When verifying a constructed/parsed object, one test asserts all relevant fields together.
2. **Test observable behavior only.** Assert return values, raised exceptions, calls to collaborators, and changes to public state. Never assert on private attributes (`_foo`).
3. **One test per distinct code path.** Keep variants only when they trigger genuinely different logic.
4. **Delete trivial structural tests.** `isinstance(x, SomeClass)` tests are not worth writing.
5. **Error paths deserve individual tests.** `missing_key`, `empty_key`, `unknown_type` are distinct scenarios.
6. **Merge lifecycle tests.** start/stop, connect/disconnect sequences belong in one test.

**Speed rule** — the full unit test suite (`pytest tests/`) must complete in under 5 seconds.

**Smell checklist** — delete or merge a test if it:
- Asserts a private attribute
- Is fully subsumed by another test in the same file
- Checks something that cannot break independently
- Is one of N identical tests differing only in which field they check

## Logging conventions

- Every module uses `log = logging.getLogger(__name__)` (variable name: `log`, not `logger`).
- **Library modules** (`src/tts_mcp/`) never call `basicConfig` or configure handlers.
- **Entry points** (`cli.py`) call `setup_logging()` from `tts_mcp._logging` at startup.

## Adding a new TTS module

1. Create `src/tts_mcp/modules/<name>.py` implementing `TTSModule` from `modules/base.py`
2. Register it in `modules/__init__.py`: `REGISTRY["<name>"] = <ClassName>`
3. Document its config fields (the `tts` block accepts any fields beyond `type`)

## Documentation workflow

This project follows a three-layer documentation convention:

1. **`specs/`** — Written before implementation. Describes *what* to build and *why*.
2. **`plans/`** — Written before implementation. Describes *how* to build it, step by step with checkboxes.
3. **`implementation-details/`** — Written *after* each plan is completed. One file per plan, covering deviations from spec, non-obvious decisions, SDK quirks, and known limitations.

When implementing a plan: tick off tasks in `plans/`, then write the corresponding file in `implementation-details/` and mark it as written in `implem.md`.

## Where to look first

- Understand the system: [`specs/specs.md`](specs/specs.md)
- Check implementation status: [`plans/plans.md`](plans/plans.md)
- Understand what was actually built: [`implementation-details/implem.md`](implementation-details/implem.md)
- Understand data flow: [`specs/architecture.md`](specs/architecture.md)
- Understand the module contract: [`specs/tts-module-interface.md`](specs/tts-module-interface.md)
