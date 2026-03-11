# Lightweight Script AI API (Render Optimized)

Generate video scripts from articles using AI (DistilGPT2) - Optimized for Render Free Tier.

## Features

- REST API for script generation
- Uses DistilGPT2 (82M params) - smallest GPT-2 variant
- **Optimized for 450MB RAM** (stays under 500MB Render limit)
- CPU-only inference (no CUDA dependencies)
- Lazy model loading with idle timeout
- Memory monitoring endpoints
- Input/output size limits
- Automatic garbage collection

## API Endpoints

### GET /
Service info, memory usage, and limits

### GET /health
Health check with memory status

### GET /memory
Detailed memory usage statistics

### POST /generate
Generate video script from article

**Request:**
```json
{
  "text": "The government announced major reforms today...",
  "max_length": 200
}
```

**Response:**
```json
{
  "success": true,
  "script": "What just happened could affect millions...",
  "input_length": 45,
  "output_length": 150,
  "memory_usage": {
    "before_mb": 120.5,
    "after_mb": 180.2,
    "delta_mb": 59.7
  }
}
```

## Limits (Render Free Tier)

- **Max input**: 2000 characters
- **Max generation**: 300 tokens
- **Target memory**: < 450MB
- **Model idle timeout**: 5 minutes

## Local Testing

```bash
# Install dependencies (CPU-only torch)
pip install -r requirements.txt

# Run server
python main.py

# Test with curl
curl -X POST http://localhost:8000/generate \
  -H "Content-Type: application/json" \
  -d '{"text": "Breaking news today...", "max_length": 200}'

# Check memory
curl http://localhost:8000/memory
```

## Deploy to Render

1. Push to GitHub
2. Create new Web Service on Render
3. Connect repository
4. Render will use `render.yaml` automatically
5. Wait for build (~5 minutes)

## Performance (Optimized)

- **Cold start**: 30-60s (model downloads on first request)
- **Response time**: 5-15s
- **RAM usage**: ~300-400MB
- **Model**: DistilGPT2 (82M params, CPU-only)
- **Dependencies**: 4 packages only

## Architecture

```
Client → FastAPI → Memory Monitor → Script Engine → DistilGPT2 → JSON Response
                     ↑
                Garbage Collection
                     ↑
                Idle Timeout (5min)
```

## Files

- `main.py` - FastAPI server with memory monitoring
- `model_loader.py` - Lazy model loading with idle timeout
- `script_engine.py` - Script generation with memory cleanup
- `requirements.txt` - Minimal dependencies (CPU-only torch)
- `render.yaml` - Render config with memory optimizations
- `start.sh` - Startup script (single worker)
- `test_local.py` - Comprehensive local testing

## Render Optimization Features

✅ **CPU-only torch** - Saves ~500MB  
✅ **Lazy loading** - Model loads on first request only  
✅ **Idle timeout** - Unloads model after 5 minutes idle  
✅ **Memory monitoring** - Real-time RAM tracking  
✅ **Input limits** - Prevents memory spikes  
✅ **Single worker** - Avoids memory duplication  
✅ **Garbage collection** - Automatic memory cleanup  
✅ **Temp cache** - Uses /tmp for model storage
