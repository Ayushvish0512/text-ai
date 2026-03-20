# model.py

import os
import sys

MODEL_PATH = os.path.join("models", "tinyllama.gguf")
FILE_ID = "1Q_PILsxyMDTK8yyF0j--eMzbeLN-YiMK"


def download_model():
    if os.path.exists(MODEL_PATH):
        size = os.path.getsize(MODEL_PATH)
        if size > 10 * 1024 * 1024:
            print("Model already present.")
            return
        else:
            print("Existing model file looks invalid, re-downloading...")
            os.remove(MODEL_PATH)

    os.makedirs("models", exist_ok=True)
    print("Downloading model from Google Drive...")

    import gdown
    url = f"https://drive.google.com/uc?id={FILE_ID}"
    gdown.download(url, MODEL_PATH, quiet=False, fuzzy=True)

    if not os.path.exists(MODEL_PATH) or os.path.getsize(MODEL_PATH) < 10 * 1024 * 1024:
        print("Download failed or file is invalid.")
        sys.exit(1)

    print(f"Download complete: {os.path.getsize(MODEL_PATH) // (1024*1024)} MB")


def initialize_model():
    download_model()

    from llama_cpp import Llama
    print("Loading model...")
    llm = Llama(
        model_path=MODEL_PATH,
        n_ctx=512,
        n_threads=2,
        use_mlock=False
    )
    print("Model loaded.")
    return llm
