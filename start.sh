#!/bin/bash
set -e

# Render and other platforms use the PORT environment variable
PORT="${PORT:-8000}"

echo "Ensuring model is downloaded (if DOWNLOAD_MODEL=1)..."
echo "DOWNLOAD_MODEL=${DOWNLOAD_MODEL:-0}"
echo "Expected model path: models/qwen2.5-0.5b-instruct-q2_k.gguf"

# Download-only; avoids loading into RAM during build/start.
python -c "from model import ensure_model_downloaded; ensure_model_downloaded(); print('Model ensure step finished')"

echo "Starting uvicorn..."
# --workers 1 is CRITICAL to stay under 400MB RAM.
exec uvicorn main:app --host 0.0.0.0 --port "$PORT" --workers 1
