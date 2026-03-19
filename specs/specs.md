# TTS MCP — Specifications Index

## Reading Order

| # | Spec | Description | Implemented |
|---|---|---|---|
| 1 | [Overview](overview.md) | Goals, components, constraints, non-goals | no |
| 2 | [Architecture](architecture.md) | System diagram, concurrency model, data flow | no |
| 3 | [Configuration](configuration.md) | Config file schema, fields, validation rules | yes |
| 4 | [MCP Server](mcp-server.md) | `speak` tool, transport, lifecycle, error handling | yes |
| 5 | [TTS Module Interface](tts-module-interface.md) | ABC, audio format contract, registry, `TTSOptions` | yes |
| 6 | [ElevenLabs Module](elevenlabs-module.md) | Streaming PCM, config fields, SDK usage, error handling | yes |
| 7 | [Audio Player](audio-player.md) | `AudioPlayer`, sounddevice integration, stream lifecycle | yes |
| 8 | [Project Structure](project-structure.md) | Folder layout, entry points, dependencies | yes |

**Legend:** no = not implemented · yes = implemented
