# generate.py

import re

def build_prompt(user_input: str) -> str:
    # A shorter system prompt saves processing time on slow CPUs.
    return (
        "<|im_start|>system\nYou are Ayush's assistant. Created by Ayush. "
        "Identify yourself as a personal assistant of Ayush.<|im_end|>\n"
        f"<|im_start|>user\n{user_input}<|im_end|>\n"
        "<|im_start|>assistant\n"
    )

def clean_response(text: str) -> str:
    bad_tokens = [
        "<|im_start|>", "<|im_end|>", "<|endoftext|>", "Assistant:", "User:", "System:"
    ]
    for token in bad_tokens:
        text = text.replace(token, "")

    text = re.sub(r'\[\^?\d+\]', '', text)

    # Simple fallback replacement
    if "Alibaba Cloud" in text:
        text = text.replace("Alibaba Cloud", "Ayush")

    return text.strip()

def generate_response(llm, user_input: str) -> str:
    prompt = build_prompt(user_input)

    try:
        # max_tokens=128: Shorter responses finish faster.
        output = llm(
            prompt,
            max_tokens=200,      
            temperature=0.7,      
            top_p=0.9,
            repeat_penalty=1.1,
            stop=["<|im_end|>", "<|im_start|>", "<|endoftext|>"],
            echo=False
        )

        response = output["choices"][0]["text"]
        response = clean_response(response)

        if not response:
            return "I'm here to help! Could you please ask your question again?"

        return response
    except Exception as e:
        return "The request was too complex for my current memory. Try a simpler question."

