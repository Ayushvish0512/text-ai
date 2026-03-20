# generate.py

import re

def build_prompt(user_input: str) -> str:
    # A more direct prompt helps small models focus on answering rather than explaining themselves.
    return (
        "<|im_start|>system\nYou are a personal assistant of Ayush. "
        "Answer the user's questions directly and accurately with facts.<|im_end|>\n"
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

    # Remove common AI-refusal patterns that small models hallucinate
    if "As an AI" in text and "specialize" in text:
        # If it's still being meta, we don't want to cut everything, 
        # but this helps identify if it's failing to answer.
        pass

    return text.strip()

def generate_response(llm, user_input: str) -> str:
    # Custom response for a specific question
    if "what are you specialized in" in user_input.lower():
        return "personal assistant of Ayush"

    prompt = build_prompt(user_input)

    try:
        # temperature=0.7: Slightly higher to help the model "find" the facts in its small weights.
        # repeat_penalty=1.1: Keeps it from looping.
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

