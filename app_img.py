import gradio as gr
import asyncio
import numpy as np
import os
import warnings
import cv2

# --- NEW IMPORTS ---
from LLM.GeminiLive import GeminiLiveClient
from TFG.Streamer import AudioBuffer
# -------------------

warnings.filterwarnings('ignore')

# --- CONFIGURATION ---
WSS_URL = "wss://gemini-live-bridge-production.up.railway.app/ws" # Railway URL
gemini_client = GeminiLiveClient(websocket_url=WSS_URL)
gemini_audio_buffer = AudioBuffer(sample_rate=16000, context_size_seconds=0.2)
musetalker = None
avatar_prepared = False
current_avatar_path = None

# --- INITIALIZATION ---
def init_model():
    global musetalker
    if musetalker is None:
        print("🚀 Loading MuseTalk Model...")
        from TFG import MuseTalk_RealTime
        musetalker = MuseTalk_RealTime()
        musetalker.init_model()
        print("✅ MuseTalk Model Loaded")

def prepare_avatar(image_path, bbox_shift):
    """
    Prepare a static image for streaming.
    MuseTalk treats it as a single-frame video loop.
    """
    global avatar_prepared, current_avatar_path, musetalker
    
    # 1. Load Model
    init_model()
    
    # 2. Reset
    if avatar_prepared:
        avatar_prepared = False
        gemini_audio_buffer.clear()
        if hasattr(musetalker, 'input_latent_list_cycle'):
             musetalker.input_latent_list_cycle = None
        if hasattr(musetalker, 'stream_idx'):
             delattr(musetalker, 'stream_idx')

    if image_path is None:
        return "❌ Please upload an image first."

    # 3. Process Image
    try:
        print(f"🖼️ Processing Image Avatar: {image_path}")
        musetalker.prepare_material(image_path, bbox_shift)
        current_avatar_path = image_path
        avatar_prepared = True
        gemini_audio_buffer.clear()
        return "✅ Ready! Image loaded successfully."
    except Exception as e:
        print(f"❌ Error: {e}")
        return f"❌ Error: {str(e)}"

async def start_session():
    """Connect to Gemini Live"""
    init_model()
    if not avatar_prepared:
        return "⚠️ Please prepare an avatar first."
        
    print(f"🔌 Connecting to {WSS_URL}...")
    success = await gemini_client.connect()
    if success:
        return "✅ Connected to Gemini Live"
    return "❌ Connection Failed"

async def process_stream(audio_data):
    """
    Real-time Streaming Loop
    Mic -> Railway -> Gemini -> Buffer -> MuseTalk -> Image Frame
    """
    ret_frame = None
    ret_audio = None

    if not gemini_client.running or not avatar_prepared:
        return None, None

    # 1. Send Audio
    if audio_data is not None:
        sr, y = audio_data
        await gemini_client.send_audio(y, original_sr=sr)

    # 2. Receive Audio
    new_chunks = []
    while not gemini_client.output_queue.empty():
        try:
            chunk = gemini_client.output_queue.get_nowait()
            gemini_audio_buffer.push(chunk)
            new_chunks.append(chunk)
        except asyncio.QueueEmpty:
            break
            
    if new_chunks:
        ret_audio = (16000, np.concatenate(new_chunks))

    # 3. Generate Frame
    current_window = gemini_audio_buffer.get_window()
    if current_window is not None:
        try:
            ret_frame = musetalker.inference_streaming(
                audio_buffer_16k=current_window,
                return_frame_only=False # Full image with background
            )
        except:
            pass

    return ret_frame, ret_audio

# --- UI ---
def main():
    with gr.Blocks(title="Gemini Live Image Avatar", theme=gr.themes.Soft()) as demo:
        gr.HTML(
            """
            <div style='text-align: center; margin-bottom: 20px;'>
                <h1>🖼️ Gemini Live - Talking Photo</h1>
                <p>Upload any image and bring it to life with AI conversation</p>
            </div>
            """
        )
        
        with gr.Row():
            with gr.Column():
                gr.Markdown("### 1. Upload Photo")
                image_input = gr.Image(
                    label="Source Image", 
                    type="filepath", 
                    sources=["upload"],
                    height=300
                )
                bbox_shift = gr.Slider(
                    label="Mouth Position (BBox Shift)", 
                    minimum=-20, 
                    maximum=20, 
                    value=0, 
                    step=1,
                    info="Adjust if mouth looks misaligned (+ Down, - Up)"
                )
                btn_prepare = gr.Button("🎭 Prepare Avatar", variant="secondary", size="lg")
                status = gr.Textbox(label="Status", value="Waiting...", interactive=False, show_label=False)
            
            with gr.Column():
                gr.Markdown("### 2. Connect")
                btn_connect = gr.Button("🔌 Connect to Gemini", variant="primary", size="lg")
                conn_status = gr.Textbox(label="Connection", value="Disconnected", interactive=False, show_label=False)

        gr.Markdown("### 3. Live Conversation")
        with gr.Row():
            mic = gr.Audio(
                sources=["microphone"], 
                type="numpy", 
                streaming=True, 
                label="🎤 Your Voice"
            )
            avatar_out = gr.Image(
                label="🎭 Live Avatar", 
                streaming=True, 
                interactive=False,
                height=400
            )
            speaker = gr.Audio(
                label="Gemini Audio", 
                streaming=True, 
                autoplay=True, 
                visible=False
            )

        # Wiring
        btn_prepare.click(prepare_avatar, inputs=[image_input, bbox_shift], outputs=[status])
        btn_connect.click(start_session, inputs=[], outputs=[conn_status])
        
        mic.stream(
            fn=process_stream,
            inputs=[mic],
            outputs=[avatar_out, speaker],
            time_limit=300,
            stream_every=0.04
        )

    return demo

if __name__ == "__main__":
    demo = main()
    demo.queue().launch(server_name="0.0.0.0", server_port=7860, quiet=True)