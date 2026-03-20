# tts-mcp

An MCP server that makes any MCP-compatible AI client speak aloud. Text goes in via a tool call, audio plays out on the server machine in real time.

---

## How it works

Run the server on a machine with speakers. Your MCP client (Claude Desktop, an agent, etc.) connects to it over the network and calls the `speak` tool with a text string. The server streams audio from the TTS provider and feeds it to the local audio device chunk by chunk — sound starts playing with minimal latency, before the full audio is even synthesized.

---

## MCP interface

The server exposes a single tool:

**`speak(text)`** — synthesizes `text` and plays it on the server machine. Accepts an optional `voice_id` to override the configured default. Returns when playback is complete.

Transport: StreamableHTTP. Clients connect to `http://<host>:<port>/mcp`.

---

## Prerequisites

- Python 3.11+
- [`uv`](https://docs.astral.sh/uv/)
- PortAudio (for audio playback):
  ```bash
  sudo apt-get install libportaudio2
  ```
- An [ElevenLabs API key](https://elevenlabs.io)

---

## Installation

```bash
git clone <repo-url>
cd tts-mcp
uv sync
```

---

## Configuration

Copy the example config and fill in your credentials:

```bash
cp config.example.json config.json
```

```json
{
  "tts": {
    "type": "elevenlabs",
    "api_key": "sk_...",
    "voice_id": "voice_id",
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

| Field | Description |
|---|---|
| `tts.api_key` | Your ElevenLabs API key |
| `tts.voice_id` | Voice to use — find IDs in the [ElevenLabs voice library](https://elevenlabs.io/voice-library) |
| `tts.model` | ElevenLabs model ID (e.g. `eleven_flash_v2_5` for low latency) |
| `tts.stability` / `tts.similarity_boost` | Voice tuning parameters (0.0–1.0) |
| `audio.device` | Audio output device — `null` for system default, or a device name/index |
| `server.host` / `server.port` | Where the MCP server listens |

## Running the server

```bash
uv run tts-mcp-server --config config.json
```

## Connecting an MCP client

Point your client at:

```
http://<host>:<port>/mcp
```

Example with Claude Desktop — add to your `claude_desktop_config.json`:

```json
{
  "mcpServers": {
    "tts": {
      "type": "http",
      "url": "http://127.0.0.1:8000/mcp"
    }
  }
}
```

The `speak` tool will then be available in your Claude session.


## Architecture: TTS modules

The server uses a pluggable module system. The `tts.type` field in your config selects which module is active — only one runs at a time.

**Built-in modules:**

- **`elevenlabs`** — streams audio from the ElevenLabs API, decodes it on the fly, and feeds raw PCM to the local audio device. Requires an API key; supports voice and model selection.

**Adding your own module** is straightforward — the interface is intentionally minimal:

1. Create a class that extends `TTSModule` (in [src/tts_mcp/modules/base.py](src/tts_mcp/modules/base.py)) and implements a single `async stream(text, options, callback)` method. The method synthesizes text and calls `callback` with each raw PCM chunk as it arrives.
2. Register it by name in the `REGISTRY` dict in [src/tts_mcp/modules/\_\_init\_\_.py](src/tts_mcp/modules/__init__.py).
3. Set `"tts": { "type": "<your-name>", ... }` in your config.

The server, playback layer, and MCP tool need no changes. This makes it easy to plug in any TTS backend such as a local open-source model a different cloud API, or anything that can produce a stream of PCM audio.



## Troubleshooting

**No audio plays**
- Confirm PortAudio is installed: `sudo apt-get install libportaudio2`
- Check `audio.device` — set it to `null` to use the system default, or run `python -c "import sounddevice; print(sounddevice.query_devices())"` to list available devices

**ElevenLabs API errors**
- Verify your `api_key` is correct and active
- Verify your `voice_id` exists in your ElevenLabs account
