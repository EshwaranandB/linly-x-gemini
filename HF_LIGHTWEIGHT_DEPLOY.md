# Hugging Face Deployment - Large File Issue

## Problem
Repository size: 93MB  
Hugging Face limit: Smooth uploads for repos <50MB  
Issue: Large files in git history causing timeout

## Solution: Create Lightweight Deployment Branch

Instead of cleaning git history (complex), create a fresh deployment branch with only essential files.

### Step 1: Create Deployment Branch

```bash
cd "d:/linly gg/Linly-Talker"

# Create orphan branch (no history)
git checkout --orphan hf-deploy

# Remove all large video files
rm -rf Musetalk/data/video/*.mp4
rm -rf examples/
rm -rf GPT_SoVITS/
rm -rf results/
rm -rf src/flagged/

# Keep only one small default video
# (Download a small one or use existing small file)

# Add all files
git add .

# Commit
git commit -m "Initial Hugging Face deployment"

# Force push to HF
git push hf hf-deploy:main --force
```

### Step 2: Alternative - Manual Space Creation

If git push continues to fail, use Hugging Face web interface:

1. Go to: https://huggingface.co/spaces/eshwar06/personaxgemini/files
2. Click "Add file" → "Upload files"
3. Upload only essential files:
   - `webui.py`
   - `app.py`
   - `README.md`
   - `requirements.txt`
   - `LLM/` folder
   - `TFG/` folder
   - `configs.py`
   - `.gitignore`

### Step 3: Download Models at Runtime

Update code to download default avatar at runtime instead of including in repo:

```python
# In webui.py
import requests

DEFAULT_AVATAR_URL = "https://github.com/YOUR_REPO/releases/download/v1.0/default_avatar.mp4"

def download_default_avatar():
    if not os.path.exists("./default_avatar.mp4"):
        response = requests.get(DEFAULT_AVATAR_URL)
        with open("./default_avatar.mp4", "wb") as f:
            f.write(response.content)
```

## Recommended Approach

**Use orphan branch** - cleanest solution, removes all git history.

```bash
git checkout --orphan hf-deploy
git rm -rf Musetalk/data/video/
git rm -rf examples/
git rm -rf GPT_SoVITS/
git add .
git commit -m "Lightweight HF deployment"
git push hf hf-deploy:main --force
```

This will create a fresh repository without large files!
