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

# 4. CRITICAL: Install Specific PyTorch Version (2.4.1)
# We pin this version because MMCV has pre-built wheels for it.
RUN pip install --no-cache-dir \
    torch==2.4.1+cu118 \
    torchvision==0.19.1+cu118 \
    torchaudio==2.4.1+cu118 \
    --index-url https://download.pytorch.org/whl/cu118

# 5. CRITICAL FIX: Install chumpy manually
# mmpose requires chumpy, but chumpy's installer is broken in modern pip.
# We must use --no-build-isolation to fix the "No module named pip" error.
RUN pip install --no-cache-dir --no-build-isolation chumpy

# 6. Install MMCV, MMPOSE, and MMDET via MIM
# Now that PyTorch and Chumpy are ready, this will run smoothly.
# mmpose requires chumpy (installed above)
# mmdet is required for MuseTalk's face detection
# mmdet requires mmcv<2.2.0
RUN pip install --no-cache-dir openmim && \
    mim install "mmcv>=2.1.0,<2.2.0" && \
    mim install "mmpose>=1.0.0" && \
    mim install "mmdet>=3.0.0"

# 7. Install remaining dependencies
COPY requirements.txt /tmp/requirements.txt
RUN pip install --no-cache-dir -r /tmp/requirements.txt

# 8. Copy application code
COPY . /app

# 9. Setup permissions for Hugging Face Spaces
RUN mkdir -p /home/user && \
    ([ -e /home/user/app ] || ln -s /app/ /home/user/app) || true

# 10. Launch Configuration
EXPOSE 7860
ENV GRADIO_SERVER_NAME="0.0.0.0"
ENV GRADIO_SERVER_PORT=7860

# Start the Gemini Live WebUI
CMD ["python", "webui.py"]
