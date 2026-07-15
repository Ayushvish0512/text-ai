#!/bin/bash
set -e

# Render and other platforms use the PORT environment variable
PORT="${PORT:-8000}"

# Start uvicorn. 
# --workers 1 is CRITICAL to stay under 400MB RAM.
exec uvicorn main:app --host 0.0.0.0 --port "$PORT" --workers 1
