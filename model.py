import os
import gc

# Standardize Model Path
MODEL_DIR = "models"
MODEL_FILENAME = "qwen2.5-0.5b-instruct-q2_k.gguf"
MODEL_PATH = os.path.join(MODEL_DIR, MODEL_FILENAME)

# Google Drive file id for the GGUF
FILE_ID = "1iwluL_LzkdMxx7VgUw3gaCxDectPCTo8"

# Rough sanity check: GGUF should be far larger than 10MB.
MIN_MODEL_SIZE_BYTES = 10 * 1024 * 1024

def _model_is_present_and_valid() -> bool:
    return os.path.exists(MODEL_PATH) and os.path.getsize(MODEL_PATH) > MIN_MODEL_SIZE_BYTES

def download_model(max_retries: int = 3, retry_sleep_s: int = 5) -> None:
    """
    Downloads the model if not present.
    Retries to reduce flakiness on Render build/start.
    """
    if _model_is_present_and_valid():
        return

    # Remove any partial/corrupt file
    os.makedirs(MODEL_DIR, exist_ok=True)
    if os.path.exists(MODEL_PATH) and os.path.getsize(MODEL_PATH) <= MIN_MODEL_SIZE_BYTES:
        try:
            os.remove(MODEL_PATH)
        except OSError:
            pass

    print(f"Model file missing or invalid. Downloading {MODEL_FILENAME}...")
    last_error: Exception | None = None

    try:
        import gdown  # type: ignore
    except ImportError as e:
        raise ImportError("gdown not installed. Please install it or place the model manually.") from e

    url = f"https://drive.google.com/uc?id={FILE_ID}"
    for attempt in range(1, max_retries + 1):
        try:
            print(f"Download attempt {attempt}/{max_retries}...")
            # gdown has its own retry logic; we still wrap it for network flakiness.
            gdown.download(url, MODEL_PATH, quiet=False)
            if not _model_is_present_and_valid():
                raise RuntimeError(
                    f"Download finished but file is still missing/too small. "
                    f"Size={os.path.getsize(MODEL_PATH) if os.path.exists(MODEL_PATH) else 'missing'}"
                )
            print("Model download succeeded.")
            return
        except Exception as e:  # noqa: BLE001
            last_error = e
            print(f"Download attempt {attempt} failed: {e}")
            if attempt < max_retries:
                import time
                time.sleep(retry_sleep_s)

    raise RuntimeError(f"Download failed after {max_retries} attempts: {last_error}")

def ensure_model_downloaded() -> None:
    """
    Ensures the GGUF exists on disk if DOWNLOAD_MODEL=1.
    Safe to call from Render start scripts (before uvicorn) and from app startup.
    """
    download_flag = os.getenv("DOWNLOAD_MODEL", "0")
    print(f"[model] ensure_model_downloaded(): DOWNLOAD_MODEL={download_flag}")
    print(f"[model] ensure_model_downloaded(): expecting {MODEL_PATH}")

    if _model_is_present_and_valid():
        print(f"[model] Model already present/valid: {MODEL_PATH}")
        return

    if download_flag != "1":
        print(f"[model] CRITICAL: Model file not found at {MODEL_PATH}")
        print("[model] Set DOWNLOAD_MODEL=1 or place the model manually.")
        raise FileNotFoundError(MODEL_PATH)

    print("[model] Model missing/invalid; starting download...")
    download_model()

def initialize_model():
    """
    Load the model with extreme memory constraints for Render's 400MB limit.
    """
    ensure_model_downloaded()
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
            logits_all=False,
        )
        return llm
    except Exception as e:  # noqa: BLE001
        raise RuntimeError(f"Critical error loading model: {e}") from e
