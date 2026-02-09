#!/bin/bash
set -e

echo "Starting Automated Model Download..."

# Install huggingface_hub if not present (just in case)
# pip install --upgrade huggingface_hub

# 1. Create Directories
mkdir -p Musetalk/models/dwpose
mkdir -p Musetalk/models/face-parsing
mkdir -p Musetalk/models/sd-vae-ft-mse
mkdir -p checkpoints
mkdir -p gfpgan/weights

# 2. Download DWPose Models (Required for pose)
echo "Downloading DWPose..."
wget -nc -O Musetalk/models/dwpose/dw-ll_ucoco_384.pth https://huggingface.co/yzd-v/DWPose/resolve/main/dw-ll_ucoco_384.pth
wget -nc -O Musetalk/models/dwpose/yolox_l.onnx https://huggingface.co/yzd-v/DWPose/resolve/main/yolox_l.onnx

# 3. Download Face Parsing Models
mkdir -p Musetalk/models/face-parse-bisent
echo "Downloading Face Parsing..."
# Use a public mirror for 79999_iter.pth since the original repo might be gated/private
# Mirror: leonelhs/faceparser (Public)
wget -nc -O Musetalk/models/face-parse-bisent/79999_iter.pth https://huggingface.co/leonelhs/faceparser/resolve/main/79999_iter.pth
wget -nc -O Musetalk/models/face-parse-bisent/resnet18-5c106cde.pth https://download.pytorch.org/models/resnet18-5c106cde.pth

# 4. Download VAE
echo "Downloading VAE..."
wget -nc -O Musetalk/models/sd-vae-ft-mse/config.json https://huggingface.co/stabilityai/sd-vae-ft-mse/resolve/main/config.json
wget -nc -O Musetalk/models/sd-vae-ft-mse/diffusion_pytorch_model.bin https://huggingface.co/stabilityai/sd-vae-ft-mse/resolve/main/diffusion_pytorch_model.bin

# 5. Download MuseTalk Checkpoints (using TMElyralab/MuseTalk)
echo "Downloading MuseTalk Checkpoints..."
# Official repo: TMElyralab/MuseTalk
huggingface-cli download TMElyralab/MuseTalk musetalk/musetalk.json --local-dir checkpoints --local-dir-use-symlinks False
huggingface-cli download TMElyralab/MuseTalk musetalk/pytorch_model.bin --local-dir checkpoints --local-dir-use-symlinks False
huggingface-cli download TMElyralab/MuseTalk musetalk/musetalk_whisper_adapter_model.bin --local-dir checkpoints --local-dir-use-symlinks False || echo "Adapter model optional/not found"

# whisper (if needed inside checkpoints/whisper)
# huggingface-cli download TMElyralab/MuseTalk whisper/tiny.pt --local-dir checkpoints/whisper --local-dir-use-symlinks False || true

# 6. GFPGAN (Optional but good to have)
echo "Downloading GFPGAN..."
wget -nc -O gfpgan/weights/detection_Resnet50_Final.pth https://github.com/xinntao/facexlib/releases/download/v0.1.0/detection_Resnet50_Final.pth
wget -nc -O gfpgan/weights/parsing_parsenet.pth https://github.com/xinntao/facexlib/releases/download/v0.2.2/parsing_parsenet.pth

echo "All models downloaded successfully!"
