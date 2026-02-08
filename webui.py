import gradio as gr
import asyncio
import numpy as np
import os
import time
import sys
import warnings

# Suppress warnings for clean demo
warnings.filterwarnings('ignore')

# --- IMPORTS ---
from LLM.GeminiLive import GeminiLiveClient
from TFG.Streamer import AudioBuffer

# --- CONFIGURATION ---
# Default avatar video path (ensure this file exists!)
DEFAULT_AVATAR_VIDEO = "./Musetalk/data/video/yongen_musev.mp4" 
# Your Railway Bridge URL
WSS_URL = "wss://gemini-live-bridge-production.up.railway.app/ws"
# Default mouth opening adjustment
DEFAULT_BBOX_SHIFT = 5 

# --- GLOBAL STATE ---
# Initialize the WebSocket client
client = GeminiLiveClient(websocket_url=WSS_URL)
# Audio buffer: 200ms window is optimal for MuseTalk real-time inference
audio_buffer = AudioBuffer(sample_rate=16000, context_size_seconds=0.2) 

musetalker = None
avatar_prepared = False
current_avatar_path = None

# --- CORE FUNCTIONS ---

def init_model():
    """Lazy load the MuseTalk model only when needed to save VRAM on startup."""
    global musetalker
    if musetalker is None:
        print("🚀 Loading MuseTalk Model...")
        from TFG import MuseTalk_RealTime
        musetalker = MuseTalk_RealTime()
        musetalker.init_model()
        print("✅ MuseTalk Model Loaded")

def prepare_avatar(avatar_source, bbox_shift, use_default):
    """
    Pre-processes the avatar image/video.
    This creates the latents and coordinate cycles needed for infinite streaming.
    """
    global avatar_prepared, current_avatar_path, musetalker
    
    # 1. Initialize Model
    init_model()
    
    # 2. Reset Previous State (if any)
    if avatar_prepared:
        avatar_prepared = False
        audio_buffer.clear()
        # Reset internal model state if needed
        if hasattr(musetalker, 'input_latent_list_cycle'):
             musetalker.input_latent_list_cycle = None
        if hasattr(musetalker, 'stream_idx'):
             delattr(musetalker, 'stream_idx')

    # 3. Determine Source File
    if use_default:
        avatar_path = DEFAULT_AVATAR_VIDEO
        print("📸 Using Default Avatar")
    else:
        if avatar_source is None:
            return "❌ Error: No file uploaded for Custom Avatar"
        avatar_path = avatar_source
        print(f"📸 Using Custom Avatar: {avatar_path}")

    # 4. Run Preparation
    try:
        print(f"🎭 Preparing materials for: {os.path.basename(avatar_path)}")
        # This handles both Video (frames) and Images (single frame repeat)
        musetalker.prepare_material(avatar_path, bbox_shift)
        
        current_avatar_path = avatar_path
        avatar_prepared = True
        audio_buffer.clear() # Ensure buffer is clean for fresh start
        
        return f"✅ Ready: {os.path.basename(avatar_path)}"
    except Exception as e:
        print(f"❌ Preparation Error: {e}")
        return f"❌ Error: {str(e)}"

async def start_session():
    """Establishes the WebSocket connection to the Railway Bridge."""
    init_model()
    
    print(f"🔌 Connecting to Bridge: {WSS_URL}...")
    success = await client.connect()
    
    if success:
        return "✅ Connected to Gemini 2.5 Flash (Aoede Voice)"
    return "❌ Connection Failed - Check Railway URL"

async def process_stream(audio_data):
    """
    THE REAL-TIME LOOP (Called ~25 times per second by Gradio)
    1. Send Mic Audio -> Railway Bridge
    2. Receive Gemini Audio -> Buffer
    3. Buffer -> MuseTalk -> Video Frame
    Returns: (Video Frame, Audio Chunk)
    """
    # Initialize returns
    ret_frame = None
    ret_audio = None

    # Stop if not connected or avatar not ready
    if not client.running or not avatar_prepared:
        return None, None

    # --- 1. SEND USER AUDIO ---
    if audio_data is not None:
        sr, y = audio_data
        # Send to Railway (Client handles resampling to 16k)
        await client.send_audio(y, original_sr=sr)

    # --- 2. COLLECT GEMINI AUDIO ---
    # Drain the WebSocket queue
    new_audio_chunks = []
    while not client.output_queue.empty():
        try:
            gemini_audio_chunk = client.output_queue.get_nowait()
            # Push to Avatar Buffer
            audio_buffer.push(gemini_audio_chunk)
            # Collect for User Playback
            new_audio_chunks.append(gemini_audio_chunk)
        except asyncio.QueueEmpty:
            break

    # Format Audio for Gradio Output (if any)
    if new_audio_chunks:
        audio_concat = np.concatenate(new_audio_chunks)
        ret_audio = (16000, audio_concat)

    # --- 3. GENERATE AVATAR FRAME ---
    # Get current 200ms audio window
    current_audio_window = audio_buffer.get_window()
    
    if current_audio_window is not None:
        try:
            # Streaming Inference (Low Latency)
            ret_frame = musetalker.inference_streaming(
                audio_buffer_16k=current_audio_window,
                return_frame_only=False # Set True for faster speed (crop only)
            )
        except Exception as e:
            # Suppress print spam for frame drops
            pass

    return ret_frame, ret_audio

# --- GRADIO UI LAYOUT ---

with gr.Blocks(title="Gemini Live Avatar", theme=gr.themes.Soft()) as demo:
    
    # Header
    gr.HTML(
        """
        <div style='text-align: center; margin-bottom: 20px;'>
            <h1>⚡ Gemini Live Real-time Avatar ⚡</h1>
            <p>Powered by <b>Google Gemini 2.5 Flash</b> & <b>Linly-Talker</b></p>
        </div>
        """
    )

    with gr.Row():
        # --- LEFT COLUMN: SETTINGS ---
        with gr.Column(scale=1, variant="panel"):
            gr.Markdown("### 1. Avatar Setup")
            
            # Source Toggle
            use_default = gr.Checkbox(
                label="Use Default Avatar", 
                value=True,
                info="Uncheck to upload your own Image or Video"
            )
            
            # Custom Upload (Hidden by default)
            with gr.Group(visible=False) as custom_group:
                avatar_upload = gr.File(
                    label="Upload File",
                    file_types=["image", "video"],
                    type="filepath"
                )
                gr.Markdown("<i>Supported: .mp4, .jpg, .png (Static image will animate lips only)</i>")

            # Fine-tuning
            bbox_shift = gr.Slider(
                label="Mouth Position Fix",
                minimum=-20, maximum=20, value=5, step=1,
                info="Adjust if mouth looks misaligned (+ Down, - Up)"
            )
            
            # Prepare Button
            btn_prepare = gr.Button("🎭 Prepare Avatar", variant="secondary")
            status_prepare = gr.Textbox(label="Status", value="Waiting...", interactive=False, show_label=False)

            gr.Markdown("---")
            gr.Markdown("### 2. Connection")
            btn_connect = gr.Button("🔌 Connect to Gemini", variant="primary")
            status_connect = gr.Textbox(label="Connection", value="Disconnected", interactive=False, show_label=False)

        # --- RIGHT COLUMN: INTERACTION ---
        with gr.Column(scale=2, variant="panel"):
            gr.Markdown("### 3. Live Interaction")
            
            # The Avatar Display
            avatar_output = gr.Image(
                label="Live Stream", 
                streaming=True, 
                interactive=False,
                height=400
            )
            
            # Audio Input (Mic)
            mic_input = gr.Audio(
                sources=["microphone"], 
                type="numpy", 
                label="Your Voice (Click Record to Speak)", 
                streaming=True
            )
            
            # Hidden Speaker (Plays Gemini's Audio)
            speaker_output = gr.Audio(
                label="Gemini Voice", 
                autoplay=True, 
                streaming=True, 
                visible=False
            )

    # --- UI LOGIC & WIRING ---

    # 1. Toggle Custom Upload Visibility
    def toggle_upload(checkbox_val):
        return gr.update(visible=not checkbox_val)
    
    use_default.change(fn=toggle_upload, inputs=use_default, outputs=custom_group)

    # 2. Prepare Avatar Action
    btn_prepare.click(
        fn=prepare_avatar,
        inputs=[avatar_upload, bbox_shift, use_default],
        outputs=[status_prepare]
    )

    # 3. Connect Action
    btn_connect.click(
        fn=start_session,
        inputs=[],
        outputs=[status_connect]
    )

    # 4. The Main Streaming Loop
    # Latency Tuning: stream_every=0.04 targets ~25 FPS
    mic_input.stream(
        fn=process_stream,
        inputs=[mic_input],
        outputs=[avatar_output, speaker_output],
        time_limit=300, # 5 minute timeout safety
        stream_every=0.04
    )

# Launch
if __name__ == "__main__":
    demo.queue().launch(
        server_name="0.0.0.0", 
        server_port=7860,
        quiet=True
    )