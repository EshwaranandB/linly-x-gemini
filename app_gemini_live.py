import gradio as gr
import asyncio
import numpy as np
import os
import time
from LLM.GeminiLive import GeminiLiveClient
from TFG.Streamer import AudioBuffer

# --- CONFIGURATION ---
DEFAULT_AVATAR_VIDEO = "./Musetalk/data/video/yongen_musev.mp4" 
WSS_URL = "wss://gemini-live-bridge-production.up.railway.app/ws"
BBOX_SHIFT = 5 

# --- GLOBAL STATE ---
client = GeminiLiveClient(websocket_url=WSS_URL)
audio_buffer = AudioBuffer(sample_rate=16000, context_size_seconds=0.2) 
musetalk_model = None
avatar_prepared = False
current_avatar_path = None

# --- INITIALIZATION ---
def init_model():
    global musetalk_model
    if musetalk_model is None:
        print("🚀 Loading MuseTalk Model...")
        from TFG import MuseTalk_RealTime
        musetalk_model = MuseTalk_RealTime()
        musetalk_model.init_model()
        print("✅ MuseTalk Loaded")

def prepare_avatar(avatar_source, bbox_shift, use_default):
    """Prepare avatar materials before streaming"""
    global avatar_prepared, current_avatar_path
    
    # Reset if previously prepared
    if avatar_prepared:
        avatar_prepared = False
        if musetalk_model:
            musetalk_model.input_latent_list_cycle = None
            if hasattr(musetalk_model, 'stream_idx'):
                delattr(musetalk_model, 'stream_idx')
    
    init_model()
    
    # Determine which avatar to use
    if use_default:
        avatar_path = DEFAULT_AVATAR_VIDEO
        print("📸 Using default avatar")
    else:
        if avatar_source is None:
            return "❌ Please upload an avatar image/video or use default"
        avatar_path = avatar_source
        print(f"📸 Using custom avatar: {avatar_path}")
    
    if musetalk_model:
        try:
            print("🎭 Preparing Avatar Materials...")
            musetalk_model.prepare_material(avatar_path, bbox_shift)
            current_avatar_path = avatar_path
            avatar_prepared = True
            print("✅ Avatar Ready")
            return f"✅ Avatar Prepared: {os.path.basename(avatar_path)}"
        except Exception as e:
            print(f"❌ Error preparing avatar: {e}")
            return f"❌ Error: {str(e)}"
    
    return "⚠️ Model not loaded"

# --- CORE STREAMING LOGIC ---
async def start_session():
    """Connects to Gemini Bridge"""
    init_model()
    success = await client.connect()
    if success:
        return "✅ Connected to Gemini Live (Aoede Voice)"
    return "❌ Connection Failed"

async def process_audio_stream(audio_data):
    """
    LOW-LATENCY STREAMING LOOP
    Returns: (Video Frame, Audio Chunk)
    """
    # Initialize returns
    ret_frame = None
    ret_audio = None

    if not client.running or not avatar_prepared:
        return None, None

    # --- 1. SEND USER AUDIO ---
    if audio_data is not None:
        sr, y = audio_data
        # Send to Railway
        await client.send_audio(y, original_sr=sr)

    # --- 2. COLLECT GEMINI AUDIO ---
    # We capture NEW audio chunks to play back to the user
    new_audio_chunks = []
    
    while not client.output_queue.empty():
        try:
            # Get chunk from Gemini
            gemini_audio_chunk = client.output_queue.get_nowait()
            
            # A. Push to Buffer (for Avatar Animation)
            audio_buffer.push(gemini_audio_chunk)
            
            # B. Collect for Playback (for User Speakers)
            new_audio_chunks.append(gemini_audio_chunk)
            
        except asyncio.QueueEmpty:
            break

    # Prepare Audio Output (if we got any new audio)
    if new_audio_chunks:
        # Concatenate all new chunks
        audio_concat = np.concatenate(new_audio_chunks)
        # Gradio Audio output expects (sample_rate, numpy_array)
        # We know Gemini client resamples to 16000
        ret_audio = (16000, audio_concat)

    # --- 3. GENERATE AVATAR FRAME ---
    # Get the current window (context) for the avatar to pronounce
    current_audio_window = audio_buffer.get_window()
    
    if current_audio_window is not None:
        try:
            # Generate 1 Frame
            ret_frame = musetalk_model.inference_streaming(
                audio_buffer_16k=current_audio_window,
                return_frame_only=False  # Full blending mode
            )
        except Exception as e:
            print(f"❌ Streaming Inference Error: {e}")
            import traceback
            traceback.print_exc()

    # Return both Video and Audio
    return ret_frame, ret_audio

# --- GRADIO UI ---
with gr.Blocks(title="Linly-Talker + Gemini Live", theme=gr.themes.Soft()) as demo:
    gr.Markdown(
        """
        # ⚡ Linly-Talker x Gemini Live (STREAMING)
        **Real-time AI Avatar** | Powered by Gemini 2.5 Flash & MuseTalk
        """
    )
    
    with gr.Row():
        with gr.Column():
            gr.Markdown("### 1. Avatar Setup")
            
            # Avatar source selection
            use_default_avatar = gr.Checkbox(
                label="Use Default Avatar",
                value=True,
                info="Uncheck to upload your own image/video"
            )
            
            with gr.Group() as custom_avatar_group:
                gr.Markdown("**Upload Custom Avatar** (Image or Video)")
                avatar_upload = gr.File(
                    label="Upload Image/Video",
                    file_types=["image", "video"],
                    type="filepath"
                )
                gr.Markdown("💡 *Tip: Use a clear frontal face photo or short video*")
            
            # BBox shift control
            bbox_shift_input = gr.Slider(
                label="BBox Shift",
                minimum=-20,
                maximum=20,
                value=BBOX_SHIFT,
                step=1,
                info="Adjust mouth position (+ = down, - = up)"
            )
            
            btn_prepare = gr.Button("🎭 Prepare Avatar", variant="secondary", size="lg")
            prepare_status = gr.Textbox(label="Status", value="Not Prepared", interactive=False)
        
        with gr.Column():
            gr.Markdown("### 2. Connect")
            btn_connect = gr.Button("🔌 Connect to Bridge", variant="primary")
            connection_status = gr.Textbox(label="Status", value="Disconnected", interactive=False)

    gr.Markdown("### 3. Live Conversation")
    with gr.Row():
        # Input Microphone
        mic_input = gr.Audio(sources=["microphone"], type="numpy", label="Your Voice", streaming=True)
        
        # Output Avatar (Video)
        avatar_output = gr.Image(label="Live Avatar", streaming=True, interactive=False)
        
        # Output Audio (Hidden Speaker) - This plays Gemini's voice!
        speaker_output = gr.Audio(label="Gemini Voice", autoplay=True, streaming=True, visible=False)

    # --- WIRING ---
    
    # Toggle custom avatar upload visibility
    def toggle_custom_upload(use_default):
        return gr.update(visible=not use_default)
    
    use_default_avatar.change(
        fn=toggle_custom_upload,
        inputs=[use_default_avatar],
        outputs=[custom_avatar_group]
    )
    
    # Prepare avatar
    btn_prepare.click(
        prepare_avatar,
        inputs=[avatar_upload, bbox_shift_input, use_default_avatar],
        outputs=[prepare_status]
    )
    
    # Connect to bridge
    btn_connect.click(start_session, inputs=[], outputs=[connection_status])
    
    # THE STREAM LOOP
    mic_input.stream(
        fn=process_audio_stream,
        inputs=[mic_input],
        outputs=[avatar_output, speaker_output], # Update both Image and Audio
        time_limit=300, 
        stream_every=0.04 # 25 FPS target
    )

if __name__ == "__main__":
    demo.queue().launch(server_name="0.0.0.0", server_port=7860)
