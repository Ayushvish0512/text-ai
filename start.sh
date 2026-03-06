#!/bin/bash
set -e

echo "Starting Tiny LLM API..."

# Memory optimization
export PYTHONUNBUFFERED=1
export MALLOC_TRIM_THRESHOLD_=100000
export PYTHONDONTWRITEBYTECODE=1

# Verify files exist
if [ ! -f "models/distilgpt2-q4_k_m.gguf" ]; then
    echo "ERROR: Model file not found!"
    exit 1
fi

if [ ! -f "llama.cpp/llama-cli" ]; then
    echo "ERROR: llama-cli not found!"
    exit 1
fi

echo "Model and binary verified. Starting server..."

# Start uvicorn with production settings
exec uvicorn app:app \
    --host 0.0.0.0 \
    --port ${PORT:-8000} \
    --workers 1 \
    --limit-concurrency 2 \
    --timeout-keep-alive 5 \
    --log-level info \
    --no-access-log
