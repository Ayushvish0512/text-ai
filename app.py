from fastapi import FastAPI
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
    return {"status": "running"}

@app.post("/generate")
def generate(prompt: Prompt):
    try:
        result = subprocess.run(
            [LLAMA_BIN, "-m", MODEL_PATH, "-p", prompt.text, 
             "-n", str(prompt.max_length), "--temp", "0.7",
             "--ctx-size", "256", "--no-display-prompt"],
            capture_output=True,
            text=True,
            timeout=60
        )
        return {"response": result.stdout.strip()}
    except Exception as e:
        return {"error": str(e)}

if __name__ == "__main__":
    import uvicorn
    port = int(os.environ.get("PORT", 8000))
    uvicorn.run(app, host="0.0.0.0", port=port)
