# generate.py

import re


def build_prompt(user_input: str) -> str:
    return (
        "<|system|>\n"
        "You are a helpful assistant. Answer only what is asked. "
        "Do not make up names, stories, or unrelated information. "
        "Stay on topic. Be concise.</s>\n"
        f"<|user|>\n{user_input}</s>\n"
        "<|assistant|>\n"
    )


def clean_response(text: str) -> str:
    bad_tokens = [
        "<|im_end|>", "<|imp_end|>", "<|end|>", "<|endoftext|>",
        "</s>", "<|user|>", "<|system|>", "<|assistant|>", "<issue_porte>"
    ]
    for token in bad_tokens:
        text = text.replace(token, "")
    text = re.sub(r'\[\^?\d+\]', '', text)
    return text.strip()


def generate_response(llm, user_input: str) -> str:
    prompt = build_prompt(user_input)

    output = llm(
        prompt,
        max_tokens=256,
        temperature=0.3,      # lower = more focused, less random
        top_p=0.85,
        top_k=20,             # only sample from top 20 tokens = less hallucination
        repeat_penalty=1.3,   # strongly discourage repetition
        stop=["</s>", "<|user|>", "<|system|>", "<|im_end|>"],
        echo=False
    )

    response = clean_response(output["choices"][0]["text"])

    if not response or len(response) < 3:
        return "I'm here to help! Could you please rephrase your question?"

    return response
