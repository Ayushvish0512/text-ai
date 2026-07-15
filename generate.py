import re

def build_prompt(user_input: str) -> str:
    """
    Builds a prompt for the Qwen-2.5-Instruct model.
    """
    return (
        f"<|im_start|>system\nYou are a helpful assistant.<|im_end|>\n"
        f"<|im_start|>user\n{user_input}<|im_end|>\n"
        f"<|im_start|>assistant\n"
    )

def clean_chunk(text: str) -> str:
    """
    Cleans unwanted tokens from streaming chunks.
    """
    bad_tokens = ["<|im_start|>", "<|im_end|>", "<|endoftext|>"]
    for token in bad_tokens:
        text = text.replace(token, "")
    return text
