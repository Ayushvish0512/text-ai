import os
from contextlib import asynccontextmanager
from fastapi import FastAPI, Request, HTTPException
from fastapi.responses import HTMLResponse, StreamingResponse
from fastapi.middleware.cors import CORSMiddleware
from pydantic import BaseModel, Field
from typing import AsyncGenerator

from model import initialize_model
from generate import build_prompt, clean_chunk

# Global state
state = {}

@asynccontextmanager
async def lifespan(app: FastAPI):
    # Initialize model once at startup
    # This will fail fast if model is missing and DOWNLOAD_MODEL=0
    state["llm"] = initialize_model()
    yield
    # Cleanup
    state.clear()

app = FastAPI(lifespan=lifespan)

# Secure CORS: Replace "*" with specific domains in production
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["GET", "POST"],
    allow_headers=["*"],
)

class Prompt(BaseModel):
    text: str = Field(..., max_length=1000)
    max_length: int = Field(128, ge=1, le=512)

@app.get("/")
def health():
    return {"status": "running", "model": "loaded" if "llm" in state else "loading"}

@app.get("/chat")
def chat_page() -> HTMLResponse:
    # Use absolute path relative to this file
    base_dir = os.path.dirname(os.path.abspath(__file__))
    page_path = os.path.join(base_dir, "chat_page.html")
    try:
        with open(page_path, "r", encoding="utf-8") as f:
            return HTMLResponse(f.read())
    except FileNotFoundError:
        raise HTTPException(status_code=404, detail="chat_page.html not found")

@app.post("/generate")
async def generate(prompt: Prompt):
    llm = state.get("llm")
    if not llm:
        # This shouldn't happen due to lifespan, but good for safety
        return StreamingResponse(iter(["[error] Model not loaded."]), media_type="text/plain")

    full_prompt = build_prompt(prompt.text)

    async def stream_generator() -> AsyncGenerator[str, None]:
        try:
            # Token-by-token streaming
            response_iter = llm.create_completion(
                prompt=full_prompt,
                max_tokens=prompt.max_length,
                stream=True,
                temperature=0.7,
                stop=["<|im_end|>", "<|im_start|>", "<|endoftext|>"]
            )

            for chunk in response_iter:
                token = chunk["choices"][0]["text"]
                if token:
                    yield clean_chunk(token)
        except Exception as e:
            yield f"\n[error] Generation failed: {str(e)}"

    return StreamingResponse(stream_generator(), media_type="text/plain; charset=utf-8")
