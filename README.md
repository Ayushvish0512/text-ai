# Tiny LLM API - Production Ready

Ultra-lightweight FastAPI service running distilgpt2 (82M params) optimized for Render free tier (400MB RAM).

## 🚀 Features

- **Minimal memory footprint**: ~155MB total usage
- **Production-ready**: Error handling, logging, health checks
- **Async processing**: Non-blocking inference
- **Memory optimized**: Single worker, limited concurrency
- **No Python ML libraries**: Uses llama.cpp binary directly

## 📊 Memory Breakdown

| Component | Memory Usage |
|-----------|--------------|
| FastAPI + Uvicorn | ~50MB |
| Model (distilgpt2 Q4) | ~35MB |
| llama.cpp runtime | ~50MB |
| Context buffer (128) | ~20MB |
| **Total** | **~155MB** |

Leaves ~245MB buffer for OS and overhead on 400MB RAM.

## 🛠️ Local Development

### Prerequisites
- Python 3.11+
- Git
- Make (for building llama.cpp)
- curl

### Setup

```bash
# Install Python dependencies
pip install -r requirements.txt

# Download model (35MB)
mkdir -p models
curl -L -o models/distilgpt2-q4_k_m.gguf \
  https://huggingface.co/Crataco/distilgpt2-82M-GGUF/resolve/main/distilgpt2-q4_k_m.gguf

# Clone and build llama.cpp
git clone --depth 1 https://github.com/ggerganov/llama.cpp.git
cd llama.cpp
make llama-cli LLAMA_NO_ACCELERATE=1 LLAMA_NO_METAL=1 LLAMA_OPENBLAS=0
cd ..

# Run server
python app.py
```

Server will start on http://localhost:8000

### Testing

```bash
# Run test suite
python test_generate.py

# Or manual tests
curl http://localhost:8000/

curl -X POST http://localhost:8000/generate \
  -H "Content-Type: application/json" \
  -d '{"text": "Hello world", "max_length": 30}'
```

## 🌐 API Endpoints

### GET /
Health check endpoint

**Response:**
```json
{
  "status": "ok",
  "model": "distilgpt2-82M-q4",
  "memory_optimized": true
}
```

### POST /generate
Generate text completion

**Request:**
```json
{
  "text": "Your prompt here",
  "max_length": 50
}
```

**Parameters:**
- `text` (required): Input prompt text
- `max_length` (optional): Max tokens to generate (default: 50, max: 100)

**Response:**
```json
{
  "response": "Generated text...",
  "prompt": "Your prompt here",
  "length": 45
}
```

**Error Responses:**
- `400`: Invalid input (missing text, invalid max_length)
- `500`: Generation failed
- `504`: Request timeout (reduce max_length)

## 🚢 Deploy to Render

### Automatic Deployment (Recommended)

1. Push code to GitHub
2. Go to [Render Dashboard](https://dashboard.render.com/)
3. Click "New +" → "Web Service"
4. Connect your repository
5. Render will auto-detect `render.yaml`
6. Click "Create Web Service"
7. Wait 5-10 minutes for build

### Verify Deployment

```bash
# Replace with your Render URL
curl https://your-app.onrender.com/

curl -X POST https://your-app.onrender.com/generate \
  -H "Content-Type: application/json" \
  -d '{"text": "Hello", "max_length": 20}'
```

## ⚙️ Configuration

### Memory Optimization Settings

In `start.sh`:
- `--workers 1`: Single worker process
- `--limit-concurrency 2`: Max 2 concurrent requests
- `--timeout-keep-alive 5`: Close idle connections quickly
- `--no-access-log`: Reduce logging overhead

In `app.py`:
- `--ctx-size 128`: Minimal context window
- `--threads 1`: Single thread inference
- `timeout=30`: 30s max per request

### Alternative Models

If you need even less memory:

**TinyStories 15M (smallest)**
```bash
curl -L -o models/tinystories-15m.gguf \
  https://huggingface.co/karpathy/tinyllamas/resolve/main/stories15M.bin
```

**DistilGPT2 Q2 (lower quality, less memory)**
```bash
curl -L -o models/distilgpt2-q2.gguf \
  https://huggingface.co/Crataco/distilgpt2-82M-GGUF/resolve/main/distilgpt2-q2_k.gguf
```

Update `MODEL_PATH` in `app.py` accordingly.

## 🐛 Troubleshooting

### Build fails on Render
- Check build logs for specific errors
- Ensure llama.cpp compiles successfully
- Verify model downloads completely

### Memory errors
- Switch to smaller model (TinyStories 15M)
- Reduce `--ctx-size` to 64
- Lower `--limit-concurrency` to 1

### Timeout errors
- Reduce `max_length` in requests
- Increase timeout in `app.py` (but watch memory)
- Use shorter prompts

### Slow responses
- Expected on 0.1 CPU free tier
- Consider caching common prompts
- Upgrade to paid tier for better performance

## 📝 Production Checklist

- [x] Minimal dependencies (no numpy, no torch)
- [x] Memory optimization flags
- [x] Error handling and logging
- [x] Health check endpoint
- [x] Request validation
- [x] Timeout protection
- [x] Async processing
- [x] Production-ready uvicorn config
- [x] Git ignore for models/binaries

## 📄 License

MIT License - feel free to use for your projects!
