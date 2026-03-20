# main.py

import logging
import gc
from fastapi import FastAPI, Query, HTTPException
from model import initialize_model
from generate import generate_response

# Configure logging
logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

app = FastAPI(
    title="Lightweight LLM API",
    description="A memory-optimized LLM serving TinyLlama or similar small models.",
    version="1.0.0"
)

# Global LLM instance
llm = None

@app.on_event("startup")
def startup_event():
    global llm
    logger.info("Initializing model...")
    try:
        llm = initialize_model()
        logger.info("Model initialization complete.")
    except Exception as e:
        logger.error(f"Critical error during startup: {e}")

@app.get("/")
def health():
    """Health check endpoint."""
    return {
        "status": "online",
        "model_loaded": llm is not None,
        "memory_limit": "400MB"
    }

@app.get("/chat")
def chat(message: str = Query(..., description="User message")):
    """
    Chat endpoint.
    """
    if llm is None:
        raise HTTPException(status_code=503, detail="Model not loaded or failed to initialize.")

    try:
        logger.info(f"Generating response for: {message}")
        reply = generate_response(llm, message)

        # Manually trigger garbage collection after each request
        # to prevent RAM buildup that causes 'stuck after 3 outputs'.
        gc.collect()

        return {
            "user": message,
            "assistant": reply
        }
    except Exception as e:
        logger.error(f"Generation error: {e}")
        raise HTTPException(status_code=500, detail="Error generating response.")