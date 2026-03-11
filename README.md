# Lightweight Script AI API

Generate video scripts from articles using AI (DistilGPT2).

## Features

- REST API for script generation
- Uses DistilGPT2 (82M params)
- Optimized for 500MB RAM
- Deployed on Render Free Tier

## API Endpoints

### GET /
Service info and available endpoints

### GET /health
Health check

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
  "output_length": 150
}
```

## Local Testing

```bash
# Install dependencies
pip install -r requirements.txt

# Run server
python main.py

# Test
curl -X POST http://localhost:8000/generate \
  -H "Content-Type: application/json" \
  -d '{"text": "Breaking news today..."}'
```

## Deploy to Render

1. Push to GitHub
2. Create new Web Service on Render
3. Connect repository
4. Render will use `render.yaml` automatically
5. Wait for build (~5 minutes)

## Performance

- Cold start: 30-60s
- Response time: 5-15s
- RAM usage: ~350MB
- Model: DistilGPT2 (82M params)

## Architecture

```
Client → FastAPI → Script Engine → DistilGPT2 → JSON Response
```

## Files

- `main.py` - FastAPI server
- `model_loader.py` - Lazy model loading
- `script_engine.py` - Script generation logic
- `requirements.txt` - Dependencies
- `render.yaml` - Render config
- `start.sh` - Startup script
