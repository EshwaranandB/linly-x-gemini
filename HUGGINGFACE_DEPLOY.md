# Hugging Face Spaces Deployment Guide

## 🔐 Authentication Required

Hugging Face requires a **User Access Token** for git operations.

### Step 1: Create Access Token

1. Go to: https://huggingface.co/settings/tokens
2. Click **"New token"**
3. Settings:
   - **Name**: `linly-x-gemini-deploy`
   - **Type**: **Write** (required for pushing)
   - **Repositories**: Select `personaxgemini` or leave as "All"
4. Click **"Generate token"**
5. **Copy the token** (you won't see it again!)

### Step 2: Configure Git Credentials

#### Option A: Use Git Credential Manager (Recommended)

When you push, Git will prompt for credentials:
- **Username**: `eshwar06`
- **Password**: Paste your **access token** (not your Hugging Face password)

#### Option B: Embed Token in URL (Less Secure)

```bash
cd "d:/linly gg/Linly-Talker"

# Remove current HF remote
git remote remove hf

# Add with token embedded (replace YOUR_TOKEN)
git remote add hf https://eshwar06:YOUR_TOKEN@huggingface.co/spaces/eshwar06/personaxgemini

# Push
git push hf main
```

### Step 3: Push to Hugging Face

```bash
cd "d:/linly gg/Linly-Talker"
git push hf main
```

When prompted:
- **Username**: `eshwar06`
- **Password**: [Paste your access token]

---

## 🚀 After Successful Push

### Configure Space Settings

1. Go to: https://huggingface.co/spaces/eshwar06/personaxgemini/settings
2. **Hardware**:
   - Select: **GPU T4** (minimum) or better
   - Enable **Persistent Storage** (for model caching)
3. **SDK**: Should auto-detect Gradio 4.44.0 from README.md
4. **App File**: Should be `webui.py` (from README.md)

### Expected Build Time

- **First build**: ~10-15 minutes (downloading models)
- **Subsequent builds**: ~2-3 minutes (cached models)

---

## 📋 Quick Reference

### Space URL
https://huggingface.co/spaces/eshwar06/personaxgemini

### Token Settings
https://huggingface.co/settings/tokens

### Space Settings
https://huggingface.co/spaces/eshwar06/personaxgemini/settings

---

## 🔧 Troubleshooting

### Issue: "Authentication failed"
**Solution**: Create access token with **Write** permissions

### Issue: "Space not found"
**Solution**: Create the Space first at https://huggingface.co/new-space

### Issue: "Build failed"
**Solution**: Check logs at https://huggingface.co/spaces/eshwar06/personaxgemini/logs

---

## ✅ Deployment Checklist

- [ ] Create Hugging Face access token (Write permission)
- [ ] Configure git credentials
- [ ] Push code to Space
- [ ] Enable GPU (T4 or better)
- [ ] Enable persistent storage
- [ ] Wait for build to complete
- [ ] Test the deployed app

---

**Ready to deploy!** Create your access token and push! 🚀
