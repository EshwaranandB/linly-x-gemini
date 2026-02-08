import asyncio
import websockets
import json
import numpy as np
import librosa
import traceback
import logging

# Configure logging
logging.basicConfig(level=logging.INFO)
logger = logging.getLogger("GeminiLiveClient")

class GeminiLiveClient:
    def __init__(self, websocket_url="wss://gemini-live-bridge-production.up.railway.app/ws"):
        self.uri = websocket_url
        self.websocket = None
        self.running = False
        self.output_queue = asyncio.Queue() # Audio queue for Avatar (16kHz)
        
    async def connect(self):
        """Connects to the Railway Bridge"""
        try:
            self.websocket = await websockets.connect(self.uri)
            self.running = True
            logger.info(f"✅ Connected to {self.uri}")
            
            # Start the listener loop
            asyncio.create_task(self.receive_loop())
            return True
        except Exception as e:
            logger.error(f"❌ Connection Failed: {e}")
            return False

    async def send_audio(self, audio_chunk, original_sr=16000):
        """
        Sends user audio to the bridge.
        Expects numpy array. Resamples to 16k if needed.
        """
        if not self.websocket or not self.running:
            return

        try:
            # 1. Resample to 16kHz if input is different (Mic is often 44.1k or 48k)
            if original_sr != 16000:
                audio_chunk = librosa.resample(audio_chunk, orig_sr=original_sr, target_sr=16000)

            # 2. Convert to PCM16 Bytes (Gemini expects raw PCM)
            # Clip to valid range [-1, 1] before converting
            audio_chunk = np.clip(audio_chunk, -1.0, 1.0)
            pcm_bytes = (audio_chunk * 32767).astype(np.int16).tobytes()
            
            # 3. Send
            await self.websocket.send(pcm_bytes)
        except Exception as e:
            logger.error(f"Send Error: {e}")

    async def receive_loop(self):
        """
        Listens for Gemini audio -> Resamples (24k to 16k) -> Puts in Queue
        """
        logger.info("🎧 Listening for Gemini response...")
        while self.running:
            try:
                message = await self.websocket.recv()
                
                # Case A: Audio Data (Bytes)
                if isinstance(message, bytes):
                    # 1. Convert Bytes -> Numpy Float32
                    audio_np = np.frombuffer(message, dtype=np.int16).astype(np.float32) / 32767.0
                    
                    # 2. Resample 24kHz (Gemini Native) -> 16kHz (MuseTalk Native)
                    # We use a fast resample for realtime performance
                    audio_16k = librosa.resample(audio_np, orig_sr=24000, target_sr=16000)
                    
                    # 3. Push to Avatar Queue
                    await self.output_queue.put(audio_16k)

                # Case B: Control Messages (JSON)
                else:
                    data = json.loads(message)
                    if data.get("type") == "turn_complete":
                        logger.info("⚡ Turn Complete")

            except websockets.exceptions.ConnectionClosed:
                logger.warning("🔌 Disconnected from Bridge")
                self.running = False
                break
            except Exception as e:
                logger.error(f"Receive Error: {e}")
                break

    async def close(self):
        self.running = False
        if self.websocket:
            await self.websocket.close()
