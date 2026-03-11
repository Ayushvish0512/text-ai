"""
Script generation engine combining rule-based logic + AI model.
"""
from model_loader import load_model, check_and_unload_idle
import logging
import gc

logger = logging.getLogger(__name__)

def generate_script(article_text: str, max_length: int = 200) -> str:
    """
    Generate video script from article text.
    
    Args:
        article_text: Input article text
        max_length: Maximum tokens to generate
    
    Returns:
        Generated script text
    """
    try:
        # Check and unload idle model before loading
        check_and_unload_idle()
        
        # Load model (lazy loading)
        tokenizer, model = load_model()
        
        # Create prompt for script generation
        prompt = f"""Convert this article into an engaging video script with hook, context, and call-to-action.

Article:
{article_text[:500]}

Video Script:"""
        
        # Tokenize input
        inputs = tokenizer(
            prompt,
            return_tensors="pt",
            truncation=True,
            max_length=512
        )
        
        logger.info("Generating script...")
        
        # Generate script with memory-efficient settings
        outputs = model.generate(
            **inputs,
            max_length=max_length,
            temperature=0.7,
            do_sample=True,
            top_p=0.9,
            pad_token_id=tokenizer.eos_token_id,
            no_repeat_ngram_size=2,  # Reduce repetition
            repetition_penalty=1.1,   # Encourage diversity
        )
        
        # Decode output
        result = tokenizer.decode(outputs[0], skip_special_tokens=True)
        
        # Extract only the generated part (after prompt)
        script = result.split("Video Script:")[-1].strip()
        
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
