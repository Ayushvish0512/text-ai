# generate.py

def build_prompt(user_input: str) -> str:
    """
    Formats user input into a chatbot conversation prompt.
    """
    return f"""
You are a helpful AI assistant.

User: {user_input}
Assistant:
"""


def generate_response(llm, user_input: str) -> str:
    """
    Generates response from the model.
    """
    prompt = build_prompt(user_input)

    output = llm(
        prompt,
        max_tokens=150,
        stop=["User:", "Assistant:"]
    )

    return output["choices"][0]["text"].strip()