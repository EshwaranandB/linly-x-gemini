# Gemini Live Avatar - FAQ

## Quick Start Guide

### Prerequisites
- **GPU**: NVIDIA GPU with 11GB+ VRAM (recommended)
- **Python**: 3.10
- **CUDA**: 11.8
- **OS**: Windows/Linux

### Installation

1. **Clone Repository**
```bash
git clone https://github.com/Kedreamix/Linly-Talker.git
cd Linly-Talker
```

2. **Create Environment**
```bash
conda create -n linly python=3.10
conda activate linly
```

3. **Install PyTorch**
```bash
# CUDA 11.8
pip install torch==2.0.1 torchvision==0.15.2 torchaudio==2.0.2 --index-url https://download.pytorch.org/whl/cu118
```

4. **Install Dependencies**
```bash
conda install -q ffmpeg
pip install -r requirements_webui.txt

# MuseTalk dependencies
pip install --no-cache-dir -U openmim
mim install mmengine 
mim install "mmcv>=2.0.1" 
mim install "mmdet>=3.1.0" 
mim install "mmpose>=1.1.0"
```

5. **Download Models**

Download the required models from one of these sources:
- [Baidu Netdisk](https://pan.baidu.com/s/1eF13O-8wyw4B3MtesctQyg?pwd=linl) (Password: linl)
- [HuggingFace](https://huggingface.co/Kedreamix/Linly-Talker)
- [ModelScope](https://modelscope.cn/models/Kedreamix/Linly-Talker)

**Required Models:**
- MuseTalk models → `Musetalk/models/`
- SadTalker checkpoints → `checkpoints/`
- Face detection models → `gfpgan/weights/`

6. **Launch**
```bash
python webui.py
```

Open `http://localhost:7860` in your browser.

---

## Common Issues

### 1. Installation Issues

#### Q: `Microsoft Visual C++ 14.0 is required`
**A:** Install [Microsoft C++ Build Tools](https://visualstudio.microsoft.com/visual-cpp-build-tools/)

#### Q: `version GLIBCXX_3.4.* not found`
**A:** Use Python 3.10 or downgrade libraries:
```bash
pip install pyopenjtalk==0.3.1
pip install opencc==1.1.1
```

#### Q: FFMPEG not found
**A:** Install via conda:
```bash
conda install -q ffmpeg
```

Or on Linux:
```bash
sudo apt install ffmpeg
```

---

### 2. Model & Weight Issues

#### Q: `FileNotFoundError` for model weights
**A:** Ensure models are in correct folders:
```
Linly-Talker/
├── checkpoints/
│   ├── mapping_00109-model.pth.tar (149MB)
│   ├── mapping_00229-model.pth.tar (149MB)
│   └── ...
├── Musetalk/
│   └── models/
│       ├── musetalk/
│       ├── dwpose/
│       └── ...
└── gfpgan/
    └── weights/
```

#### Q: `SadTalker Error: invalid load key, 'v'`
**A:** Re-download `mapping_*.pth.tar` files (they should be 149MB each):
```bash
wget -c https://modelscope.cn/api/v1/models/Kedreamix/Linly-Talker/repo?Revision=master&FilePath=checkpoints%2Fmapping_00109-model.pth.tar
wget -c https://modelscope.cn/api/v1/models/Kedreamix/Linly-Talker/repo?Revision=master&FilePath=checkpoints%2Fmapping_00229-model.pth.tar
```

#### Q: `File is not a zip file` (NLTK error)
**A:** Manually download `nltk_data`:
```python
import nltk
print(nltk.data.path)  # Find cache path
```
Download from [Quark Netdisk](https://pan.quark.cn/s/f48f5e35796b) and place in cache path.

---

### 3. Runtime Issues

#### Q: VRAM overflow / Out of Memory
**A:** 
- **Minimum**: 6GB VRAM (SadTalker only)
- **Recommended**: 11GB+ VRAM (MuseTalk)
- **Solution**: Use lower resolution images or reduce batch size

#### Q: `GFPGANer is not defined`
**A:** Install enhancement module:
```bash
pip install gfpgan
```

#### Q: `Gradio Connection errored out`
**A:** 
- Check firewall settings
- Try different port in `webui.py`:
```python
demo.launch(server_port=7861)  # Change port
```

#### Q: Avatar preparation fails
**A:**
- Use clear frontal face images/videos
- Recommended resolution: 512x512 to 1024x1024
- Supported formats: `.jpg`, `.png`, `.mp4`

---

### 4. Gemini Live Specific Issues

#### Q: WebSocket connection fails
**A:** 
- Verify Railway bridge is running: `wss://gemini-live-bridge-production.up.railway.app/ws`
- Check internet connection
- Ensure no firewall blocking WebSocket connections

#### Q: No audio playback
**A:** 
- Check browser audio permissions
- Verify `speaker_output` component has `autoplay=True`
- Test with different browser (Chrome recommended)

#### Q: Avatar not lip-syncing
**A:**
1. Click "🎭 Prepare Avatar" and wait for "✅ Ready"
2. Click "🔌 Connect to Gemini" and wait for "✅ Connected"
3. Ensure microphone permissions are granted
4. Check audio buffer is receiving data

#### Q: High latency / Lag
**A:**
- **Target**: <1 second end-to-end
- **Optimize**:
  - Use GPU (not CPU)
  - Reduce image resolution
  - Set `return_frame_only=True` in `inference_streaming()` for faster rendering
  - Check network speed to Railway bridge

---

### 5. Usage Tips

#### Q: How to use custom avatar?
**A:**
1. Uncheck "Use Default Avatar"
2. Upload your image/video (frontal face, clear features)
3. Adjust "Mouth Position Fix" slider if needed
4. Click "🎭 Prepare Avatar"

#### Q: How to adjust mouth position?
**A:** Use the "BBox Shift" slider:
- **Positive values** (+): Move mouth down
- **Negative values** (-): Move mouth up
- Default: 5

#### Q: Best practices for demo?
**A:**
1. **Preparation**: Always prepare avatar before connecting
2. **Connection**: Wait for "✅ Connected" status
3. **Speaking**: Speak clearly, natural pace
4. **Interruption**: Gemini 2.5 Flash handles interruptions natively - try it!
5. **Quality**: Use good microphone for best results

---

## Performance Benchmarks

| Component | Latency | VRAM Usage |
|-----------|---------|------------|
| WebSocket (Railway) | ~50ms | 0GB |
| Gemini 2.5 Flash | ~200ms | 0GB (Cloud) |
| MuseTalk Inference | ~40ms/frame | 6-8GB |
| Audio Buffer | ~200ms | <1GB |
| **Total End-to-End** | **~500ms** | **8-11GB** |

---

## System Requirements

### Minimum
- GPU: 6GB VRAM
- RAM: 8GB
- CPU: 4 cores
- Network: 10 Mbps

### Recommended
- GPU: 11GB+ VRAM (RTX 2080 Ti / RTX 3060 or better)
- RAM: 16GB
- CPU: 8 cores
- Network: 50 Mbps

---

## Troubleshooting Checklist

Before reporting issues, verify:

- [ ] Python 3.10 installed
- [ ] CUDA 11.8 installed (for GPU)
- [ ] All model weights downloaded (check file sizes)
- [ ] Models in correct folder structure
- [ ] Dependencies installed (`requirements_webui.txt`)
- [ ] FFMPEG installed
- [ ] Sufficient VRAM available
- [ ] Railway bridge is accessible
- [ ] Firewall allows WebSocket connections
- [ ] Browser has microphone permissions

---

## Getting Help

1. **Check this FAQ first**
2. **Review error messages** - most include hints
3. **Check model file sizes** - incomplete downloads are common
4. **Try with default avatar** - isolates custom image issues
5. **Report issues** with:
   - Full error message
   - Python version
   - GPU model
   - Steps to reproduce

---

## Links

- **GitHub**: [Kedreamix/Linly-Talker](https://github.com/Kedreamix/Linly-Talker)
- **Models**: [HuggingFace](https://huggingface.co/Kedreamix/Linly-Talker) | [ModelScope](https://modelscope.cn/models/Kedreamix/Linly-Talker)
- **Railway Bridge**: [gemini-live-bridge](https://gemini-live-bridge-production.up.railway.app)

---

**Last Updated**: February 2026  
**Version**: Gemini Live Integration v1.0
