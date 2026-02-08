# Optional imports - gracefully handle missing dependencies
try:
    from .SadTalker import SadTalker
    SADTALKER_AVAILABLE = True
except ImportError as e:
    SadTalker = None
    SADTALKER_AVAILABLE = False
    print(f"⚠️ SadTalker not available: {e}")

try:
    from .Wav2Lip import Wav2Lip
    WAV2LIP_AVAILABLE = True
except ImportError as e:
    Wav2Lip = None
    WAV2LIP_AVAILABLE = False
    print(f"⚠️ Wav2Lip not available: {e}")

try:
    from .Wav2Lipv2 import Wav2Lipv2
    WAV2LIPV2_AVAILABLE = True
except ImportError as e:
    Wav2Lipv2 = None
    WAV2LIPV2_AVAILABLE = False
    print(f"⚠️ Wav2Lipv2 not available: {e}")

try:
    from .NeRFTalk import NeRFTalk
    NERFTALK_AVAILABLE = True
except ImportError as e:
    NeRFTalk = None
    NERFTALK_AVAILABLE = False
    print(f"⚠️ NeRFTalk not available: {e}")

try:
    # Changed from MuseTalk to MuseTalk_RealTime to match webui.py
    from .MuseTalk import MuseTalk_RealTime 
    # Also expose as MuseTalk for backward compatibility if needed
    MuseTalk = MuseTalk_RealTime
    MUSETALK_AVAILABLE = True
except ImportError as e:
    MuseTalk_RealTime = None
    MuseTalk = None
    MUSETALK_AVAILABLE = False
    print(f"⚠️ MuseTalk not available: {e}")

# Export availability flags
__all__ = ['SadTalker', 'Wav2Lip', 'Wav2Lipv2', 'NeRFTalk', 'MuseTalk_RealTime', 'MuseTalk',
           'SADTALKER_AVAILABLE', 'WAV2LIP_AVAILABLE', 'WAV2LIPV2_AVAILABLE', 'NERFTALK_AVAILABLE', 'MUSETALK_AVAILABLE']