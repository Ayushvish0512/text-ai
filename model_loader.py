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
            import torch
            
            # Use distilgpt2 - smallest GPT2 variant
            model_name = "distilgpt2"
            
            logger.info(f"Loading tokenizer: {model_name}")
            tokenizer = AutoTokenizer.from_pretrained(model_name)
            
            logger.info(f"Loading model: {model_name}")
            # Try to load with 8-bit quantization for maximum memory savings
            try:
                # First try with 8-bit quantization (saves ~50% memory)
                model = AutoModelForCausalLM.from_pretrained(
                    model_name,
                    low_cpu_mem_usage=True,
                    load_in_8bit=True,  # 8-bit quantization
                    device_map="auto"  # Automatically place layers
                )
                logger.info("Model loaded with 8-bit quantization")
            except Exception as e:
                logger.warning(f"8-bit quantization failed: {e}. Falling back to float16.")
                # Fallback to float16
                model = AutoModelForCausalLM.from_pretrained(
                    model_name,
                    low_cpu_mem_usage=True,
                    dtype=torch.float16  # Use half precision
                )
                logger.info("Model loaded with float16 (fallback)")
            
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
