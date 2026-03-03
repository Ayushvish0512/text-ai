from flask import Flask, request, jsonify
from transformers import AutoModelForCausalLM, AutoTokenizer
import torch

app = Flask(__name__)

model_name = "distilgpt2"

tokenizer = AutoTokenizer.from_pretrained(model_name)
model = AutoModelForCausalLM.from_pretrained(model_name)

@app.route("/generate", methods=["POST"])
def generate():
    prompt = request.json.get("prompt", "")

    inputs = tokenizer(prompt, return_tensors="pt")
    outputs = model.generate(**inputs, max_length=100)

    text = tokenizer.decode(outputs[0], skip_special_tokens=True)

    return jsonify({"response": text})

@app.route("/")
def home():
    return "Model is running!"

if __name__ == "__main__":
    app.run(host="0.0.0.0", port=10000)