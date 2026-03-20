# model.py

import os
import sys
import gc

# Constants
MODEL_PATH = os.path.join("models", "qwen2.5-0.5b-instruct-q2_k.gguf")
FILE_ID = "1iwluL_LzkdMxx7VgUw3gaCxDectPCTo8"

def download_model():
    """
    Downloads the model if not present.
    """
    if os.path.exists(MODEL_PATH):
        if os.path.getsize(MODEL_PATH) > 10 * 1024 * 1024:
            return
        os.remove(MODEL_PATH)

    os.makedirs("models", exist_ok=True)
    print("Model file missing. Downloading from Google Drive...")
    
    try:
        import gdown
        url = f"https://drive.google.com/uc?id={FILE_ID}"
        gdown.download(url, MODEL_PATH, quiet=False, fuzzy=True)
    except ImportError:
        print("Error: gdown not installed. Please install it or place the model manually.")
        sys.exit(1)
    except Exception as e:
        print(f"Download failed: {e}")
        sys.exit(1)

def initialize_model():
    """
    Load the model with extreme memory constraints for Render's 400MB limit.
    """
    # Auto-download if missing
    if not os.path.exists(MODEL_PATH):
        download_model()

    gc.collect()

    from llama_cpp import Llama
    
    # RAM Optimizations:
    # n_ctx=512: Balanced for prompt/answer space.
    # n_batch=32: Small batch to prevent spikes.
    try:
        llm = Llama(
            model_path=MODEL_PATH,
            n_ctx=512,           
            n_batch=32,         
            n_threads=1,
            use_mlock=False,
            use_mmap=True,      
            verbose=False,
            logits_all=False
        )
        print("Model loaded successfully.")
        return llm
    except Exception as e:
        print(f"Critical error loading model: {e}")
        sys.exit(1)
