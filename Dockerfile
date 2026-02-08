# 1. Use Python 3.10 (Required for stable mmcv/basicsr wheels)
FROM python:3.10-slim

# Set working directory
WORKDIR /app

# 2. Install system dependencies
# libgl1/libsm6 for OpenCV, ffmpeg for audio, build-essential for compiling basicsr
RUN apt-get update && apt-get install -y \
    git \
    git-lfs \
    ffmpeg \
    libsm6 \
    libxext6 \
    cmake \
    rsync \
    libgl1 \
    build-essential \
    && rm -rf /var/lib/apt/lists/* \
    && git lfs install

# 3. Upgrade pip and setuptools (CRITICAL for mmcv)
RUN pip install --no-cache-dir --upgrade pip setuptools==70.0.0 wheel

# 4. CRITICAL FIX: Install PyTorch FIRST
# basicsr will CRASH if torch is not found during its installation.
# Using latest PyTorch with CUDA 11.8 support
RUN pip install --no-cache-dir \
    torch \
    torchvision \
    torchaudio \
    --index-url https://download.pytorch.org/whl/cu118

# 5. Install MMCV via MIM (after PyTorch and with upgraded setuptools)
# Must be done after PyTorch but before requirements.txt
RUN pip install --no-cache-dir openmim && \
    mim install "mmcv>=2.1.0"

# 6. Install remaining dependencies
COPY requirements.txt /tmp/requirements.txt
RUN pip install --no-cache-dir -r /tmp/requirements.txt

# 7. Copy application code
COPY . /app

# 8. Setup permissions for Hugging Face Spaces
RUN mkdir -p /home/user && \
    ([ -e /home/user/app ] || ln -s /app/ /home/user/app) || true

# 9. Launch Configuration
EXPOSE 7860
ENV GRADIO_SERVER_NAME="0.0.0.0"
ENV GRADIO_SERVER_PORT=7860

# Start the Gemini Live WebUI
CMD ["python", "webui.py"]
