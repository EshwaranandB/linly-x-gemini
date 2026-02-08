import os

# --- OPTIONAL IMPORTS (Handle Missing Modules Gracefully) ---
try:
    from .Linly import Linly
    linly_available = True
except ImportError:
    Linly = None
    linly_available = False
    print("⚠️ Linly module not available")

try:
    from .Gemini import Gemini
    gemini_available = True
except ImportError:
    Gemini = None
    gemini_available = False
    print("⚠️ Gemini (Standard) module not available")

# --- GEMINI LIVE EXPORT ---
# We export this so it can be imported via 'from LLM import GeminiLiveClient'
try:
    from .GeminiLive import GeminiLiveClient
except ImportError:
    print("⚠️ GeminiLive module not found in LLM package")

# --- MINIMAL LLM FACTORY CLASS ---
class LLM:
    def __init__(self, mode='offline'):
        self.mode = mode
        self.model = None
        
    def init_model(self, model_name, model_path='', api_key=None, proxy_url=None, prefix_prompt='Please answer in less than 25 words.\n\n'):
        """
        Initialize the selected LLM.
        Supports: Linly, Gemini (Standard), and Direct Reply.
        """
        if model_name == 'Linly' and linly_available:
            self.model = Linly(self.mode, model_path)
        
        elif model_name == 'Gemini' and gemini_available:
            self.model = Gemini(model_path, api_key, proxy_url)
            
        elif model_name == 'Direct Reply' or model_name == '直接回复 Direct Reply':
            # Bypass model, just echo/pass-through
            self.model = self
            
        else:
            print(f"⚠️ Model '{model_name}' not found or dependencies missing. Defaulting to Direct Reply.")
            self.model = self
            
        # Set prompt prefix if the underlying model supports it
        if hasattr(self.model, 'prefix_prompt'):
            self.model.prefix_prompt = prefix_prompt
            
        return self.model
    
    def chat(self, system_prompt, message, history):
        """
        Standard Chat Interface
        """
        if self.model and self.model != self:
            # Delegate to loaded model (Linly/Gemini)
            return self.model.chat(system_prompt, message, history)
        else:
            # Direct Reply Fallback
            response = self.generate(message, system_prompt)
            history.append((message, response))
            return response, history

    def generate(self, question, system_prompt=''):
        """
        Direct generation (Non-Chat)
        """
        # If we are in "Direct Reply" mode (self.model == self), just return the question/echo
        return question

    def clear_history(self):
        if self.model and self.model != self:
            if hasattr(self.model, 'clear_history'):
                self.model.clear_history()
