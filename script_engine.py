"""
Script generation engine combining rule-based logic + AI model.
"""
from model_loader import load_model
import logging

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
        
        # Generate script
        outputs = model.generate(
            **inputs,
            max_length=max_length,
            temperature=0.7,
            do_sample=True,
            top_p=0.9,
            pad_token_id=tokenizer.eos_token_id
        )
        
        # Decode output
        result = tokenizer.decode(outputs[0], skip_special_tokens=True)
        
        # Extract only the generated part (after prompt)
        script = result.split("Video Script:")[-1].strip()
        
        logger.info(f"Script generated: {len(script)} chars")
        
        return script
    
    except Exception as e:
        logger.error(f"Script generation error: {str(e)}")
        raise
