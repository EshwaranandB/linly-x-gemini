import gradio as gr
import os
import random
import warnings
from src.cost_time import calculate_time

# Make configs optional for deployment
try:
    from configs import *
except ImportError:
    ip = "0.0.0.0"
    port = 7860

# --- NEW GEMINI LIVE IMPORTS ---
try:
    from LLM.GeminiLive import GeminiLiveClient
    from TFG.Streamer import AudioBuffer
    from TFG import MuseTalk_RealTime
    gemini_available = True
except ImportError:
    gemini_available = False
    print("⚠️ Gemini Live modules not found. Real-time mode disabled.")

# --- LEGACY IMPORTS (With Safety Checks) ---
try:
    from TFG import SadTalker
    sadtalker = SadTalker(lazy_load=True)
except:
    sadtalker = None

try:
    from ASR import WhisperASR
    asr = WhisperASR('base')
except:
    asr = None

try:
    from TTS import EdgeTTS
    edgetts = EdgeTTS()
except:
    edgetts = None

try:
    from LLM import LLM
    llm = LLM(mode='offline').init_model('Qwen', 'Qwen/Qwen-1_8B-Chat')
except:
    llm = None

os.environ["GRADIO_TEMP_DIR"] = './temp'
warnings.filterwarnings("ignore")

# --- CONFIGURATION ---
WSS_URL = "wss://gemini-live-bridge-production.up.railway.app/ws"
DEFAULT_AVATAR = "./Musetalk/data/video/yongen_musev.mp4"

# --- GLOBAL STATE ---
if gemini_available:
    client = GeminiLiveClient(websocket_url=WSS_URL)
    audio_buffer = AudioBuffer(sample_rate=16000, context_size_seconds=0.2)
    musetalker = None
    avatar_prepared = False
    current_avatar_path = None

# --- GEMINI LIVE LOGIC ---
async def start_session():
    """Connect to Gemini Live"""
    global musetalker
    if not gemini_available: return "❌ Module Missing"
    
    if musetalker is None:
        musetalker = MuseTalk_RealTime()
        musetalker.init_model()
        
    print(f"🔌 Connecting to {WSS_URL}...")
    success = await client.connect()
    return "✅ Connected" if success else "❌ Connection Failed"

def prepare_avatar(avatar_source, bbox_shift):
    """Prepare Avatar for Streaming"""
    global avatar_prepared, current_avatar_path, musetalker
    if not gemini_available: return "❌ Module Missing"
    
    if musetalker is None:
        musetalker = MuseTalk_RealTime()
        musetalker.init_model()

    if avatar_source is None:
        avatar_path = DEFAULT_AVATAR
    else:
        avatar_path = avatar_source

    try:
        musetalker.prepare_material(avatar_path, bbox_shift)
        current_avatar_path = avatar_path
        avatar_prepared = True
        audio_buffer.clear()
        return "✅ Avatar Ready"
    except Exception as e:
        return f"❌ Error: {str(e)}"

async def process_stream(audio_data):
    """Real-time Loop"""
    if not gemini_available or not client.running or not avatar_prepared:
        return None, None

    if audio_data is not None:
        sr, y = audio_data
        await client.send_audio(y, original_sr=sr)

    import numpy as np
    import asyncio
    new_chunks = []
    while not client.output_queue.empty():
        try:
            chunk = client.output_queue.get_nowait()
            audio_buffer.push(chunk)
            new_chunks.append(chunk)
        except asyncio.QueueEmpty:
            break
            
    ret_audio = (16000, np.concatenate(new_chunks)) if new_chunks else None
    
    current_window = audio_buffer.get_window()
    ret_frame = None
    if current_window is not None:
        try:
            ret_frame = musetalker.inference_streaming(current_window, return_frame_only=False)
        except: 
            pass

    return ret_frame, ret_audio

# --- LEGACY LOGIC ---
@calculate_time
def legacy_chat_response(audio, text_input, voice):
    # 1. ASR
    if audio and asr:
        question = asr.transcribe(audio)
    else:
        question = text_input if text_input else "Hello"
        
    # 2. LLM
    answer = llm.generate(question) if llm else "LLM not loaded."
    
    # 3. TTS
    tts_file = 'answer.wav'
    if edgetts:
        try:
            edgetts.predict(answer, voice, 0, 100, 0, tts_file, 'answer.vtt')
        except:
            pass
        
    # 4. SadTalker
    video = None
    if sadtalker:
        try:
            # Simplified call for demo stability
            video = sadtalker.test(
                "./inputs/girl.png", 
                "./inputs/first_frame_dir_girl/girl.png",
                "./inputs/first_frame_dir_girl/girl.mat",
                ((403, 403), (19, 30, 502, 513), [40.05, 40.17, 443.78, 443.90]),
                "./inputs/girl.png",
                tts_file,
                'crop', False, False, 1, 256, 0, 'facevid2vid', 1, False, None, 'pose', False, 5, True, 20
            )
        except Exception as e:
            print(f"SadTalker error: {e}")
        
    return answer, video

# --- UI ---
def main():
    with gr.Blocks(title="Linly-Talker Unified", theme=gr.themes.Soft()) as demo:
        gr.HTML(
            """
            <div style='text-align: center; margin-bottom: 20px;'>
                <h1>🎭 Linly-X-Gemini</h1>
                <p>Real-time AI Avatar powered by Gemini 2.5 Flash + MuseTalk</p>
            </div>
            """
        )
        
        with gr.Tabs():
            # TAB 1: GEMINI LIVE (NEW)
            with gr.Tab("⚡ Gemini Live (Real-time)"):
                gr.Markdown("### Next-Generation Real-time Avatar Conversation")
                
                with gr.Row():
                    with gr.Column(scale=1, variant='panel'):
                        gr.Markdown("#### Setup")
                        avatar_in = gr.Image(
                            label="Avatar Image/Video", 
                            sources=["upload"], 
                            type="filepath",
                            height=200
                        )
                        bbox = gr.Slider(
                            label="Mouth Position Fix", 
                            minimum=-10, 
                            maximum=10, 
                            value=5,
                            info="+ = down, - = up"
                        )
                        btn_prep = gr.Button("1. 🎭 Prepare Avatar", variant="secondary", size="lg")
                        btn_conn = gr.Button("2. 🔌 Connect Gemini", variant="primary", size="lg")
                        status = gr.Textbox(label="Status", interactive=False)
                    
                    with gr.Column(scale=2):
                        gr.Markdown("#### Live Interaction")
                        avatar_out = gr.Image(label="Live Stream", streaming=True, height=400)
                        mic = gr.Audio(
                            sources=["microphone"], 
                            type="numpy", 
                            streaming=True,
                            label="🎤 Your Voice"
                        )
                        speaker = gr.Audio(visible=False, autoplay=True, streaming=True)

                btn_prep.click(prepare_avatar, inputs=[avatar_in, bbox], outputs=[status])
                btn_conn.click(start_session, inputs=[], outputs=[status])
                mic.stream(
                    process_stream, 
                    inputs=[mic], 
                    outputs=[avatar_out, speaker],
                    stream_every=0.04,
                    time_limit=300
                )

            # TAB 2: LEGACY MODE (ORIGINAL)
            with gr.Tab("🐢 Legacy Mode (Offline Generation)"):
                gr.Markdown("### Traditional Pipeline: ASR → LLM → TTS → SadTalker")
                
                with gr.Row():
                    with gr.Column(variant='panel'):
                        gr.Markdown("#### Input")
                        audio_in = gr.Audio(sources=["microphone"], type="filepath", label="Voice Input")
                        text_in = gr.Textbox(label="Or Type Here", placeholder="Enter your question...")
                        voice_sel = gr.Dropdown(
                            edgetts.SUPPORTED_VOICE if edgetts else [], 
                            label="Voice", 
                            value='zh-CN-XiaoxiaoNeural'
                        )
                        btn_run = gr.Button("🎬 Generate", variant="primary", size="lg")
                    
                    with gr.Column():
                        gr.Markdown("#### Output")
                        text_out = gr.Textbox(label="LLM Response", lines=3)
                        video_out = gr.Video(label="SadTalker Result", autoplay=True)
                
                btn_run.click(
                    legacy_chat_response, 
                    inputs=[audio_in, text_in, voice_sel], 
                    outputs=[text_out, video_out]
                )
                
                gr.Markdown(
                    """
                    ### 📊 Comparison:
                    
                    | Feature | Gemini Live | Legacy Mode |
                    |---------|-------------|-------------|
                    | **Latency** | <1 second | 10-30 seconds |
                    | **Interaction** | Real-time streaming | Batch generation |
                    | **Interruption** | ✅ Supported | ❌ Not supported |
                    | **Quality** | MuseTalk (High) | SadTalker (Good) |
                    | **Use Case** | Live demos, conversation | Offline content |
                    """
                )

    return demo

if __name__ == "__main__":
    demo = main()
    demo.queue().launch(server_name=ip, server_port=port, debug=True, quiet=True)