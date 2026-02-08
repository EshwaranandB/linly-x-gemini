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

# --- NEW IMPORTS (Gemini Live) ---
try:
    from TFG import MuseTalk_RealTime
    musetalk_available = True
except ImportError:
    musetalk_available = False

# --- LEGACY IMPORTS ---
try:
    from TFG import SadTalker
    sadtalker = SadTalker(lazy_load=True)
except:
    sadtalker = None

try:
    from VITS import GPT_SoVITS
    vits = GPT_SoVITS()
except:
    vits = None

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

os.environ["GRADIO_TEMP_DIR"]= './temp'
warnings.filterwarnings('ignore')

# --- CONFIGURATION ---
pic_path = "./inputs/boy.png"
crop_pic_path = "./inputs/first_frame_dir_boy/boy.png"
first_coeff_path = "./inputs/first_frame_dir_boy/boy.mat"
crop_info = ((876, 747), (0, 0, 886, 838), [10.382, 0, 886, 747.707])

# --- LOGIC ---

@calculate_time
def Talker_response(question_audio, text, voice, rate, volume, pitch, batch_size):
    driven_audio = 'answer.wav'
    
    # 1. LLM Generation
    if llm:
        answer = llm.generate(text)
    else:
        answer = text # Fallback

    # 2. Voice Generation (Cloning vs EdgeTTS)
    if voice == "Cloned Voice (GPT-SoVITS)" and vits:
        if question_audio is None:
            return None, "❌ No reference audio for cloning!"
        # Simplified cloning call for demo
        try:
            vits.predict(ref_wav_path=question_audio, 
                        prompt_text="Hello", 
                        prompt_language="English", 
                        text=answer, 
                        text_language="English", 
                        save_path=driven_audio)
        except Exception as e:
            return None, f"❌ Voice cloning failed: {str(e)}"
    elif edgetts:
        try:
            edgetts.predict(answer, voice, rate, volume, pitch, driven_audio, 'answer.vtt')
        except:
            os.system(f'edge-tts --text "{answer}" --voice {voice} --write-media {driven_audio}')

    # 3. Video Generation
    if sadtalker:
        try:
            video = sadtalker.test(pic_path, crop_pic_path, first_coeff_path, crop_info, 
                                  pic_path, driven_audio, 'crop', False, False, batch_size, 256, 
                                  0, 'facevid2vid', 1, False, None, 'pose', False, 5, True, 20)
            return video, f"✅ Generated with {voice}"
        except Exception as e:
            return None, f"❌ Video generation failed: {str(e)}"
    
    return None, "❌ SadTalker not loaded"

# --- UI ---
def main():
    with gr.Blocks(title='Linly-Talker VITS Clone', theme=gr.themes.Soft()) as inference:
        gr.HTML(
            """
            <div style='text-align: center; margin-bottom: 20px;'>
                <h1>🗣️ Voice Cloning Avatar</h1>
                <p>Clone voices using GPT-SoVITS or use EdgeTTS</p>
            </div>
            """
        )
        
        with gr.Row():
            with gr.Column(variant='panel'):
                gr.Markdown("### Input")
                input_text = gr.Textbox(
                    label="Input Text", 
                    lines=3,
                    placeholder="Enter the text you want the avatar to say..."
                )
                question_audio = gr.Audio(
                    sources=['microphone','upload'], 
                    type="filepath", 
                    label='Reference Audio (for Voice Cloning)',
                    info="Upload 5-10 seconds of clear speech for best cloning results"
                )
                
                with gr.Accordion("Settings", open=True):
                    voice = gr.Dropdown(
                        ["Cloned Voice (GPT-SoVITS)"] + (edgetts.SUPPORTED_VOICE if edgetts else []), 
                        value='Cloned Voice (GPT-SoVITS)', 
                        label="Voice"
                    )
                    batch_size = gr.Slider(
                        minimum=1, 
                        maximum=10, 
                        value=2, 
                        step=1, 
                        label='Batch Size'
                    )

                submit_btn = gr.Button("🎬 Generate Avatar", variant='primary', size='lg')

            with gr.Column():
                gr.Markdown("### Output")
                output_video = gr.Video(label="Result", autoplay=True, height=500)
                status = gr.Textbox(label="Status", interactive=False)
                
                gr.Markdown(
                    """
                    ### 💡 Tips:
                    - **Voice Cloning**: Upload clear reference audio (5-10 seconds)
                    - **EdgeTTS**: Select from 400+ voices in different languages
                    - **LLM**: Qwen model generates responses if loaded
                    - **Avatar**: Uses SadTalker for video generation
                    """
                )

        submit_btn.click(
            fn=Talker_response,
            inputs=[question_audio, input_text, voice, 0, 100, 0, batch_size],
            outputs=[output_video, status]
        )

    return inference

if __name__ == "__main__":
    demo = main()
    demo.queue().launch(server_name=ip, server_port=port, debug=True, quiet=True)