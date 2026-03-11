"""
Script generation engine optimized for Render memory limits.
"""
from model_loader import load_model, check_and_unload_idle
import logging
import gc

logger = logging.getLogger(__name__)

def generate_script(article_text: str, max_length: int = 150) -> str:
    """
    Generate video script from article text.
    Optimized for memory efficiency on Render free tier.
    
    Args:
        article_text: Input article text (max 1000 chars)
        max_length: Maximum tokens to generate (max 150)
    
    Returns:
        Generated script text
    """
    try:
        # Check and unload idle model before loading
        check_and_unload_idle()
        
        # Load model (lazy loading)
        tokenizer, model = load_model()
        
        # Create prompt for script generation (shorter for memory)
        prompt = f"""Create a short video script from this article:

{article_text[:300]}

Script:"""
        
        # Tokenize input
        inputs = tokenizer(
            prompt,
            return_tensors="pt",
            truncation=True,
            max_length=256  # Shorter for memory
        )
        
        logger.info(f"Generating script ({max_length} tokens max)...")
        
        # Generate script with memory-efficient settings
        outputs = model.generate(
            **inputs,
            max_length=max_length,
            temperature=0.7,
            do_sample=True,
            top_p=0.9,
            pad_token_id=tokenizer.eos_token_id,
            no_repeat_ngram_size=2,
            repetition_penalty=1.1,
        )
        
        # Decode output
        result = tokenizer.decode(outputs[0], skip_special_tokens=True)
        
        # Extract only the generated part (after "Script:")
        if "Script:" in result:
            script = result.split("Script:")[-1].strip()
        else:
            script = result.strip()
        
        # Clean up tensors to free memory
        del inputs
        del outputs
        gc.collect()
        
        logger.info(f"Script generated: {len(script)} chars")
        
        return script
    
    except Exception as e:
        logger.error(f"Script generation error: {str(e)}")
        # Force cleanup on error
        gc.collect()
        raise
