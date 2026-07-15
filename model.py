import os
import gc
import sys

# Standardize Model Path
MODEL_DIR = "models"
MODEL_FILENAME = "qwen2.5-0.5b-instruct-q2_k.gguf"
MODEL_PATH = os.path.join(MODEL_DIR, MODEL_FILENAME)
FILE_ID = "1iwluL_LzkdMxx7VgUw3gaCxDectPCTo8"

def download_model():
    """
    Downloads the model if not present.
    """
    if os.path.exists(MODEL_PATH):
        if os.path.getsize(MODEL_PATH) > 10 * 1024 * 1024:
            return
        os.remove(MODEL_PATH)

    os.makedirs(MODEL_DIR, exist_ok=True)
    print(f"Model file missing. Downloading {MODEL_FILENAME}...")
    
    try:
        import gdown
        url = f"https://drive.google.com/uc?id={FILE_ID}"
        gdown.download(url, MODEL_PATH, quiet=False, fuzzy=True)
        if not os.path.exists(MODEL_PATH):
            raise RuntimeError("Download completed but file is missing.")
    except ImportError:
        raise ImportError("gdown not installed. Please install it or place the model manually.")
    except Exception as e:
        raise RuntimeError(f"Download failed: {e}")

def initialize_model():
    """
    Load the model with extreme memory constraints for Render's 400MB limit.
    """
    if not os.path.exists(MODEL_PATH):
        if os.getenv("DOWNLOAD_MODEL", "0") == "1":
            download_model()
        else:
            print(f"CRITICAL: Model file not found at {MODEL_PATH}")
            print("Set DOWNLOAD_MODEL=1 or place the model manually.")
            sys.exit(1) # Fail fast on startup

    gc.collect()

    from llama_cpp import Llama
    
    # RAM Optimizations for 400MB limit:
    # n_ctx=512: Small context to save KV cache RAM.
    # n_threads=2: CPU limit for Render free tier.
    # use_mmap=True: Map model into memory (essential for low RAM).
    try:
        llm = Llama(
            model_path=MODEL_PATH,
            n_ctx=512,           
            n_batch=32,         
            n_threads=2,
            use_mlock=False,
            use_mmap=True,      
            verbose=False,
            logits_all=False
        )
        return llm
    except Exception as e:
        print(f"Critical error loading model: {e}")
        sys.exit(1)
