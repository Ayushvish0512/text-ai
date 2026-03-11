from fastapi import FastAPI, HTTPException
from pydantic import BaseModel
from script_engine import generate_script
import logging
import os
import psutil
import gc

logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

app = FastAPI(
    title="Lightweight Script AI API",
    description="Generate video scripts from articles using AI (Optimized for Render Free Tier)",
    version="1.0.0"
)

# Memory limits for Render free tier
MAX_INPUT_LENGTH = 1000  # characters (reduced from 2000)
MAX_GENERATION_LENGTH = 150  # tokens (reduced from 300)
MAX_MEMORY_MB = 450  # Stay under 500MB

class ArticleInput(BaseModel):
    text: str
    max_length: int = 200

def get_memory_usage():
    """Get current memory usage in MB"""
    try:
        process = psutil.Process(os.getpid())
        return process.memory_info().rss / 1024 / 1024
    except:
        return 0

@app.get("/")
def home():
    memory_mb = get_memory_usage()
    return {
        "status": "running",
        "service": "Lightweight Script AI API",
        "model": "distilgpt2",
        "memory_usage_mb": round(memory_mb, 1),
        "limits": {
            "max_input_chars": MAX_INPUT_LENGTH,
            "max_generation_tokens": MAX_GENERATION_LENGTH,
            "max_memory_mb": MAX_MEMORY_MB
        },
        "endpoints": {
            "generate": "/generate",
            "health": "/health",
            "memory": "/memory"
        }
    }

@app.get("/health")
def health():
    memory_mb = get_memory_usage()
    return {
        "status": "healthy",
        "memory_optimized": True,
        "memory_mb": round(memory_mb, 1),
        "under_limit": memory_mb < MAX_MEMORY_MB
    }

@app.get("/memory")
def memory():
    """Memory usage endpoint"""
    memory_mb = get_memory_usage()
    
    # Force garbage collection
    gc.collect()
    
    return {
        "memory_mb": round(memory_mb, 1),
        "max_limit_mb": MAX_MEMORY_MB,
        "under_limit": memory_mb < MAX_MEMORY_MB,
        "percentage_used": round((memory_mb / MAX_MEMORY_MB) * 100, 1) if MAX_MEMORY_MB > 0 else 0
    }

@app.post("/generate")
def generate(data: ArticleInput):
    try:
        # Input validation
        if not data.text or len(data.text.strip()) < 10:
            raise HTTPException(status_code=400, detail="Article text too short (min 10 chars)")
        
        if len(data.text) > MAX_INPUT_LENGTH:
            raise HTTPException(
                status_code=400, 
                detail=f"Article too long ({len(data.text)} chars). Max: {MAX_INPUT_LENGTH}"
            )
        
        if data.max_length > MAX_GENERATION_LENGTH:
            raise HTTPException(
                status_code=400,
                detail=f"Max length too high ({data.max_length}). Max: {MAX_GENERATION_LENGTH}"
            )
        
        # Check memory before generation
        memory_before = get_memory_usage()
        if memory_before > MAX_MEMORY_MB:
            logger.warning(f"High memory before generation: {memory_before:.1f}MB")
            # Force GC
            gc.collect()
        
        logger.info(f"Generating script for article: {data.text[:50]}...")
        
        script = generate_script(data.text, max_length=data.max_length)
        
        # Check memory after generation
        memory_after = get_memory_usage()
        
        return {
            "success": True,
            "script": script,
            "input_length": len(data.text),
            "output_length": len(script),
            "memory_usage": {
                "before_mb": round(memory_before, 1),
                "after_mb": round(memory_after, 1),
                "delta_mb": round(memory_after - memory_before, 1)
            }
        }
    
    except Exception as e:
        logger.error(f"Error generating script: {str(e)}")
        raise HTTPException(status_code=500, detail=f"Generation failed: {str(e)}")

if __name__ == "__main__":
    import uvicorn
    port = int(os.environ.get("PORT", 8000))
    uvicorn.run(app, host="0.0.0.0", port=port)
