"""
Lazy model loader to prevent memory spikes.
Model loads only when first needed.
"""
import logging
import os
import time
import gc

logger = logging.getLogger(__name__)

tokenizer = None
model = None
last_used = None
MAX_IDLE_TIME = 300  # 5 minutes

def load_model():
    """
    Lazy load DistilGPT2 model.
    Only loads once, then reuses.
    """
    global tokenizer, model, last_used
    
    if model is None:
        logger.info("Loading DistilGPT2 model (first time only)...")
        
        try:
            from transformers import AutoTokenizer, AutoModelForCausalLM
            
            # Use distilgpt2 - smallest GPT2 variant
            model_name = "distilgpt2"
            
            logger.info(f"Loading tokenizer: {model_name}")
            tokenizer = AutoTokenizer.from_pretrained(model_name)
            
            logger.info(f"Loading model: {model_name}")
            model = AutoModelForCausalLM.from_pretrained(
                model_name,
                low_cpu_mem_usage=True,  # Memory optimization
                torch_dtype="auto"  # Auto-select dtype for memory efficiency
            )
            
            # Set pad token
            if tokenizer.pad_token is None:
                tokenizer.pad_token = tokenizer.eos_token
            
            logger.info("Model loaded successfully!")
            
        except Exception as e:
            logger.error(f"Failed to load model: {str(e)}")
            raise
    
    # Update last used time
    last_used = time.time()
    return tokenizer, model

def unload_model():
    """
    Unload model to free memory (if needed).
    """
    global tokenizer, model, last_used
    tokenizer = None
    model = None
    last_used = None
    
    # Force garbage collection
    gc.collect()
    
    logger.info("Model unloaded from memory")

def check_and_unload_idle():
    """
    Check if model has been idle too long and unload it.
    Returns True if model was unloaded.
    """
    global last_used
    
    if model is not None and last_used is not None:
        idle_time = time.time() - last_used
        if idle_time > MAX_IDLE_TIME:
            logger.info(f"Model idle for {idle_time:.0f}s, unloading...")
            unload_model()
            return True
    return False
