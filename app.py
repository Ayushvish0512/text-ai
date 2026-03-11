from fastapi import FastAPI, Request
from fastapi.responses import JSONResponse
import requests
import os

app = FastAPI(
    title="Tiny LLM API",
    docs_url=None,
    redoc_url=None,
    openapi_url=None
)

# Hugging Face Inference API - using 0.5B model
HF_API_URL = "https://router.huggingface.co/models/microsoft/phi-1"
HF_API_KEY = os.environ.get("HF_API_KEY", "")

@app.get("/")
async def health():
    return {
        "status": "ok",
        "model": "microsoft/phi-1 (0.5B params)",
        "memory_optimized": True
    }

@app.post("/generate")
async def generate(request: Request):
    try:
        data = await request.json()
        text = data.get("text", "").strip()
        max_length = min(int(data.get("max_length", 50)), 100)
        
        if not text:
            return JSONResponse(
                {"error": "text field is required"},
                status_code=400
            )
        
        headers = {}
        if HF_API_KEY:
            headers["Authorization"] = f"Bearer {HF_API_KEY}"
        
        payload = {
            "inputs": text,
            "parameters": {
                "max_new_tokens": max_length,
                "temperature": 0.7,
                "return_full_text": False
            }
        }
        
        response = requests.post(HF_API_URL, json=payload, headers=headers, timeout=580)
        
        if response.status_code == 200:
            result = response.json()
            generated_text = result[0]['generated_text'] if isinstance(result, list) else result.get('generated_text', '')
            return {
                "response": generated_text,
                "prompt": text,
                "length": len(generated_text)
            }
        else:
            return JSONResponse(
                {"error": f"API error: {response.status_code}", "details": response.text},
                status_code=response.status_code
            )
            
    except requests.Timeout:
        return JSONResponse(
            {"error": "request timeout"},
            status_code=504
        )
    except Exception as e:
        return JSONResponse(
            {"error": str(e)},
            status_code=500
        )

if __name__ == "__main__":
    import uvicorn
    port = int(os.environ.get("PORT", 8000))
    uvicorn.run(app, host="0.0.0.0", port=port)
