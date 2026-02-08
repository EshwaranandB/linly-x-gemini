# Linly-Talker Gemini Live - Directory Structure

```
Linly-Talker/
│
├── 📄 Core Application Files
│   ├── webui.py                    # Main Gradio WebUI (Gemini Live only)
│   ├── app_gemini_live.py          # Standalone Gemini Live app
│   ├── app.py                      # Original multi-feature app
│   ├── app_musetalk.py             # MuseTalk-specific app
│   ├── app_talk.py                 # SadTalker app
│   ├── app_vits.py                 # VITS voice cloning app
│   ├── app_multi.py                # Multi-turn conversation app
│   ├── app_img.py                  # Image-based app
│   └── configs.py                  # Configuration settings
│
├── 🤖 LLM/ (Large Language Models)
│   ├── GeminiLive.py              # ⭐ WebSocket client for Gemini Live
│   ├── Gemini.py                  # Standard Gemini API
│   ├── Linly-api-fast.py          # FastAPI LLM server
│   ├── template.py                # LLM template class
│   ├── __init__.py                # LLM module initialization
│   └── README.md                  # LLM documentation
│
├── 🎭 TFG/ (Talking Face Generation)
│   ├── MuseTalk.py                # ⭐ MuseTalk real-time inference
│   ├── MuseV.py                   # MuseV variant
│   ├── SadTalker.py               # SadTalker implementation
│   ├── Wav2Lip.py                 # Wav2Lip lip-sync
│   ├── Wav2Lipv2.py               # Wav2Lip v2
│   ├── NeRFTalk.py                # NeRF-based talking face
│   ├── Streamer.py                # ⭐ Audio buffer for streaming
│   ├── __init__.py                # TFG module initialization
│   ├── requirements_musetalk.txt  # MuseTalk dependencies
│   ├── requirements_nerf.txt      # NeRF dependencies
│   └── README.md                  # TFG documentation
│
├── 🎤 ASR/ (Automatic Speech Recognition)
│   ├── Whisper.py                 # OpenAI Whisper
│   ├── FunASR.py                  # FunASR implementation
│   ├── OmniSenseVoice.py          # OmniSenseVoice
│   ├── __init__.py                # ASR module initialization
│   ├── requirements_funasr.txt    # FunASR dependencies
│   ├── requirements_OmniSenseVoice.txt
│   └── README.md                  # ASR documentation
│
├── 🔊 TTS/ (Text-to-Speech)
│   ├── EdgeTTS.py                 # Microsoft Edge TTS
│   ├── PaddleTTS.py               # PaddlePaddle TTS
│   ├── XTTS.py                    # XTTS implementation
│   ├── edge_app.py                # EdgeTTS demo app
│   ├── paddletts_app.py           # PaddleTTS demo app
│   ├── __init__.py                # TTS module initialization
│   ├── requirements_paddle.txt    # PaddleTTS dependencies
│   └── README.md                  # TTS documentation
│
├── 🎵 Voice Cloning Models
│   ├── GPT_SoVITS/                # GPT-SoVITS voice cloning (86 files)
│   ├── VITS/                      # VITS voice synthesis (8 files)
│   ├── CosyVoice/                 # CosyVoice model
│   └── ChatTTS/                   # ChatTTS model
│
├── 🎬 Avatar Models & Data
│   ├── Musetalk/                  # MuseTalk models & data (57 files)
│   │   ├── models/                # Model weights
│   │   │   ├── musetalk/          # Core MuseTalk models
│   │   │   ├── dwpose/            # Pose detection models
│   │   │   └── face-parse-bisent/ # Face parsing models
│   │   └── data/
│   │       └── video/             # Avatar video sources
│   │           └── yongen_musev.mp4  # Default avatar
│   │
│   ├── NeRF/                      # NeRF models (59 files)
│   ├── checkpoints/               # SadTalker checkpoints
│   │   ├── mapping_00109-model.pth.tar  # 149MB
│   │   ├── mapping_00229-model.pth.tar  # 149MB
│   │   └── ...
│   └── face_detection/            # Face detection models (12 files)
│
├── 🌐 API & Server
│   └── api/                       # API implementations (8 files)
│
├── 📦 Dependencies & Scripts
│   ├── requirements.txt           # Basic requirements
│   ├── requirements_app.txt       # App-specific requirements
│   ├── requirements_webui.txt     # ⭐ WebUI requirements (main)
│   └── scripts/                   # Utility scripts (5 files)
│       ├── download_models.sh     # Auto-download models
│       └── modelscope_download.py # ModelScope downloader
│
├── 📚 Documentation
│   ├── README.md                  # Main README (English)
│   ├── README_zh.md               # Chinese README
│   ├── FAQ.md                     # ⭐ English FAQ (Gemini Live)
│   ├── AutoDL部署.md              # AutoDL deployment guide
│   ├── SECURITY.md                # Security policy
│   └── docs/                      # Additional documentation
│
├── 🖼️ Assets
│   ├── inputs/                    # Input files (4 files)
│   └── examples/                  # Example files
│
├── 🔧 Configuration
│   ├── .gitignore                 # Git ignore rules
│   ├── .gitmodules                # Git submodules
│   ├── configs.py                 # ⭐ Main configuration
│   └── https_cert/                # HTTPS certificates (2 files)
│
├── 📓 Notebooks
│   └── colab_webui.ipynb          # Google Colab notebook
│
└── 📜 License & Source
    ├── LICENSE                    # Apache 2.0 License
    └── src/                       # Source code (151 files)
```

---

## Key Files for Gemini Live Integration

### Essential Components (⭐)
1. **`webui.py`** - Main application entry point
2. **`LLM/GeminiLive.py`** - WebSocket client for Gemini API
3. **`TFG/MuseTalk.py`** - Real-time avatar rendering
4. **`TFG/Streamer.py`** - Audio buffer management
5. **`FAQ.md`** - Troubleshooting guide
6. **`requirements_webui.txt`** - All dependencies

### Model Weights (Must Download)
```
checkpoints/
├── mapping_00109-model.pth.tar    # 149MB - SadTalker
├── mapping_00229-model.pth.tar    # 149MB - SadTalker
└── ...

Musetalk/models/
├── musetalk/
│   ├── pytorch_model.bin          # Main MuseTalk model
│   └── ...
├── dwpose/
│   └── dw-ll_ucoco_384.pth        # Pose detection
└── face-parse-bisent/
    └── 79999_iter.pth             # Face parsing
```

---

## File Count Summary

| Category | Count |
|----------|-------|
| **Core Apps** | 8 files |
| **LLM Module** | 6 files |
| **TFG Module** | 11 files |
| **ASR Module** | 7 files |
| **TTS Module** | 8 files |
| **Voice Cloning** | ~100 files |
| **Avatar Models** | ~120 files |
| **Documentation** | 6 files |
| **Total** | ~260+ files |

---

## Disk Space Requirements

| Component | Size |
|-----------|------|
| Code & Scripts | ~50 MB |
| MuseTalk Models | ~2.5 GB |
| SadTalker Checkpoints | ~1.5 GB |
| Face Detection | ~500 MB |
| GPT-SoVITS (optional) | ~1 GB |
| **Total (Minimum)** | **~5.5 GB** |
| **Total (Full)** | **~8 GB** |

---

## Quick Navigation

- **Start Here**: `webui.py`
- **Configuration**: `configs.py`
- **Gemini Integration**: `LLM/GeminiLive.py`
- **Avatar Rendering**: `TFG/MuseTalk.py`
- **Audio Streaming**: `TFG/Streamer.py`
- **Troubleshooting**: `FAQ.md`
- **Installation**: `requirements_webui.txt`

---

**Last Updated**: February 2026  
**Repository**: [Kedreamix/Linly-Talker](https://github.com/Kedreamix/Linly-Talker)
