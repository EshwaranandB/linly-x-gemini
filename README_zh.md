Digital Human Intelligent Dialogue System - Linly-Talker — “Digital Human Interaction, Interact with the Virtual You”<div align="center"><h1>Linly-Talker WebUI</h1><img src="docs/linly_logo.png" />English | Simplified Chinese</div>2023.12 Update 📆Users can upload any image for dialogue.2024.01 Update 📆Exciting news! I have now integrated the powerful GeminiPro and Qwen large models into our conversation scenarios. Users can now upload any image during the conversation, adding a brand new dimension to our interactions.Updated the FastAPI deployment invocation method.Updated Microsoft TTS advanced setting options, increasing the diversity of voice types and adding video subtitles to enhance visualization.Updated the GPT multi-turn dialogue system, enabling context-aware conversations and improving the interactivity and realism of the digital human.2024.02 Update 📆Updated Gradio to the latest version 4.16.0, enabling more features in the interface, such as capturing images via camera to build digital humans.Updated ASR and THG. ASR now includes Alibaba's FunASR for faster speeds; the THG section added the Wav2Lip model, with ER-NeRF coming soon.Added the voice cloning method GPT-SoVITS model, capable of cloning voices with just one minute of fine-tuning data. The effect is quite impressive and highly recommended.Integrated a WebUI interface to better run Linly-Talker.2024.04 Update 📆Updated offline method for Paddle TTS in addition to Edge TTS.Updated ER-NeRF as one of the Avatar generation choices.Updated app_talk.py to allow free upload of voice and images/videos for generation without being based on a dialogue scenario.2024.05 Update 📆Updated the zero-basis beginner AutoDL deployment tutorial and updated the codewithgpu image for one-click experience and learning.Updated WebUI.py, Linly-Talker WebUI now supports multiple modules, multiple models, and multiple options.2024.06 Update 📆Updated MuseTalk integration into Linly-Talker and updated the WebUI to basically achieve real-time dialogue.The improved WebUI does not load the LLM model by default to reduce VRAM usage, and can complete broadcasting functions directly through Q&A. The refined WebUI includes three main functions: personalized character generation, multi-turn intelligent dialogue with digital humans, and MuseTalk real-time dialogue. These improvements not only reduce previous VRAM redundancy but also add more tips to help users use it more easily.2024.08 Update 📆Updated CosyVoice, featuring high-quality Text-To-Speech (TTS) capabilities and voice cloning abilities; simultaneously updated Wav2Lipv2 to improve overall results.2024.09 Update 📆Added Linly-Talker API documentation, providing detailed interface descriptions to help users use Linly-Talker functions via API.2024.12 Update 📆Simple bug fixes for Edge-TTS, resolved some issues with MuseTalk, planned to add fishTTS for more stable TTS effects, and introduced advanced digital human technologies.2025.02 Update 📆Added the faster speech recognition model OmniSenseVoice.<details><summary>Table of Contents</summary>Digital Human Intelligent Dialogue System - Linly-Talker — “Digital Human Interaction, Interact with the Virtual You”IntroductionTO DO LISTExamplesEnvironment SetupAPI DocumentationASR - Speech RecognitionWhisperFunASRComing SoonTTS Text To SpeechEdge TTSPaddleTTSComing SoonVoice CloneGPT-SoVITS (Recommended)XTTSCosyVoiceComing SoonTHG - AvatarSadTalkerWav2LipWav2Lipv2ER-NeRFMuseTalkComing SoonLLM - ConversationLinly-AIQwenGemini-ProChatGPTChatGLMGPT4FreeLLM Multi-model SelectionComing SoonOptimizationGradioLaunching WebUIWebUIOld VersionFolder StructureReferencesLicenseStar History</details>IntroductionLinly-Talker is an innovative digital human dialogue system that integrates the latest artificial intelligence technologies, including Large Language Models (LLM) 🤖, Automatic Speech Recognition (ASR) 🎙️, Text-to-Speech (TTS) 🗣️, and Voice Cloning technologies 🎤. This system provides an interactive Web interface through the Gradio platform, allowing users to upload images 📷 and engage in personalized conversations 💬 with AI.Key features of the system include:Multi-model Integration: Linly-Talker integrates large models such as Linly, GeminiPro, and Qwen, as well as visual models like Whisper and SadTalker, achieving high-quality dialogue and visual generation.Multi-turn Dialogue Capability: Through the GPT model's multi-turn dialogue system, Linly-Talker can understand and maintain contextually relevant continuous conversations, greatly enhancing the realism of interaction.Voice Cloning: Utilizing technologies like GPT-SoVITS, users can upload a one-minute voice sample for fine-tuning, and the system will clone the user's voice, allowing the digital human to speak with the user's voice.Real-time Interaction: The system supports real-time speech recognition and video subtitles, enabling users to communicate naturally with the digital human via voice.Visual Enhancement: Through digital human generation technologies, Linly-Talker can generate realistic digital human figures, providing a more immersive experience.The design philosophy of Linly-Talker is to create a new way of human-computer interaction, not just simple Q&A, but providing an intelligent digital human capable of understanding, responding, and simulating human communication through highly integrated technologies.[!NOTE]Watch our introduction video demo videoI have recorded a series of videos on Bilibili, representing every step of my updates and usage methods. For details, view the Digital Human Intelligent Dialogue System - Linly-Talker Collection🔥🔥🔥Digital Human Dialogue System Linly-Talker🔥🔥🔥🚀The Future of Digital Humans: Empowerment via Linly-Talker + GPT-SoVITS Voice Cloning TechnologyDeploy Linly-Talker on AutoDL Platform (Super detailed tutorial for beginners)Linly-Talker Update: Offline TTS Integration & Custom Digital Human SolutionsTO DO LIST[x] Basically completed the dialogue system process, capable of voice dialogue[x] Added LLM large models, including usage of Linly, Qwen, and GeminiPro[x] Ability to upload any digital human photo for dialogue[x] Added FastAPI invocation method for Linly[x] utilized Microsoft TTS to add advanced options, allowing settings for corresponding human voices and pitch parameters, increasing voice diversity[x] Added subtitles to video generation for better visualization[x] GPT multi-turn dialogue system (improves interactivity and realism, enhances intelligence)[x] Optimized Gradio interface, added more models like Wav2Lip, FunASR, etc.[x] Voice Cloning technology, added GPT-SoVITS, requiring only one minute of voice for simple fine-tuning (synthesizing your own voice improves realism and interaction experience)[x] Added offline TTS and NeRF-based methods and models[x] Linly-Talker WebUI supports multiple modules, multiple models, and multiple options[x] Added MuseTalk functionality to Linly-Talker, basically achieving real-time speed with fast communication[x] Integrated MuseTalk into Linly-Talker WebUI[x] Added CosyVoice, featuring high-quality Text-To-Speech (TTS) and voice cloning capabilities. Also updated Wav2Lipv2 to improve image quality.[x] Added Linly-Talker API documentation, providing detailed interface descriptions[ ] Real-time speech recognition (enabling voice conversation between humans and digital humans)[!IMPORTANT]🔆 The Linly-Talker project is ongoing - PR requests are welcome! If you have any suggestions regarding new model methods, research, techniques, or find runtime errors, please feel free to edit and submit a PR. You can also open an issue or contact me directly via email. 📩⭐ If you find this Github Project useful, please give it a star! 🤩[!TIP]If you encounter any problems during deployment, you can check the FAQ / Troubleshooting Summary section. I have compiled all potential issues. The community group is also there. I will update it regularly. Thank you for your attention and usage!!!ExamplesText/Voice DialogueDigital Human ResponseWhat is the most effective way to deal with stress?<video src="https://github.com/Kedreamix/Linly-Talker/assets/61195303/f1deb189-b682-4175-9dea-7eeb0fb392ca"></video>How to manage time?<video src="https://github.com/Kedreamix/Linly-Talker/assets/61195303/968b5c43-4dce-484b-b6c6-0fd4d621ac03"></video>Write a symphony concert review discussing the orchestra's performance and the audience's overall experience.<video src="https://github.com/Kedreamix/Linly-Talker/assets/61195303/f052820f-6511-4cf0-a383-daf8402630db"></video>Translate to Chinese: Luck is a dividend of sweat. The more you sweat, the luckier you get.<video src="https://github.com/Kedreamix/Linly-Talker/assets/61195303/118eec13-a9f7-4c38-b4ad-044d36ba9776"></video>Environment Setup[!NOTE]AutoDL image has been released and can be used directly: https://www.codewithgpu.com/i/Kedreamix/Linly-Talker/Kedreamix-Linly-Talker. You can also use Docker to create the environment directly. I will continuously update the image.Bashdocker pull registry.cn-beijing.aliyuncs.com/codewithgpu2/kedreamix-linly-talker:afGA8RPDLf
For Windows, I added a Python one-click integration package. You can run it in sequence to install the corresponding dependencies and download the corresponding models as needed. The main process involves installing PyTorch starting from 02 after conda. If there are any questions, please feel free to communicate with me.Windows One-Click Integration PackageDownload CodeBashgit clone https://github.com/Kedreamix/Linly-Talker.git --depth 1

cd Linly-Talker
git submodule update --init --recursive
If using Linly-Talker, you can use Anaconda to install the environment directly, including almost all dependencies required by the models. The specific operations are as follows:Bashconda create -n linly python=3.10
conda activate linly

# Pytorch installation method 1: conda installation
# CUDA 11.8
# conda install pytorch==2.4.1 torchvision==0.19.1 torchaudio==2.4.1  pytorch-cuda=11.8 -c pytorch -c nvidia
# CUDA 12.1
# conda install pytorch==2.4.1 torchvision==0.19.1 torchaudio==2.4.1 pytorch-cuda=12.1 -c pytorch -c nvidia
# CUDA 12.4
# conda install pytorch==2.4.1 torchvision==0.19.1 torchaudio==2.4.1 pytorch-cuda=12.4 -c pytorch -c nvidia

# Pytorch installation method 2: pip installation
# CUDA 11.8
# pip install torch==2.4.1 torchvision==0.19.1 torchaudio==2.4.1 --index-url https://download.pytorch.org/whl/cu118
# CUDA 12.1
# pip install torch==2.4.1 torchvision==0.19.1 torchaudio==2.4.1 --index-url https://download.pytorch.org/whl/cu121
# CUDA 12.4
# pip install torch==2.4.1 torchvision==0.19.1 torchaudio==2.4.1 --index-url https://download.pytorch.org/whl/cu124

conda install -q ffmpeg==4.2.2 # ffmpeg==4.2.2

# Upgrade pip
python -m pip install --upgrade pip
# Change pypi source to accelerate library installation (Tsinghua source)
pip config set global.index-url https://pypi.tuna.tsinghua.edu.cn/simple

pip install tb-nightly -i https://mirrors.aliyun.com/pypi/simple
pip install -r requirements_webui.txt

# Install dependencies related to musetalk
pip install --no-cache-dir -U  openmim
mim install mmengine 
mim install "mmcv==2.1.0" 
mim install "mmdet>=3.1.0" 
mim install "mmpose>=1.1.0" 

# 💡CosyVoice's ttsfrd can be replaced by WeTextProcessing, so the following steps can be omitted, ensuring operation in other python versions

# ⚠️Note: First download CosyVoice-ttsfrd. You need to finish downloading the model before this step.
# mkdir -p CosyVoice/pretrained_models # Create folder CosyVoice/pretrained_models
# mv checkpoints/CosyVoice_ckpt/CosyVoice-ttsfrd CosyVoice/pretrained_models # Move directory
# unzip CosyVoice/pretrained_models/CosyVoice-ttsfrd/resource.zip # Unzip
# This whl library is only suitable for python 3.8 version
# pip install CosyVoice/pretrained_models/CosyVoice-ttsfrd/ttsfrd-0.3.6-cp38-cp38-linux_x86_64.whl

# Install NeRF-based dependencies. There might be many issues, can skip for now.
pip install "git+https://github.com/facebookresearch/pytorch3d.git"
# If issues occur installing pytorch3d, run the following command directly
# python scripts/install_pytorch3d.py
pip install -r TFG/requirements_nerf.txt

# If pyaudio issues occur, install corresponding dependencies fatal error: portaudio.h
# sudo apt-get update
# sudo apt-get install libasound-dev portaudio19-dev libportaudio2 libportaudiocpp0

# Note the following modules. If installation fails, enter the path and use pip install . or python setup.py install to compile and install
# NeRF/freqencoder
# NeRF/gridencoder
# NeRF/raymarching
# NeRF/shencoder

# If you encounter sox compatibility issues
# ubuntu
sudo apt-get install sox libsox-dev
# centos
sudo yum install sox sox-devel
[!NOTE]The installation process may take a long time.Below are some installation methods for older versions. There may be some dependency conflict issues, but generally not too many bugs. However, for better and more convenient installation, I have updated the above version. The following can be ignored or referenced if you encounter problems.First use Anaconda to install the environment and PyTorch environment. Operations are as follows:Bashconda create -n linly python=3.10  
conda activate linly
Pytorch installation method 1: conda installation (Recommended)conda install pytorch==1.12.1 torchvision==0.13.1 torchaudio==0.12.1 cudatoolkit=11.3 -c pytorchPytorch installation method 2: pip installationpip install torch==1.12.1+cu113 torchvision==0.13.1+cu113 torchaudio==0.12.1 --extra-index-url https://download.pytorch.org/whl/cu113conda install -q ffmpeg # ffmpeg==4.2.2pip install -r requirements_app.txt
If using Voice Cloning models, higher versions of Pytorch are needed, but features will be richer. However, the required driver version might need to be cuda11.8. Options:
Bashconda create -n linly python=3.10  
conda activate linly
pip install torch==2.0.1 torchvision==0.15.2 torchaudio==2.0.2 --index-url https://download.pytorch.org/whl/cu118conda install -q ffmpeg # ffmpeg==4.2.2pip install -r requirements_app.txtInstall dependencies for voice cloningpip install -r VITS/requirements_gptsovits.txt
If you wish to use NeRF-based models, you may need to install the corresponding environment:
Bash# Install NeRF corresponding dependencies
pip install "git+https://github.com/facebookresearch/pytorch3d.git"
pip install -r TFG/requirements_nerf.txt
If pyaudio issues occur, install corresponding dependenciessudo apt-get updatesudo apt-get install libasound-dev portaudio19-dev libportaudio2 libportaudiocpp0Note the following modules. If installation fails, enter the path and use pip install . or python setup.py install to compile and installNeRF/freqencoderNeRF/gridencoderNeRF/raymarchingNeRF/shencoder
If using PaddleTTS, install the corresponding environment:
Bashpip install -r TTS/requirements_paddle.txt
If using FunASR speech recognition model, install environment:pip install -r ASR/requirements_funasr.txt
If using MuseTalk model, install environment:Bashpip install --no-cache-dir -U openmim 
mim install mmengine 
mim install "mmcv>=2.0.1" 
mim install "mmdet>=3.1.0" 
mim install "mmpose>=1.1.0" 
pip install -r TFG/requirements_musetalk.txt 
[!NOTE]Next, you need to install the corresponding models. There are the following download methods. After downloading, place them according to the folder structure explained at the end of this document. It is recommended to download from ModelScope for the latest updates.Baidu (Baidu Netdisk) (Password: linl)huggingfacemodelscopeQuark(Quark Netdisk)I created a script that can complete the download of all the models mentioned below without excessive user operation. This method is suitable for stable network conditions and is particularly suitable for Linux users. Windows users can also use Git to download models. If the network environment is unstable, users can choose to use the manual download method or try running the Shell script to complete the download. The script has the following functions:Select Download Method: Users can choose to download models from three different sources: ModelScope, Huggingface, or Huggingface mirror site.Download Models: Executes the corresponding download command based on the user's choice.Move Model Files: After downloading, move the model files to the specified directory.Error Handling: Error checking is included in every step. If an operation fails, the script will output an error message and stop execution.Bashsh scripts/download_models.sh
HuggingFace DownloadIf the speed is too slow, consider using a mirror. Reference Easy and fast acquisition of Hugging Face models (using mirror sites)Bash# Download pretrained models from huggingface
git lfs install
git clone https://huggingface.co/Kedreamix/Linly-Talker --depth 1
# git lfs clone https://huggingface.co/Kedreamix/Linly-Talker

# pip install -U huggingface_hub
# export HF_ENDPOINT=https://hf-mirror.com # Use mirror site
huggingface-cli download --resume-download --local-dir-use-symlinks False Kedreamix/Linly-Talker --local-dir Linly-Talker
ModelScope DownloadBash# Download pretrained models from modelscope
# 1. git method
git lfs install
git clone https://www.modelscope.cn/Kedreamix/Linly-Talker.git --depth 1
# git lfs clone https://www.modelscope.cn/Kedreamix/Linly-Talker.git --depth 1

# 2. Python code download
pip install modelscope
from modelscope import snapshot_download
model_dir = snapshot_download('Kedreamix/Linly-Talker', resume_download=True, cache_dir='./', revision='master')
Move all models to the current directoryIf downloaded via Baidu Netdisk, please refer to the directory structure at the end of the document to move the directories.Bash# Move all models to the current directory
# checkpoints contains SadTalker and Wav2Lip weights
mv Linly-Talker/checkpoints/* ./checkpoints

# If using GFPGAN enhancement, install the library
# pip install gfpgan
# mv Linly-Talker/gfpan ./

# Voice cloning models
mv Linly-Talker/GPT_SoVITS/pretrained_models/* ./GPT_SoVITS/pretrained_models/

# Qwen Large Model
mv Linly-Talker/Qwen ./

# MuseTalk Model
mkdir -p ./Musetalk/models
mv Linly-Talker/MuseTalk/* ./Musetalk/models
For easier deployment and usage, a configs.py file has been updated. You can modify some hyperparameters in it.Bash# Device running port
port = 6006

# API running port and IP
mode = 'api' # api needs to run Linly-api-fast.py first, currently only applies to Linly

# Local port localhost:127.0.0.1 Global port forwarding: "0.0.0.0"
ip = '127.0.0.1' 
api_port = 7871

# LLM model path (Linly model path)
mode = 'offline'
model_path = 'Qwen/Qwen-1_8B-Chat'

# SSL certificate (SSL certificate) Microphone dialogue needs this parameter
# Best adjusted to absolute path
ssl_certfile = "./https_cert/cert.pem"
ssl_keyfile = "./https_cert/key.pem"
API DocumentationIn the api/README.md file, we detail the usage and configuration of the Linly-Talker API. These documents provide users with information on how to call the API, required parameters, returned data formats, etc. By consulting these documents, users can gain deeper insight into how to implement Linly-Talker's functions via API interfaces, including starting dialogues, uploading images, performing speech recognition, and generating speech.To get these detailed API interface descriptions, please visit the api/README.md file.ASR - Speech RecognitionFor detailed usage introduction and code implementation regarding speech recognition, see ASR - Bridge to Communicate with Digital Humans.WhisperImplemented ASR speech recognition borrowing from OpenAI's Whisper. For specific usage, refer to https://github.com/openai/whisper.FunASRAlibaba's FunASR offers quite good speech recognition results, is faster than Whisper, and is actually better for Chinese.Since FunASR can achieve real-time effects better, FunASR has also been added. You can experience it in the FunASR file under the ASR folder. Refer to https://github.com/alibaba-damo-academy/FunASR.Coming SoonSuggestions are welcome to motivate me to constantly update models and enrich Linly-Talker's functions.TTS Text To SpeechFor detailed usage introduction and code implementation regarding Text-to-Speech, see TTS - Endowing Digital Humans with Realistic Voice Interaction.Edge TTSBorrowed usage of Microsoft speech services. For specific usage, refer to https://github.com/rany2/edge-tts.[!Warning]Due to some issues with the Edge TTS repository, seemingly because Microsoft restricted certain IPs, see 403 error is back/need to implement Sec-MS-GEC token and Add support for clock adjustment for Sec-MS-GEC token. It is currently found to be unstable. I have made modifications, but if you find it unstable, please use other methods. The CosyVoice method is recommended.PaddleTTSIn actual use, you may encounter situations requiring offline operation. Since Edge TTS requires an online environment to generate speech, we chose the open-source PaddleSpeech as an alternative for text-to-speech (TTS). Although the effect may differ, PaddleSpeech supports offline operation. For more information, refer to the PaddleSpeech GitHub page: PaddleSpeech.Coming SoonSuggestions are welcome to motivate me to constantly update models and enrich Linly-Talker's functions.Voice CloneFor detailed usage introduction and code implementation regarding Voice Cloning, see Voice Clone - Stealing Your Voice Quietly During Conversation.GPT-SoVITS (Recommended)Thanks to everyone's open-source contributions, I borrowed the current open-source voice cloning model GPT-SoVITS. I think the effect is quite good. Project address: https://github.com/RVC-Boss/GPT-SoVITS.I have placed some trained cloning weights in Quark(Quark Netdisk). You can pick up the weights and reference audio there.XTTSCoqui XTTS is a leading deep learning text-to-speech toolkit (TTS voice generation model) that can complete voice cloning cloning voice into different languages using a voice clip of over 5 seconds.🐸TTS is a library for advanced text-to-speech generation.🚀 Pretrained models for over 1100 languages.🛠️ Tools for training new models and fine-tuning existing models in any language.📚 Utilities for dataset analysis and management.Experience XTTS online: https://huggingface.co/spaces/coqui/xttsOfficial Github repository: https://github.com/coqui-ai/TTSCosyVoiceCosyVoice is a multilingual speech understanding model open-sourced by Alibaba's Tongyi Lab, focusing on high-quality speech synthesis. This model has been trained on over 150,000 hours of data and supports speech synthesis in multiple languages including Chinese, English, Japanese, Cantonese, and Korean. CosyVoice excels in multi-language speech generation, zero-shot speech generation, cross-language voice synthesis, and instruction execution capabilities.CosyVoice supports one-shot voice cloning technology, generating realistic and natural simulated voices, including prosody and emotion details, with just 3 to 10 seconds of original audio.GitHub Project Address: https://github.com/FunAudioLLM/CosyVoiceCosyVoice includes several pretrained speech synthesis models, mainly:CosyVoice-300M: Supports multi-language zero-shot and cross-lingual speech synthesis in Chinese, English, Japanese, Cantonese, and Korean.CosyVoice-300M-SFT: A model focused on Supervised Fine-Tuning (SFT) inference.CosyVoice-300M-Instruct: A model supporting instruction inference, capable of generating speech containing specific tones, emotions, etc.Main Features:Multi-language Support: Capable of processing multiple languages, including Chinese, English, Japanese, Cantonese, and Korean.Multi-style Speech Synthesis: Can control the tone and emotion of generated speech via instructions.Streaming Inference Support: Will support streaming inference mode in the future, including KV cache and SDPA technologies for real-time optimization.Currently, Linly-Talker has integrated three functions: Pretrained Voice, 3s Quick Clone, and Cross-lingual Clone. For more interesting features, please continue to follow Linly-Talker. Below are some effects of CosyVoice:<table><tr><th></th><th align="center">PROMPT TEXT</th><th align="center">PROMPT SPEECH</th><th align="center">TARGET TEXT</th><th align="center">RESULT</th></tr><tr><td align="center"><strong>Pretrained Voice</strong></td><td align="center">Chinese Female Voice ('Chinese Female', 'Chinese Male', 'Japanese Male', 'Cantonese Female', 'English Female', 'English Male', 'Korean Female')</td><td align="center">—</td><td align="center">Hello, I am the Tongyi generative speech large model. Is there anything I can help you with?</td><td align="center">sft.webm</td></tr><tr><td align="center"><strong>3s Language Clone</strong></td><td align="center">Hope you can do better than me in the future.</td><td align="center">zero_shot_prompt.webm</td><td align="center">Receiving a birthday gift from a friend far away, that unexpected surprise and deep blessing filled my heart with sweet happiness, and a smile bloomed like a flower.</td><td align="center">zero_shot.webm</td></tr><tr><td align="center"><strong>Cross-lingual Clone</strong></td><td align="center">And then later on, fully acquiring that company. So keeping management in line, interest in line with the asset that's coming into the family is a reason why sometimes we don't buy the whole thing.</td><td align="center">cross_lingual_prompt.webm</td><td align="center">&lt; |en|&gt;And then later on, fully acquiring that company. So keeping management in line, interest in line with the asset that's coming into the family is a reason why sometimes we don't buy the whole thing.</td><td align="center">cross_lingual.webm</td></tr></table>Coming SoonSuggestions are welcome to motivate me to constantly update models and enrich Linly-Talker's functions.THG - AvatarFor detailed usage introduction and code implementation regarding Digital Human Generation, see THG - Building Intelligent Digital Humans.SadTalkerDigital human generation can use SadTalker (CVPR 2023). For details, see https://sadtalker.github.io.Download SadTalker models before use:Bashbash scripts/sadtalker_download_models.sh 
Baidu (Baidu Netdisk) (Password: linl)Quark(Quark Netdisk)If downloading from Baidu Netdisk, remember to place it under the checkpoints folder. The default name from Baidu Netdisk download is sadtalker, which should actually be renamed to checkpoints.Wav2LipDigital human generation can also use Wav2Lip (ACM 2020). For details, see https://github.com/Rudrabha/Wav2Lip.Download Wav2Lip models before use:ModelDescriptionLink to the modelWav2LipHighly accurate lip-syncLinkWav2Lip + GANSlightly inferior lip-sync, but better visual qualityLinkExpert DiscriminatorWeights of the expert discriminatorLinkVisual Quality DiscriminatorWeights of the visual disc trained in a GAN setupLinkWav2Lipv2Borrowed from the https://github.com/primepake/wav2lip_288x288 repository, using a newly trained 288 model, yielding higher quality results.Also uses YOLO for face detection, improving the overall effect slightly. You can compare and test in Linly-Talker. The model has been updated. The comparison is as follows:Wav2LipWav2Lipv2<video src="https://github.com/user-attachments/assets/d61df5cf-e3b9-4057-81fc-d69dcff806d6"></video><video src="https://github.com/user-attachments/assets/7f6be271-2a4d-4d9c-98f8-db25816c28b3"></video>ER-NeRFER-NeRF (ICCV2023) builds digital humans using the latest NeRF technology, featuring customized digital humans. It only requires about five minutes of video of a person to reconstruct them. Refer to https://github.com/Fictionarry/ER-NeRF.Updated with Obama's image as a reference. If better results are desired, consider cloning the customized digital human's voice for better effect.MuseTalkMuseTalk is a real-time high-quality audio-driven lip synchronization model capable of running at over 30 fps on an NVIDIA Tesla V100 GPU. This model can be used in conjunction with input video generated by MuseV as part of a complete virtual human solution. Refer to https://github.com/TMElyralab/MuseTalk.MuseTalk is a real-time high-quality audio-driven lip synchronization model trained to work in the latent space of ft-mse-vae. It features:Unseen Face Synchronization: Modifies unseen faces based on input audio, with a face region size of 256 x 256.Multi-language Support: Supports audio input in multiple languages, including Chinese, English, and Japanese.High-Performance Real-time Inference: Achieves over 30fps real-time inference on NVIDIA Tesla V100.Face Center Adjustment: Supports modifying the center position of the face region, significantly affecting generation results.HDTF Dataset Training: Provides model checkpoints trained on the HDTF dataset.Training Code Coming Soon: Training code will be released soon to facilitate further development and research.MuseTalk offers an efficient and flexible tool for precise audio-lip synchronization of virtual humans, taking a significant step towards fully interactive virtual humans.MuseTalk has been added to Linly-Talker, inferencing based on MuseV videos, achieving ideal speeds for dialogue, basically reaching real-time effects, which is very impressive. It also supports streaming inference.Coming SoonSuggestions are welcome to motivate me to constantly update models and enrich Linly-Talker's functions.LLM - ConversationFor detailed usage introduction and code implementation regarding Large Models, see LLM - Large Language Models Empowering Digital Humans.Linly-AILinly comes from the National Key Laboratory of Data Engineering at Shenzhen University. Refer to https://github.com/CVI-SZU/Linly.QwenQwen from Alibaba Cloud. View https://github.com/QwenLM/Qwen.If you want quick usage, you can choose the 1.8B model. It has fewer parameters and works normally with smaller VRAM. Of course, this part can be replaced.Download Qwen1.8B model: https://huggingface.co/Qwen/Qwen-1_8B-Chat.Gemini-ProGemini-Pro from Google. Learn more at https://deepmind.google/technologies/gemini/.Request API Key: https://makersuite.google.com/.ChatGPTFrom OpenAI. Requires API application. Learn more at https://platform.openai.com/docs/introduction.ChatGLMFrom Tsinghua University. Learn more at https://github.com/THUDM/ChatGLM3.GPT4FreeRefer to https://github.com/xtekky/gpt4free for free usage of models like GPT4.LLM Multi-model SelectionIn the webui.py file, easily select the model you need. ⚠️ Download the model first for the first run, referencing Qwen1.8B.Coming SoonSuggestions are welcome to motivate me to constantly update models and enrich Linly-Talker's functions.OptimizationSome optimizations:Use fixed input face images, extract features in advance to avoid reading every time.Remove unnecessary libraries to shorten total time.Only save final video output, do not save intermediate results, improving performance.Use OpenCV to generate the final video, faster than mimwrite.GradioGradio is a Python library that provides a simple way to deploy machine learning models as interactive Web applications.For Linly-Talker, using Gradio has two main purposes:Visualization and Demonstration: Gradio provides a simple Web GUI for the model. After uploading images and text, results can be seen intuitively. This is an effective way to showcase system capabilities.User Interaction: The Gradio GUI serves as a frontend, allowing users to interact with Linly-Talker. Users can upload their own images and input questions to get real-time answers. This provides a more natural way of voice interaction.Specifically, we created a Gradio Interface in app.py that receives image and text inputs, calls functions to generate response videos, and displays them in the GUI. This achieves browser interaction without writing complex frontends.In summary, Gradio provides visualization and user interaction interfaces for Linly-Talker, making it an effective way to showcase system functions and let end-users use the system.If considering real-time dialogue, frameworks might need to be changed, or Gradio heavily modified. Hope to work hard with everyone on this.Launching WebUIPreviously, I separated many versions, which was troublesome to run individually. So I added a WebUI to experience everything in one interface, which will be continuously updated.WebUIFeatures currently added to WebUI:[x] Text/Voice Digital Human Dialogue (Fixed digital human, Male/Female roles)[x] Any Image Digital Human Dialogue (Upload any digital human image)[x] Multi-turn GPT Dialogue (Includes history data, context linking)[x] Voice Cloning Dialogue (Based on GPT-SoVITS settings for voice cloning, or cloning based on voice dialogue sound)[x] Digital Human Text/Voice Broadcasting (Broadcasting based on input text/voice)[x] Multi-module ➕ Multi-model ➕ Multi-choice[x] Role Selection: Female/Male/Custom (Custom allows auto image upload) / Coming Soon[x] TTS Model Selection: EdgeTTS / PaddleTTS / GPT-SoVITS / CosyVoice / Coming Soon[x] LLM Model Selection: Linly / Qwen / ChatGLM / GeminiPro / ChatGPT / Coming Soon[x] Talker Model Selection: Wav2Lip / Wav2Lipv2 / SadTalker / ERNeRF / MuseTalk / Coming Soon[x] ASR Model Selection: Whisper / FunASR / Coming SoonYou can run the webui directly to get results. The page looks like this:Bash# WebUI
python webui.py
Updated the interface recently. We can freely choose the GPT-SoVITS fine-tuned model to implement, uploading reference audio to clone the voice well.Old VersionThis part is to ensure every part of the code is correct, so every module will be tested and improved first.There are several modes to start, allowing selection of specific scenarios.The first mode only has fixed character Q&A, with characters set up, saving preprocessing time.Bashpython app.py
Recently updated the first mode, adding Wav2Lip model for dialogue.Bashpython appv2.py
The second mode allows uploading any image for dialogue.Bashpython app_img.py
The third mode adds Large Language Models based on the first mode, adding multi-turn GPT dialogue.Bashpython app_multi.py
Now added voice cloning part, allowing free switching of cloned voice models and corresponding person images. Here I chose a husky voice and a male image.Bashpython app_vits.py
Added a fourth mode, allowing dialogue without fixed scenarios, directly inputting voice or generating voice for digital human generation. Built-in Sadtalker, Wav2Lip, ER-NeRF, etc.ER-NeRF is trained on a single person's video, so specific models need to be replaced to render correct results. Obama weights are built-in and can be used directly.Bashpython app_talk.py
Added MuseTalk method, capable of preprocessing MuseV videos. After preprocessing, dialogue can be conducted. The speed basically meets real-time requirements and is very fast. MuseTalk has been added to WebUI.Bashpython app_musetalk.py
Folder Structure[!NOTE]All weight parts can be downloaded here. Baidu Netdisk might update slowly sometimes. It is recommended to download from Quark Netdisk for the earliest updates.Baidu (Baidu Netdisk) (Password: linl)huggingfacemodelscopeQuark(Quark Netdisk)Weight folder structure is as follows:BashLinly-Talker/ 
├── checkpoints
│   ├── audio_visual_encoder.pth
│   ├── hub
│   │   └── checkpoints
│   │       └── s3fd-619a316812.pth
│   ├── lipsync_expert.pth
│   ├── mapping_00109-model.pth.tar
│   ├── mapping_00229-model.pth.tar
│   ├── May.json
│   ├── May.pth
│   ├── Obama_ave.pth
│   ├── Obama.json
│   ├── Obama.pth
│   ├── ref_eo.npy
│   ├── ref.npy
│   ├── ref.wav
│   ├── SadTalker_V0.0.2_256.safetensors
│   ├── visual_quality_disc.pth
│   ├── wav2lip_gan.pth
│   └── wav2lip.pth
├── gfpgan
│   └── weights
│       ├── alignment_WFLW_4HG.pth
│       └── detection_Resnet50_Final.pth
├── GPT_SoVITS
│   └── pretrained_models
│       ├── chinese-hubert-base
│       │   ├── config.json
│       │   ├── preprocessor_config.json
│       │   └── pytorch_model.bin
│       ├── chinese-roberta-wwm-ext-large
│       │   ├── config.json
│       │   ├── pytorch_model.bin
│       │   └── tokenizer.json
│       ├── README.md
│       ├── s1bert25hz-2kh-longer-epoch=68e-step=50232.ckpt
│       ├── s2D488k.pth
│       ├── s2G488k.pth
│       └── speech_paraformer-large_asr_nat-zh-cn-16k-common-vocab8404-pytorch
├── MuseTalk
│   ├── models
│   │   ├── dwpose
│   │   │   └── dw-ll_ucoco_384.pth
│   │   ├── face-parse-bisent
│   │   │   ├── 79999_iter.pth
│   │   │   └── resnet18-5c106cde.pth
│   │   ├── musetalk
│   │   │   ├── musetalk.json
│   │   │   └── pytorch_model.bin
│   │   ├── README.md
│   │   ├── sd-vae-ft-mse
│   │   │   ├── config.json
│   │   │   └── diffusion_pytorch_model.bin
│   │   └── whisper
│   │       └── tiny.pt
├── Qwen
│   └── Qwen-1_8B-Chat
│       ├── assets
│       │   ├── logo.jpg
│       │   ├── qwen_tokenizer.png
│       │   ├── react_showcase_001.png
│       │   ├── react_showcase_002.png
│       │   └── wechat.png
│       ├── cache_autogptq_cuda_256.cpp
│       ├── cache_autogptq_cuda_kernel_256.cu
│       ├── config.json
│       ├── configuration_qwen.py
│       ├── cpp_kernels.py
│       ├── examples
│       │   └── react_prompt.md
│       ├── generation_config.json
│       ├── LICENSE
│       ├── model-00001-of-00002.safetensors
│       ├── model-00002-of-00002.safetensors
│       ├── modeling_qwen.py
│       ├── model.safetensors.index.json
│       ├── NOTICE
│       ├── qwen_generation_utils.py
│       ├── qwen.tiktoken
│       ├── README.md
│       ├── tokenization_qwen.py
│       └── tokenizer_config.json
├── Whisper
│   ├── base.pt
│   └── tiny.pt
├── FunASR
│   ├── punc_ct-transformer_zh-cn-common-vocab272727-pytorch
│   │   ├── configuration.json
│   │   ├── config.yaml
│   │   ├── example
│   │   │   └── punc_example.txt
│   │   ├── fig
│   │   │   └── struct.png
│   │   ├── model.pt
│   │   ├── README.md
│   │   └── tokens.json
│   ├── speech_fsmn_vad_zh-cn-16k-common-pytorch
│   │   ├── am.mvn
│   │   ├── configuration.json
│   │   ├── config.yaml
│   │   ├── example
│   │   │   └── vad_example.wav
│   │   ├── fig
│   │   │   └── struct.png
│   │   ├── model.pt
│   │   └── README.md
│   └── speech_seaco_paraformer_large_asr_nat-zh-cn-16k-common-vocab8404-pytorch
│       ├── am.mvn
│       ├── asr_example_hotword.wav
│       ├── configuration.json
│       ├── config.yaml
│       ├── example
│       │   ├── asr_example.wav
│       │   └── hotword.txt
│       ├── fig
│       │   ├── res.png
│       │   └── seaco.png
│       ├── model.pt
│       ├── README.md
│       ├── seg_dict
│       └── tokens.json
└── README.md
ReferencesASRhttps://github.com/openai/whisperhttps://github.com/alibaba-damo-academy/FunASRTTShttps://github.com/rany2/edge-tts  https://github.com/PaddlePaddle/PaddleSpeechLLMhttps://github.com/CVI-SZU/Linlyhttps://github.com/QwenLM/Qwenhttps://deepmind.google/technologies/gemini/https://github.com/THUDM/ChatGLM3https://openai.comTHGhttps://github.com/OpenTalker/SadTalkerhttps://github.com/Rudrabha/Wav2Liphttps://github.com/Fictionarry/ER-NeRFVoice Clonehttps://github.com/RVC-Boss/GPT-SoVITShttps://github.com/coqui-ai/TTSLicense[!CAUTION]When using this tool, please comply with relevant laws, including copyright laws, data protection laws, and privacy laws. Do not use this tool without permission from the original author and/or copyright holder.Linly-Talker follows the MIT License. When using this tool, please comply with relevant laws, including copyright laws, data protection laws, and privacy laws. Do not use this tool without permission from the original author and/or copyright holder. Do not use this tool without permission from the original author and/or copyright holder. Additionally, please ensure compliance with all license agreements of the models and components you reference.