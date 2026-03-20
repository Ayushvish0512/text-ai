# main.py

from fastapi import FastAPI, Query
from model import initialize_model
from generate import generate_response

app = FastAPI()

# Load model once at startup
llm = initialize_model()


@app.get("/")
def health():
    return {"status": "chatbot running"}


@app.get("/chat")
def chat(message: str = Query(..., description="User message")):
    """
    Chat endpoint.
    """
    reply = generate_response(llm, message)

    return {
        "user": message,
        "assistant": reply
    }