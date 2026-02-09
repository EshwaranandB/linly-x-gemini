import gradio as gr
import asyncio
import numpy as np
import os
import time
import sys
import warnings

# Suppress warnings for clean demo
warnings.filterwarnings('ignore')

# --- CONFIGURATION ---
# Default avatar video path (ensure this file exists!)
DEFAULT_AVATAR_VIDEO = "./Musetalk/data/video/yongen_musev.mp4" 
# Your Railway Bridge URL
WSS_URL = "wss://gemini-live-service-production.up.railway.app/ws"
# Default mouth opening adjustment
DEFAULT_BBOX_SHIFT = 5 

# --- LAZY GLOBAL STATE ---
# We initialize these as None to save RAM at startup
client = None
audio_buffer = None
musetalker = None
avatar_prepared = False
current_avatar_path = None

# --- CORE FUNCTIONS ---

def init_audio_system():
    """Initialize AudioBuffer and Gemini Client only when needed."""
    global client, audio_buffer
    
    if client is None:
        # Import here to avoid loading network libs at startup
        from LLM.GeminiLive import GeminiLiveClient
        client = GeminiLiveClient(websocket_url=WSS_URL)
        
    if audio_buffer is None:
        # Import directly from submodule to avoid TFG/__init__.py trigger
        from TFG.Streamer import AudioBuffer
        audio_buffer = AudioBuffer(sample_rate=16000, context_size_seconds=0.2)

def init_model():
    """Lazy load the MuseTalk model only when needed to save VRAM on startup."""
    global musetalker
    if musetalker is None:
        print("🚀 Loading MuseTalk Model...")
        # CRITICAL: Import directly from file to bypass package init
        from TFG.MuseTalk import MuseTalk_RealTime
        musetalker = MuseTalk_RealTime()
        musetalker.init_model()
        print("✅ MuseTalk Model Loaded")
    return musetalker

def prepare_avatar(avatar_source, bbox_shift, use_default):
    """
    Pre-processes the avatar image/video.
    This creates the latents and coordinate cycles needed for infinite streaming.
    """
    global avatar_prepared, current_avatar_path
    
    # 1. Initialize Model
    model = init_model()
    if model is None:
        return "❌ Model failed to load (Check logs)"
    
    # 2. Initialize Audio System
    init_audio_system()
    
    # 3. Reset Previous State (if any)
    if avatar_prepared:
        avatar_prepared = False
        if audio_buffer: audio_buffer.clear()
        # Reset internal model state if needed
        if hasattr(model, 'input_latent_list_cycle'):
             model.input_latent_list_cycle = None
        if hasattr(model, 'stream_idx'):
             delattr(model, 'stream_idx')

    # 4. Determine Source File
    if use_default:
        avatar_path = DEFAULT_AVATAR_VIDEO
        print("📸 Using Default Avatar")
    else:
        if avatar_source is None:
            return "❌ Error: No file uploaded for Custom Avatar"
        avatar_path = avatar_source
        print(f"📸 Using Custom Avatar: {avatar_path}")

    # 5. Run Preparation
    try:
        print(f"🎭 Preparing materials for: {os.path.basename(avatar_path)}")
        # This handles both Video (frames) and Images (single frame repeat)
        model.prepare_material(avatar_path, bbox_shift)
        
        current_avatar_path = avatar_path
        avatar_prepared = True
        if audio_buffer: audio_buffer.clear() # Ensure buffer is clean for fresh start
        
        return f"✅ Ready: {os.path.basename(avatar_path)}"
    except Exception as e:
        print(f"❌ Preparation Error: {e}")
        return f"❌ Error: {str(e)}"

async def start_session():
    """Establishes the WebSocket connection to the Railway Bridge."""
    init_audio_system()
    
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
    
    # Ensure systems are initialized
    init_audio_system()

    # Stop if not connected or avatar not ready
    if not client or not client.running or not avatar_prepared or not musetalker:
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
                avatar_image_path=current_avatar_path,
                return_frame_only=False # Set True for faster speed (crop only)
            )
        except Exception as e:
            # Suppress print spam for frame drops
            pass

    return ret_frame, ret_audio

# --- GRADIO UI LAYOUT ---

with gr.Blocks(title="Linly-X-Gemini", theme=gr.themes.Soft()) as demo:
    
    # Header
    gr.HTML(
        """
        <div style='text-align: center; margin-bottom: 20px;'>
            <h1>🎭 Linly-X-Gemini</h1>
            <p>Real-time AI Avatar powered by Gemini 2.5 Flash</p>
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