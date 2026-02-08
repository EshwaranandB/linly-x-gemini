import queue
import numpy as np
import threading
import time

class AudioBuffer:
    def __init__(self, sample_rate=16000, context_size_seconds=0.2):
        self.sample_rate = sample_rate
        self.window_size = int(sample_rate * context_size_seconds)
        self.buffer = np.zeros(self.window_size, dtype=np.float32)
        self.input_queue = queue.Queue()
        
    def push(self, audio_chunk):
        """Add new audio chunk to the queue"""
        self.input_queue.put(audio_chunk)
        
    def get_window(self):
        """
        Updates the rolling buffer with new audio (if available) 
        and returns the current window for inference.
        """
        try:
            # Try to get new audio (non-blocking)
            new_chunk = self.input_queue.get_nowait()
            
            # Shift buffer left
            chunk_len = len(new_chunk)
            self.buffer = np.roll(self.buffer, -chunk_len)
            
            # Insert new audio at the end
            self.buffer[-chunk_len:] = new_chunk
            
            return self.buffer
        except queue.Empty:
            # If no new audio, we return None (or silence depending on logic)
            # For streaming avatar, we usually return None to signal "no change"
            return None
