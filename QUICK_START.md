# Quick Start Guide

Get your Tiny LLM API running in 5 minutes.

## Local Development

```bash
# 1. Setup (one time)
bash setup_local.sh

# 2. Start server
python app.py

# 3. Test
python test_generate.py
```

## Deploy to Render

```bash
# 1. Push to GitHub
git add .
git commit -m "Initial commit"
git push origin main

# 2. Deploy on Render
# - Go to https://dashboard.render.com
# - Click "New +" → "Web Service"
# - Connect your repo
# - Click "Create Web Service"
# - Wait 5-10 minutes

# 3. Test deployment
curl https://your-app.onrender.com/
```

## API Usage

```bash
# Health check
curl https://your-app.onrender.com/

# Generate text
curl -X POST https://your-app.onrender.com/generate \
  -H "Content-Type: application/json" \
  -d '{"text": "Hello world", "max_length": 30}'
```

## Memory Usage

```
FastAPI + Uvicorn:  ~50MB
Model (distilgpt2):  ~35MB
llama.cpp runtime:   ~50MB
Context buffer:      ~20MB
─────────────────────────────
Total:              ~155MB
Available:          ~245MB buffer
```

## Files Overview

```
app.py              - Main FastAPI application
requirements.txt    - Python dependencies (2 packages)
render.yaml         - Render deployment config
start.sh            - Production startup script
runtime.txt         - Python version
test_generate.py    - Test suite
setup_local.sh      - Local setup script
```

## Common Commands

```bash
# Local development
python app.py                    # Start server
python test_generate.py          # Run tests
pip install -r requirements.txt  # Install deps

# Git operations
git status                       # Check changes
git add .                        # Stage all
git commit -m "message"          # Commit
git push origin main             # Deploy

# Testing
curl http://localhost:8000/                    # Health
curl -X POST http://localhost:8000/generate \  # Generate
  -H "Content-Type: application/json" \
  -d '{"text": "test", "max_length": 20}'
```

## Troubleshooting

| Issue | Solution |
|-------|----------|
| Build fails | Check render.yaml, verify model URL |
| Memory error | Use smaller model or reduce ctx-size |
| Timeout | Reduce max_length or use shorter prompts |
| Slow response | Expected on 0.1 CPU, upgrade tier |
| Service sleeps | Free tier sleeps after 15 min inactivity |

## Key Settings

**Memory Optimized:**
- Single worker process
- 2 concurrent requests max
- Context size: 128 tokens
- Single thread inference

**Performance:**
- Response time: 5-30 seconds
- Max tokens: 100 per request
- Timeout: 30 seconds

## Support

- 📖 Full docs: `README.md`
- 🚀 Deployment: `DEPLOYMENT.md`
- ✅ Checklist: `PRODUCTION_CHECKLIST.md`
- 🔧 Render docs: https://render.com/docs

---

**Ready to deploy?** Follow the steps above and you'll be live in minutes! 🚀
