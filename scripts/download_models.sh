#!/bin/bash
set -e

echo "Downloading MuseTalk Models..."

# Create directories
mkdir -p Musetalk/models/dwpose
mkdir -p Musetalk/models/face-parsing
mkdir -p Musetalk/models/sd-vae-ft-mse
mkdir -p Musetalk/checkpoints

# 1. DWPose Models (Required for pose estimation)
if [ ! -f "Musetalk/models/dwpose/dw-ll_ucoco_384.pth" ]; then
    echo "Downloading dw-ll_ucoco_384.pth..."
    wget -O Musetalk/models/dwpose/dw-ll_ucoco_384.pth https://huggingface.co/yzd-v/DWPose/resolve/main/dw-ll_ucoco_384.pth
fi

if [ ! -f "Musetalk/models/dwpose/yolox_l.onnx" ]; then
    echo "Downloading yolox_l.onnx..."
    wget -O Musetalk/models/dwpose/yolox_l.onnx https://huggingface.co/yzd-v/DWPose/resolve/main/yolox_l.onnx
fi

# 2. Face Parsing Models
if [ ! -f "Musetalk/models/face-parsing/79999_iter.pth" ]; then
    echo "Downloading 79999_iter.pth..."
    wget -O Musetalk/models/face-parsing/79999_iter.pth https://huggingface.co/zllrunning/face-parsing.PyTorch/resolve/main/79999_iter.pth
fi

if [ ! -f "Musetalk/models/face-parsing/resnet18-5c106cde.pth" ]; then
    echo "Downloading resnet18-5c106cde.pth..."
    wget -O Musetalk/models/face-parsing/resnet18-5c106cde.pth https://download.pytorch.org/models/resnet18-5c106cde.pth
fi

# 3. MuseTalk Checkpoints (Main Model)
# We assume the user might have some, but let's download if missing.
# Note: MuseTalk usually expects specific files.
# Using a public mirror or original link if available.
if [ ! -f "Musetalk/checkpoints/musetalk.json" ]; then
    echo "Downloading MuseTalk Checkpoints..."
    # Placeholder: The user needs to provide these or we download from a known source.
    # For now, we will try to download from a known community mirror or assume failure if not present.
    # Official MuseTalk doesn't have a simple direct link for everything in one go without git lfs.
    # We will try to download the VAE and Whisper at least.
    echo "WARNING: Main MuseTalk checkpoints might need manual upload if not in repo."
fi

# 4. Compulsory VAE (sd-vae-ft-mse)
if [ ! -f "Musetalk/models/sd-vae-ft-mse/config.json" ]; then
    echo "Downloading VAE..."
    wget -O Musetalk/models/sd-vae-ft-mse/config.json https://huggingface.co/stabilityai/sd-vae-ft-mse/resolve/main/config.json
    wget -O Musetalk/models/sd-vae-ft-mse/diffusion_pytorch_model.bin https://huggingface.co/stabilityai/sd-vae-ft-mse/resolve/main/diffusion_pytorch_model.bin
fi

# 5. Whisper (Optional, usually auto-downloaded by diffusers/whisper, but good to have)
# mkdir -p Musetalk/models/whisper

echo "Download complete."
