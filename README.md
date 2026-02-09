## 🎥 Demo Video

[![Linly-Gemini Live Demo](https://img.youtube.com/vi/z6SfvnNrRPQ/0.jpg)](https://www.youtube.com/watch?v=z6SfvnNrRPQ)




# 🎭 Linly-Gemini Live: Real-Time AI Avatar(PersonasAI)

<div align="center">

![Python](https://img.shields.io/badge/Python-3.10-blue?style=for-the-badge&logo=python&logoColor=white)
![PyTorch](https://img.shields.io/badge/PyTorch-2.1.2-EE4C2C?style=for-the-badge&logo=pytorch&logoColor=white)
![Gradio](https://img.shields.io/badge/Gradio-4.44.0-orange?style=for-the-badge&logo=gradio&logoColor=white)
![Gemini](https://img.shields.io/badge/Gemini-Live-4285F4?style=for-the-badge&logo=google&logoColor=white)
![License](https://img.shields.io/badge/License-MIT-green?style=for-the-badge)



![ARCHITECTURE](https://i.ibb.co/mjH6rkJ/Whats-App-Image-2026-02-10-at-3-07-12-AM.jpg)


**A real-time, conversational AI avatar powered by Google's Gemini Live and TMElyralab's MuseTalk.**

[🚀 **Live Demo on Hugging Face**](https://huggingface.co/spaces/eshwar06/personaxgemini)

</div>

---

## ✨ Features

- **🗣️ Real-Time Interaction**: Engage in seamless voice conversations with ultra-low latency powered by Gemini Live.
- **👄 Lip-Sync Animation**: Uses **MuseTalk** to generate realistic lip movements synced perfectly to the AI's audio response.
- **👤 Custom Avatars**: Upload any portrait image or video to create your own unique persona instantly.
- **🔄 Self-Healing Deployment**: Automatically detects and downloads missing model weights at runtime, ensuring robust deployments on Hugging Face Spaces.
- **🛠️ Zero-Config Interface**: Simple 2-button UI meant for immediate interaction—just "Start Streaming" and go.

---

## 🏗️ Architecture

This project combines state-of-the-art storage, inference, and LLM technologies:

1.  **Frontend (Gradio)**: Captures microphone input and renders the video stream.
2.  **Orchestrator (Python)**: manages the WebSocket connection and audio buffering.
3.  **Brain (Gemini Live)**: Processes audio input and generates intelligent, conversational audio responses via a dedicated WebSocket bridge (hosted on Railway).
4.  **Face Engine (MuseTalk)**: Takes the audio from Gemini and the video frames of the avatar to generate lip-synced video in real-time.





