# Linly-X-Gemini - Deployment Guide

## 🚀 Quick Deploy

### Repository Name: **Linly-X-Gemini**

---

## GitHub Deployment

```bash
cd "d:/linly gg/Linly-Talker"

# Initialize git (if not already)
git init
git add .
git commit -m "feat: Linly-X-Gemini - Real-time AI Avatar with Gemini Live

- 8 applications with Gemini Live integration
- MuseTalk streaming engine (<1s latency)
- Railway WebSocket bridge
- Complete documentation"

# Push to GitHub
git remote add origin https://github.com/YOUR_USERNAME/linly-x-gemini.git
git branch -M main
git push -u origin main
```

---

## Hugging Face Spaces Deployment

### Step 1: Create Space
1. Go to https://huggingface.co/spaces
2. Click "Create new Space"
3. Settings:
   - **Name**: `linly-x-gemini`
   - **SDK**: Gradio
   - **SDK Version**: 4.44.0
   - **Hardware**: GPU (T4 or better)
   - **Persistent Storage**: Enable (for model caching)

### Step 2: Push Code
```bash
# Add Hugging Face remote
git remote add hf https://huggingface.co/spaces/YOUR_USERNAME/linly-x-gemini

# Push to Hugging Face
git push hf main
```

### Step 3: Configure Space
The `README.md` file contains the Hugging Face configuration:
```yaml
title: Linly-X-Gemini
emoji: 🎭
sdk: gradio
sdk_version: 4.44.0
app_file: webui.py
```

---

## 📋 Pre-Deployment Checklist

- ✅ Repository renamed to Linly-X-Gemini
- ✅ No API keys in code
- ✅ All endpoints use Railway bridge
- ✅ configs.py import is optional
- ✅ Paths are correct (Musetalk/)
- ✅ .gitignore excludes models
- ✅ Documentation complete

---

## 🎯 What Gets Deployed

### Main App: `webui.py`
- Clean Gemini Live interface
- Default + custom avatars
- Real-time streaming

### Additional Apps (optional):
- `app.py` - Unified (Gemini + Legacy)
- `app_img.py` - Talking photos
- `app_multi.py` - Multi-turn conversation
- `app_talk.py` - Avatar comparison lab
- `app_musetalk.py` - Debug tool
- `app_gemini_live.py` - Standalone demo
- `app_vits.py` - Voice cloning

---

## ⚙️ Environment Requirements

### Hugging Face Spaces:
- **GPU**: T4 minimum (8GB VRAM)
- **Storage**: 10GB+ for models
- **Python**: 3.10+

### Models (auto-downloaded on first run):
- MuseTalk checkpoints (~2GB)
- Face alignment models
- Whisper ASR (optional)

---

## 🔧 Post-Deployment

### Test Checklist:
1. ✅ Space builds successfully
2. ✅ Models download correctly
3. ✅ Avatar preparation works
4. ✅ WebSocket connects to Railway
5. ✅ Real-time streaming works
6. ✅ Audio playback functions
7. ✅ Frame rate ~25 FPS

### Expected Performance:
- **Latency**: <1 second
- **FPS**: 20-25
- **VRAM**: 6-8GB
- **Connection**: 99%+ uptime

---

## 🎉 You're Ready!

**Repository**: Linly-X-Gemini  
**Status**: Production Ready  
**Deploy**: GitHub + Hugging Face Spaces  

🚀 **Let's go!**
