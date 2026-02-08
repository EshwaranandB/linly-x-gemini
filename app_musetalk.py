import gradio as gr
import os
import warnings
import cv2

# --- NEW IMPORTS ---
from TFG import MuseTalk_RealTime # Using our updated engine
# -------------------

warnings.filterwarnings('ignore')

# --- CONFIGURATION ---
musetalker = None

# --- CORE LOGIC ---
def init_model():
    global musetalker
    if musetalker is None:
        print("🚀 Loading MuseTalk Model...")
        musetalker = MuseTalk_RealTime()
        musetalker.init_model()
        print("✅ MuseTalk Model Loaded")

def process_avatar(video_path, bbox_shift):
    """
    Pre-process video for MuseTalk (Extract frames, landmarks, latents)
    """
    init_model()
    if video_path is None:
        return None, "❌ No video uploaded"
    
    try:
        # Use our robust prepare_material (handles Images too!)
        musetalker.prepare_material(video_path, bbox_shift)
        return video_path, f"✅ Processed successfully! Avatar is ready for Gemini Live."
    except Exception as e:
        return None, f"❌ Error: {str(e)}"

# --- UI ---
def main():
    with gr.Blocks(title="MuseTalk Debugger", theme=gr.themes.Soft()) as demo:
        gr.HTML(
            """
            <div style='text-align: center; margin-bottom: 20px;'>
                <h2>🔧 MuseTalk Engine Debugger</h2>
                <p>Test avatar compatibility before using with Gemini Live</p>
            </div>
            """
        )
        
        gr.Markdown(
            """
            ### Purpose
            Use this tool to verify your avatar video/image works correctly with the MuseTalk engine 
            before connecting to Gemini Live. If processing succeeds here, it will work in the main apps.
            """
        )

        with gr.Row():
            with gr.Column():
                gr.Markdown("### 📤 Input")
                source_video = gr.Video(
                    label="Upload Avatar (Video/Image)", 
                    sources=['upload'],
                    height=300
                )
                bbox_shift = gr.Number(
                    label="BBox Shift (Mouth Fix)", 
                    value=5,
                    info="Adjust mouth position: + = down, - = up"
                )
                btn_process = gr.Button("⚙️ Process Avatar", variant="primary", size="lg")
                
            with gr.Column():
                gr.Markdown("### ✅ Output Check")
                output_path = gr.Textbox(
                    label="Processed Path", 
                    interactive=False,
                    placeholder="Processed file path will appear here"
                )
                status = gr.Textbox(
                    label="Status", 
                    interactive=False,
                    placeholder="Processing status will appear here"
                )

        # Wiring
        btn_process.click(
            fn=process_avatar,
            inputs=[source_video, bbox_shift],
            outputs=[output_path, status]
        )

        gr.Markdown("### 📋 Valid Examples")
        gr.Examples(
            examples=[
                ['Musetalk/data/video/yongen_musev.mp4', 5],
            ],
            inputs=[source_video, bbox_shift]
        )
        
        gr.Markdown(
            """
            ### 💡 Tips
            - **Video**: Use MP4 format, 5-30 seconds recommended
            - **Image**: Use JPG/PNG, frontal face, clear features
            - **BBox Shift**: Usually 0-10 works best, adjust if mouth looks misaligned
            - **Success**: If you see "✅ Processed successfully", your avatar is compatible!
            """
        )

    return demo

if __name__ == "__main__":
    demo = main()
    demo.queue().launch(server_name="0.0.0.0", server_port=7860, quiet=True)
