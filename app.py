from fastapi import FastAPI
from pydantic import BaseModel
from transformers import pipeline

app = FastAPI()

# Load small model (distilgpt2)
generator = pipeline("text-generation", model="distilgpt2")

class Prompt(BaseModel):
    prompt: str
    max_length: int = 100

@app.get("/")
def home():
    return {"message": "Model is running"}

@app.post("/generate")
def generate_text(data: Prompt):
    result = generator(
        data.prompt,
        max_length=data.max_length,
        num_return_sequences=1
    )

    return {
        "response": result[0]["generated_text"]
    }

    """curl -X POST https://tiny-llm.onrender.com/generate \
-H "Content-Type: application/json" \
-d '{"prompt": "Breaking news:", "max_length": 80}'"""