---
title: Linly-X-Gemini
emoji: 🎭
colorFrom: blue
colorTo: purple
sdk: gradio
sdk_version: 4.44.0
app_file: webui.py
pinned: false
license: mit
---

# Linly-X-Gemini: Real-time AI Avatar

🚀 **Real-time AI Avatar powered by Gemini 2.5 Flash + MuseTalk**

## Features

- ⚡ **<1 second latency** - Real-time conversation
- 🎭 **MuseTalk streaming** - High-quality lip-sync at ~25 FPS
- 🗣️ **Gemini Live** - Natural conversation with interruption support
- 🎨 **Custom avatars** - Upload any image or video
- 🔊 **Aoede voice** - Premium text-to-speech

## Quick Start

1. Click "Prepare Avatar" (uses default or upload custom)
2. Click "Connect to Gemini"
3. Start talking!

## Architecture

```
User Mic → Railway Bridge → Gemini Live API → Audio Stream → MuseTalk → Video Frames
```

## Technical Stack

- **LLM**: Gemini 2.5 Flash (via WebSocket)
- **Avatar**: MuseTalk (real-time streaming)
- **Audio**: 16kHz PCM, 200ms buffer
- **Video**: ~25 FPS streaming

## Credits

- [Linly-Talker](https://github.com/Kedreamix/Linly-Talker) - Original project
- [MuseTalk](https://github.com/TMElyralab/MuseTalk) - Avatar engine
- [Gemini Live](https://ai.google.dev/gemini-api/docs/live) - Conversation API

## License

MIT License - See LICENSE file for details
