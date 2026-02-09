# ⚠️ INTENTIONALLY LEFT EMPTY FOR LAZY LOADING ⚠️
#
# To prevent Out-Of-Memory (OOM - Exit Code 137) crashes on Hugging Face Spaces:
# We must NOT import heavy modules (SadTalker, MuseTalk, Wav2Lip) here.
#
# Doing so would trigger their internal imports (PyTorch, MoviePy, OpenCV) immediately
# at startup, consuming all 16GB of RAM before the user clicks anything.
#
# USAGE GUIDE:
# Instead of: from TFG import SadTalker
# Use:        from TFG.SadTalker import SadTalker (Inside your function)
#
# Example in webui.py:
# def load_sadtalker():
#     from TFG.SadTalker import SadTalker  <-- Loads strictly on demand
#     return SadTalker(...)