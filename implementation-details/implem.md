# TTS MCP — Implementation Details Index

This folder contains notes written **after** each component is implemented.
Each file explains non-obvious choices, gotchas, and deviations from the original specs.

| Plan | File | Description | Written |
|---|---|---|---|
| 01 — Project Setup | [01-project-setup.md](01-project-setup.md) | uv setup, dependency notes | no |
| 02 — Configuration | [02-config.md](02-config.md) | Config loading, validation notes | no |
| 03 — Audio Player | [03-audio-player.md](03-audio-player.md) | sounddevice integration notes | no |
| 04 — TTS Module Interface | [04-tts-module-interface.md](04-tts-module-interface.md) | ABC and registry notes | no |
| 05 — ElevenLabs Module | [05-elevenlabs-module.md](05-elevenlabs-module.md) | ElevenLabs SDK integration notes | no |
| 06 — TTS Engine | [06-tts-engine.md](06-tts-engine.md) | Engine wiring notes | no |
| 07 — MCP Server | [07-mcp-server.md](07-mcp-server.md) | speak tool, StreamableHTTP notes | no |
| 08 — E2E Testing | [08-e2e-testing.md](08-e2e-testing.md) | In-process server, speak tool call, assertions | no |

**Legend:** no = not yet written · yes = written

## Convention

Each file in this folder should cover:
- **What was implemented** (brief summary)
- **Deviations from spec** (if any, and why)
- **Non-obvious decisions** (trade-offs, workarounds, SDK quirks)
- **Known limitations** (anything deferred to a later iteration)
