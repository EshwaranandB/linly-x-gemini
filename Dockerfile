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
# If we use "latest", MMCV tries to compile from source and fails.
RUN pip install --no-cache-dir \
    torch==2.4.1+cu118 \
    torchvision==0.19.1+cu118 \
    torchaudio==2.4.1+cu118 \
    --index-url https://download.pytorch.org/whl/cu118

# 5. Install MMCV and MMPOSE via MIM
# Since we have a compatible PyTorch version now, this will download a .whl file
# instead of compiling, avoiding the pkg_resources error.
RUN pip install --no-cache-dir openmim && \
    mim install "mmcv>=2.1.0" && \
    mim install "mmpose>=1.0.0"

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
