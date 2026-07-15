from fastapi import FastAPI, HTTPException
from fastapi.responses import HTMLResponse, StreamingResponse
from pydantic import BaseModel
import subprocess
import os
from typing import Iterator

# Optional model download support (Render/testing)
from model import download_model

from fastapi.middleware.cors import CORSMiddleware


app = FastAPI()

# Allow your other website domain(s) to call this API from the browser
# Change origins to your real domains when deploying.
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

MODEL_PATH = "models/distilgpt2-q4_k_m.gguf"
LLAMA_BIN = "llama.cpp/main"


class Prompt(BaseModel):
    text: str
    max_length: int = 50


@app.get("/")
def health():
    return {"status": "running"}


@app.get("/chat")
def chat_page() -> HTMLResponse:
    page_path = os.path.join(os.path.dirname(__file__), "chat_page.html")
    with open(page_path, "r", encoding="utf-8") as f:
        return HTMLResponse(f.read())


@app.post("/generate")
def generate(prompt: Prompt):
    def stream() -> Iterator[str]:
        if not os.path.exists(MODEL_PATH):
            if os.getenv("DOWNLOAD_MODEL", "0") == "1":
                try:
                    # Downloads into ./models/ using gdown (network only when enabled)
                    download_model()
                except Exception as e:
                    raise HTTPException(
                        status_code=500,
                        detail=f"Model download failed: {e}",
                    )

            if not os.path.exists(MODEL_PATH):
                raise HTTPException(
                    status_code=500,
                    detail=f"Model file not found at {MODEL_PATH}. Please download and place it manually.",
                )

        n_tokens = str(min(prompt.max_length, 100))
        args = [
            LLAMA_BIN,
            "-m",
            MODEL_PATH,
            "-p",
            prompt.text,
            "-n",
            n_tokens,
            "--temp",
            "0.7",
            "--ctx-size",
            "128",
            "--no-display-prompt",
        ]

        try:
            # Stream stdout progressively
            proc = subprocess.Popen(
                args,
                stdout=subprocess.PIPE,
                stderr=subprocess.STDOUT,
                text=True,
                bufsize=1,  # line-buffered
            )

            start_cmd_failed = False
            for line in proc.stdout:  # type: ignore[union-attr]
                # yield as soon as there is output
                yield line

            ret = proc.wait(timeout=1)
            if ret != 0:
                # If llama.cpp exits non-zero, surface what we got (if any)
                if not start_cmd_failed:
                    yield ""
        except subprocess.TimeoutExpired:
            yield "\n[error] Generation timed out."
        except FileNotFoundError:
            yield "\n[error] llama.cpp binary not found. Expected: " + LLAMA_BIN
        except Exception as e:
            yield "\n[error] " + str(e)

    return StreamingResponse(stream(), media_type="text/plain; charset=utf-8")

