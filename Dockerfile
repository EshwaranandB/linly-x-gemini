# 1. Use Python 3.10 (Required for stable ML libraries)
FROM python:3.10-slim

# Set working directory
WORKDIR /app

# 2. Install system dependencies
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

# 3. Upgrade pip, wheel, and setuptools
RUN pip install --no-cache-dir --upgrade pip wheel setuptools

# 4. CRITICAL: Install PyTorch 2.1.2 (Golden Version for this stack)
# We strictly use 2.1.2 to match the pre-built wheels for mmcv 2.1.0
RUN pip install --no-cache-dir \
    torch==2.1.2+cu118 \
    torchvision==0.16.2+cu118 \
    torchaudio==2.1.2+cu118 \
    --index-url https://download.pytorch.org/whl/cu118

# 5. CRITICAL FIX: Install chumpy manually
# Prevents the "No module named pip" error during mmpose install
RUN pip install --no-cache-dir --no-build-isolation chumpy

# 6. CRITICAL FIX: Install Pinned OpenMMLab Stack
# We install ALL 3 at once with strict versions to prevent auto-upgrade.
# mmcv==2.1.0  -> The base (Must be < 2.2.0)
# mmdet==3.2.0 -> Compatible with mmcv 2.1.0
# mmpose==1.2.0 -> Compatible with mmcv 2.1.0
RUN pip install --no-cache-dir openmim && \
    mim install "mmcv==2.1.0" "mmdet==3.2.0" "mmpose==1.2.0"

# 7. Install remaining dependencies
COPY requirements.txt /tmp/requirements.txt
RUN pip install --no-cache-dir -r /tmp/requirements.txt

# 8. Copy application code
COPY . /app

# 8.5 Download Models
# Make sure the script is executable and run it
RUN chmod +x /app/scripts/download_models.sh && \
    /app/scripts/download_models.sh

# 9. Setup permissions for Hugging Face Spaces
RUN mkdir -p /home/user && \
    ([ -e /home/user/app ] || ln -s /app/ /home/user/app) || true

# 10. Launch Configuration
EXPOSE 7860
ENV GRADIO_SERVER_NAME="0.0.0.0"
ENV GRADIO_SERVER_PORT=7860

# Start the Gemini Live WebUI
CMD ["python", "webui.py"]
