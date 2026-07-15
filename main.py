from fastapi import FastAPI, Request
from fastapi.responses import HTMLResponse
from pydantic import BaseModel
import subprocess
import os

app = FastAPI()

MODEL_PATH = "models/distilgpt2-q4_k_m.gguf"
LLAMA_BIN = "llama.cpp/main"

class Prompt(BaseModel):
    text: str
    max_length: int = 50


@app.get("/")
def health():
    # Keep a small JSON response for health checks
    return {"status": "running"}


@app.get("/chat")
def chat_page() -> HTMLResponse:
    # Serve a simple web chat UI
    page_path = os.path.join(os.path.dirname(__file__), "chat_page.html")
    with open(page_path, "r", encoding="utf-8") as f:
        return HTMLResponse(f.read())


@app.post("/generate")
def generate(prompt: Prompt):
    try:
        result = subprocess.run(
            [
                LLAMA_BIN,
                "-m",
                MODEL_PATH,
                "-p",
                prompt.text,
                "-n",
                str(prompt.max_length),
                "--temp",
                "0.7",
                "--ctx-size",
                "256",
                "--no-display-prompt",
            ],
            capture_output=True,
            text=True,
            timeout=60,
        )
        return {"response": result.stdout.strip()}
    except Exception as e:
        return {"error": str(e)}

