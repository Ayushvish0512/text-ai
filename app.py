from fastapi import FastAPI, Request
from fastapi.responses import JSONResponse
import subprocess
import os
import asyncio
import logging

# Configure logging
logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

app = FastAPI(
    title="Tiny LLM API",
    docs_url=None,
    redoc_url=None,
    openapi_url=None
)

MODEL_PATH = "models/distilgpt2-q4_k_m.gguf"
LLAMA_BIN = "./llama.cpp/llama-cli"

# Verify model exists on startup
@app.on_event("startup")
async def startup_event():
    if not os.path.exists(MODEL_PATH):
        logger.error(f"Model not found at {MODEL_PATH}")
    if not os.path.exists(LLAMA_BIN):
        logger.error(f"llama-cli not found at {LLAMA_BIN}")
    logger.info("Server started successfully")

@app.get("/")
async def health():
    """Health check endpoint"""
    return {
        "status": "ok",
        "model": "distilgpt2-82M-q4",
        "memory_optimized": True
    }

@app.post("/generate")
async def generate(request: Request):
    """Generate text completion"""
    try:
        data = await request.json()
        text = data.get("text", "").strip()
        max_length = min(int(data.get("max_length", 50)), 100)
        
        if not text:
            return JSONResponse(
                {"error": "text field is required"},
                status_code=400
            )
        
        logger.info(f"Generating text for prompt: {text[:50]}...")
        
        # Run llama.cpp in thread pool
        loop = asyncio.get_event_loop()
        result = await loop.run_in_executor(
            None,
            lambda: subprocess.run(
                [
                    LLAMA_BIN,
                    "-m", MODEL_PATH,
                    "-p", text,
                    "-n", str(max_length),
                    "--temp", "0.7",
                    "--ctx-size", "128",
                    "--threads", "1",
                    "--no-display-prompt",
                    "--log-disable"
                ],
                capture_output=True,
                text=True,
                timeout=30
            )
        )
        
        if result.returncode != 0:
            logger.error(f"llama.cpp error: {result.stderr}")
            return JSONResponse(
                {"error": "generation failed", "details": result.stderr[:200]},
                status_code=500
            )
        
        output = result.stdout.strip()
        logger.info(f"Generated {len(output)} characters")
        
        return {
            "response": output,
            "prompt": text,
            "length": len(output)
        }
        
    except asyncio.TimeoutError:
        logger.error("Generation timeout")
        return JSONResponse(
            {"error": "request timeout - try shorter prompt or max_length"},
            status_code=504
        )
    except ValueError as e:
        return JSONResponse(
            {"error": f"invalid input: {str(e)}"},
            status_code=400
        )
    except Exception as e:
        logger.error(f"Unexpected error: {str(e)}")
        return JSONResponse(
            {"error": "internal server error"},
            status_code=500
        )

if __name__ == "__main__":
    import uvicorn
    port = int(os.environ.get("PORT", 8000))
    uvicorn.run(
        app,
        host="0.0.0.0",
        port=port,
        workers=1,
        log_level="info"
    )
