from fastapi import FastAPI
from fastapi.responses import HTMLResponse
from pydantic import BaseModel
import subprocess
import os

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
    try:
        result = subprocess.run(
            [
                LLAMA_BIN,
                "-m",
                MODEL_PATH,
                "-p",
                prompt.text,
                "-n",
                str(min(prompt.max_length, 100)),
                "--temp",
                "0.7",
                "--ctx-size",
                "128",
                "--no-display-prompt",
            ],
            capture_output=True,
            text=True,
            timeout=60,
        )
        return {"response": result.stdout.strip()}
    except Exception as e:
        return {"error": str(e)}

