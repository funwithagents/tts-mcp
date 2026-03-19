# TTS MCP — Implementation Plans Index

Plans are meant to be executed in order. Each plan builds on the previous ones.

| Plan | File | Description | Status |
|---|---|---|---|
| 01 | [Project Setup](01-project-setup.md) | `uv` init, dependencies, source tree, entry points | done |
| 02 | [Configuration](02-config.md) | Config dataclasses, loading, validation, CLI arg parsing | done |
| 03 | [Audio Player](03-audio-player.md) | `sounddevice` output stream, `AudioPlayer`, PCM feed + drain | done |
| 04 | [TTS Module Interface](04-tts-module-interface.md) | ABC, `TTSOptions`, `TTSError`, registry | not started |
| 05 | [ElevenLabs Module](05-elevenlabs-module.md) | Streaming PCM via ElevenLabs SDK, config, error handling | not started |
| 06 | [TTS Engine](06-tts-engine.md) | Wires module + player, `speak()` entry point | not started |
| 07 | [MCP Server](07-mcp-server.md) | `speak` tool, StreamableHTTP, startup wiring | not started |
| 08 | [E2E Testing](08-e2e-testing.md) | In-process server, `speak` tool call, no-error assertion | not started |

**Legend:** not started · in progress · done
