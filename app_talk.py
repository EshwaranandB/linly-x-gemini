import os
import random 
import gradio as gr
import warnings
from src.cost_time import calculate_time

# Make configs optional for deployment
try:
    from configs import *
except ImportError:
    ip = "0.0.0.0"
    port = 7860

# --- TFG IMPORTS (With Error Handling) ---
# We try to import everything, but prevent crashing if dependencies are missing
try:
    from TFG import SadTalker
    sadtalker_available = True
except ImportError:
    sadtalker_available = False
    print("⚠️ SadTalker not loaded (missing dependencies?)")

try:
    from TFG import Wav2Lip
    wav2lip_available = True
except ImportError:
    wav2lip_available = False
    print("⚠️ Wav2Lip not loaded")

try:
    from TFG import NeRFTalk
    nerftalk_available = True
except ImportError:
    nerftalk_available = False
    print("⚠️ NeRFTalk not loaded")

# --- NEW: GEMINI LIVE ENGINE ---
try:
    from TFG import MuseTalk_RealTime
    musetalk_available = True
except ImportError:
    musetalk_available = False
    print("⚠️ MuseTalk not loaded")

# --- TTS IMPORTS ---
try:
    from TTS import EdgeTTS
    edgetts = EdgeTTS()
except:
    edgetts = None

os.environ["GRADIO_TEMP_DIR"]= './temp'
warnings.filterwarnings("ignore")

# --- GLOBAL MODELS ---
sadtalker_model = None
wav2lip_model = None
nerftalk_model = None
musetalk_model = None

def init_sadtalker():
    global sadtalker_model
    if sadtalker_available and sadtalker_model is None:
        sadtalker_model = SadTalker(lazy_load=True)

def init_wav2lip():
    global wav2lip_model
    if wav2lip_available and wav2lip_model is None:
        wav2lip_model = Wav2Lip("checkpoints/wav2lip_gan.pth")

def init_musetalk():
    global musetalk_model
    if musetalk_available and musetalk_model is None:
        print("🚀 Loading MuseTalk RealTime Engine...")
        musetalk_model = MuseTalk_RealTime()
        musetalk_model.init_model()

@calculate_time
def TTS_response(text, voice, rate, volume, pitch, tts_method='Edge-TTS'):
    save_path = 'answer.wav'
    if tts_method == 'Edge-TTS' and edgetts:
        try:
            edgetts.predict(text, voice, rate, volume, pitch , save_path, 'answer.vtt')
        except:
            os.system(f'edge-tts --text "{text}" --voice {voice} --write-media {save_path}')
    return save_path

@calculate_time
def Talker_response(source_image, source_video, method, text, voice, rate, volume, pitch, batch_size, bbox_shift):
    
    # 1. Generate Audio first
    driven_audio = TTS_response(text, voice, rate, volume, pitch)
    
    # 2. Select Method
    video_path = None
    
    if method == 'MuseTalk (Gemini Engine)':
        if not musetalk_available: return None
        init_musetalk()
        # MuseTalk handles both Image and Video sources internally in prepare_material
        input_visual = source_video if source_video else source_image
        if input_visual is None: return None
        
        # Prepare latents (this usually happens once per avatar, but we do it here for the demo)
        musetalk_model.prepare_material(input_visual, bbox_shift)
        # Run inference (Offline mode for testing)
        video_path = musetalk_model.inference_noprepare(driven_audio, input_visual, bbox_shift, batch_size)
        if isinstance(video_path, tuple): video_path = video_path[0] # Handle return format

    elif method == 'SadTalker':
        if not sadtalker_available: return None
        init_sadtalker()
        if source_image is None: return None
        # SadTalker parameters
        pose_style = random.randint(0, 45)
        video_path = sadtalker_model.test2(source_image, driven_audio, 'crop', False, False, 
                                           batch_size, 256, pose_style, 'facevid2vid', 1, False, None, 'pose', False, 5, True)

    elif method == 'Wav2Lip':
        if not wav2lip_available: return None
        init_wav2lip()
        input_visual = source_video if source_video else source_image
        video_path = wav2lip_model.predict(input_visual, driven_audio, batch_size)

    elif method == 'NeRFTalk':
        if not nerftalk_available: return None
        if nerftalk_model is None:
            nerftalk_model = NeRFTalk()
            nerftalk_model.init_model('checkpoints/Obama_ave.pth', 'checkpoints/Obama.json')
        video_path = nerftalk_model.predict(driven_audio)

    else:
        gr.Warning(f"Method {method} not supported or not installed.")
    
    return video_path

# --- UI ---
def main():
    with gr.Blocks(title='Linly-Talker Avatar Lab', theme=gr.themes.Soft()) as inference:
        gr.HTML(
            """
            <div style='text-align: center; margin-bottom: 20px;'>
                <h1>🎭 Linly-Talker: Avatar Laboratory</h1>
                <p>Compare all avatar generation methods in one place</p>
            </div>
            """
        )
        
        with gr.Row():
            # Left: Configuration
            with gr.Column(variant='panel'):
                with gr.Tab("Input (Image/Video)"):
                    source_image = gr.Image(label='Source Image (SadTalker/MuseTalk)', type='filepath')
                    source_video = gr.Video(label="Source Video (Wav2Lip/MuseTalk)")
                
                with gr.Tab("Audio & Text"):
                    input_text = gr.Textbox(
                        label="Text to Speak", 
                        value="Hello, this is a test of the Linly Talker system.", 
                        lines=3
                    )
                    voice = gr.Dropdown(
                        edgetts.SUPPORTED_VOICE if edgetts else [], 
                        value='zh-CN-XiaoxiaoNeural', 
                        label="Voice"
                    )
                    with gr.Accordion("Audio Settings", open=False):
                        rate = gr.Slider(minimum=-100, maximum=100, value=0, step=1, label='Rate')
                        volume = gr.Slider(minimum=0, maximum=100, value=100, step=1, label='Volume')
                        pitch = gr.Slider(minimum=-100, maximum=100, value=0, step=1, label='Pitch')

                with gr.Tab("Model Settings"):
                    method = gr.Radio(
                        choices=['MuseTalk (Gemini Engine)', 'SadTalker', 'Wav2Lip', 'NeRFTalk'], 
                        value='MuseTalk (Gemini Engine)', 
                        label='Generation Method'
                    )
                    batch_size = gr.Slider(minimum=1, maximum=8, value=1, step=1, label='Batch Size')
                    bbox_shift = gr.Slider(minimum=-10, maximum=10, value=5, step=1, label='MuseTalk BBox Shift')

                submit_btn = gr.Button("🎬 Generate Video", variant='primary', size='lg')

            # Right: Output
            with gr.Column():
                output_video = gr.Video(label="Result", autoplay=True, height=500)
                gr.Markdown(
                    """
                    ### 📖 Model Guide:
                    
                    | Method | Input | Features |
                    |--------|-------|----------|
                    | **MuseTalk** | Image/Video | ⭐ Real-time engine used by Gemini Live. Best lip-sync quality. |
                    | **SadTalker** | Image Only | Generates head movement from single image. Natural expressions. |
                    | **Wav2Lip** | Video Only | High-quality lip sync. No head movement generation. |
                    | **NeRFTalk** | Audio Only | Generates Obama avatar (requires specific checkpoint). |
                    
                    ### 💡 Tips:
                    - **MuseTalk**: Best for real-time applications and Gemini Live integration
                    - **SadTalker**: Best for creating videos from photos
                    - **Wav2Lip**: Best when you have existing video footage
                    - **NeRFTalk**: Specialized for NeRF-based avatars
                    """
                )

        submit_btn.click(
            fn=Talker_response,
            inputs=[source_image, source_video, method, input_text, voice, rate, volume, pitch, batch_size, bbox_shift],
            outputs=output_video
        )

    return inference

if __name__ == "__main__":
    demo = main()
    demo.queue().launch(server_name=ip, server_port=port, debug=True, quiet=True)