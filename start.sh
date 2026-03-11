#!/bin/bash
set -e

echo "Starting Lightweight Script AI API..."

# Memory optimization
export PYTHONUNBUFFERED=1
export TRANSFORMERS_CACHE=/tmp/transformers_cache
export HF_HOME=/tmp/huggingface

# Start server
exec uvicorn main:app --host 0.0.0.0 --port ${PORT:-8000} --workers 1
