import gradio as gr
import asyncio
import numpy as np
import os
import warnings
import cv2

# --- NEW ESSENTIAL IMPORTS ---
from LLM.GeminiLive import GeminiLiveClient
from TFG.Streamer import AudioBuffer
# -----------------------------

warnings.filterwarnings('ignore')

# --- CONFIGURATION ---
DEFAULT_AVATAR = "./Musetalk/data/video/yongen_musev.mp4" 
WSS_URL = "wss://gemini-live-bridge-production.up.railway.app/ws" 
BBOX_SHIFT = 5 

# --- GLOBAL STATE ---
client = GeminiLiveClient(websocket_url=WSS_URL)
# 200ms buffer for tight lip-sync latency
audio_buffer = AudioBuffer(sample_rate=16000, context_size_seconds=0.2) 

musetalker = None
avatar_prepared = False
current_avatar_path = None

# --- INITIALIZATION & LOGIC ---

def init_model():
    """Lazy load MuseTalk to save resources"""
    global musetalker
    if musetalker is None:
        print("🚀 Loading MuseTalk Engine...")
        from TFG import MuseTalk_RealTime
        musetalker = MuseTalk_RealTime()
        musetalker.init_model()
        print("✅ MuseTalk Loaded")

def prepare_avatar(avatar_source, bbox_shift):
    """
    Pre-calculates avatar latents for real-time inference.
    Handles both Video (Looping) and Image (Static) inputs.
    """
    global avatar_prepared, current_avatar_path, musetalker
    
    init_model()
    
    # 1. Reset State
    if avatar_prepared:
        avatar_prepared = False
        audio_buffer.clear()
        if hasattr(musetalker, 'input_latent_list_cycle'):
             musetalker.input_latent_list_cycle = None
        if hasattr(musetalker, 'stream_idx'):
             delattr(musetalker, 'stream_idx')

    # 2. Validate Input
    if avatar_source is None:
        # Fallback to default if nothing provided
        if os.path.exists(DEFAULT_AVATAR):
            avatar_path = DEFAULT_AVATAR
            print(f"📸 Using Default Avatar: {avatar_path}")
        else:
            return "❌ Error: Default avatar not found and no file uploaded."
    else:
        avatar_path = avatar_source
        print(f"📸 Using Custom Avatar: {avatar_path}")

    # 3. Process
    try:
        print("🎭 Processing Avatar Materials...")
        musetalker.prepare_material(avatar_path, bbox_shift)
        
        current_avatar_path = avatar_path
        avatar_prepared = True
        audio_buffer.clear()
        return f"✅ Ready! Using: {os.path.basename(avatar_path)}"
    except Exception as e:
        print(f"❌ Error: {e}")
        return f"❌ Preparation Failed: {str(e)}"

async def start_session():
    """Connects to the Railway Bridge"""
    init_model()
    print(f"🔌 Dialing {WSS_URL}...")
    success = await client.connect()
    if success:
        return "✅ Gemini Connected (Listening...)"
    return "❌ Connection Failed"

async def process_stream(audio_data):
    """
    The Heartbeat Loop:
    Mic -> Bridge -> Gemini -> Audio -> MuseTalk -> Video Frame
    """
    ret_frame = None
    ret_audio = None

    if not client.running or not avatar_prepared:
        return None, None

    # 1. Send User Audio
    if audio_data is not None:
        sr, y = audio_data
        await client.send_audio(y, original_sr=sr)

    # 2. Receive Gemini Audio
    new_chunks = []
    while not client.output_queue.empty():
        try:
            chunk = client.output_queue.get_nowait()
            audio_buffer.push(chunk)
            new_chunks.append(chunk)
        except asyncio.QueueEmpty:
            break
            
    # 3. Playback Audio (if any)
    if new_chunks:
        # Concatenate for Gradio Output (16kHz)
        ret_audio = (16000, np.concatenate(new_chunks))

    # 4. Generate Video Frame
    current_window = audio_buffer.get_window()
    if current_window is not None:
        try:
            ret_frame = musetalker.inference_streaming(
                audio_buffer_16k=current_window,
                return_frame_only=False 
            )
        except:
            pass # Skip dropped frames to maintain sync

    return ret_frame, ret_audio

# --- GRADIO UI ---
def main():
    with gr.Blocks(title="Linly-Talker Multi-Turn", theme=gr.themes.Soft()) as inference:
        
        gr.Markdown(
            """
            # 🗣️ Linly-Talker Multi-Turn Interaction
            **Powered by Gemini Live** | Continuous Conversation Mode
            """
        )

        with gr.Row():
            # --- Left Column: The Avatar ---
            with gr.Column(scale=3):
                avatar_output = gr.Image(
                    label="Digital Human", 
                    streaming=True, 
                    interactive=False, 
                    height=500
                )
                
                # Hidden audio output for browser playback
                speaker_output = gr.Audio(
                    label="Gemini Voice", 
                    autoplay=True, 
                    streaming=True, 
                    visible=False
                )

            # --- Right Column: Controls & Setup ---
            with gr.Column(scale=2, variant="panel"):
                gr.Markdown("### ⚙️ Configuration")
                
                with gr.Tab("Avatar"):
                    avatar_upload = gr.File(
                        label="Upload Image/Video (Optional)",
                        file_types=["image", "video"],
                        type="filepath"
                    )
                    bbox_shift = gr.Slider(
                        label="Mouth Alignment (BBox Shift)", 
                        minimum=-20, maximum=20, value=5, step=1
                    )
                    btn_prepare = gr.Button("1. Load Avatar", variant="secondary")
                    status_prepare = gr.Textbox(label="Status", value="Idle", interactive=False)

                with gr.Tab("Connection"):
                    btn_connect = gr.Button("2. Connect to Gemini", variant="primary")
                    status_connect = gr.Textbox(label="Status", value="Disconnected", interactive=False)

                gr.Markdown("### 🎙️ Conversation")
                mic_input = gr.Audio(
                    sources=["microphone"], 
                    type="numpy", 
                    label="Microphone Input", 
                    streaming=True
                )
                gr.Markdown("*Speak naturally. You can interrupt the avatar at any time.*")

        # --- Event Wiring ---
        
        # 1. Prepare Avatar
        btn_prepare.click(
            fn=prepare_avatar,
            inputs=[avatar_upload, bbox_shift],
            outputs=[status_prepare]
        )

        # 2. Connect
        btn_connect.click(
            fn=start_session,
            inputs=[],
            outputs=[status_connect]
        )

        # 3. Streaming Loop
        mic_input.stream(
            fn=process_stream,
            inputs=[mic_input],
            outputs=[avatar_output, speaker_output],
            stream_every=0.04, # 25 FPS
            time_limit=300
        )

    return inference

if __name__ == "__main__":
    demo = main()
    demo.queue().launch(
        server_name="0.0.0.0", 
        server_port=7860,
        quiet=True
    )