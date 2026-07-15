# Text-AI: Lightweight Streaming LLM API

A production-ready FastAPI application that serves a Qwen-2.5-0.5B-Instruct model (GGUF) with streaming responses, optimized for low-memory environments (under 400MB RAM).

## Features
- **Streaming Responses:** Token-by-token generation for a responsive UI.
- **Memory Optimized:** Specifically tuned for Render's free tier (400MB RAM).
- **Auto-Download:** Optional model download via Google Drive at startup.
- **Fail-Fast Startup:** Validates environment and model presence before serving requests.

## Prerequisites
- Python 3.8+
- C++ Compiler (for `llama-cpp-python` compilation)

## Setup

### 1. Clone and Install
```bash
git clone <repo-url>
cd text-ai
pip install -r requirements.txt
```

### 2. Configure Environment
Set `DOWNLOAD_MODEL=1` if you want the app to automatically download the model from Google Drive on startup.
```bash
# Windows
set DOWNLOAD_MODEL=1
# Linux/Mac
export DOWNLOAD_MODEL=1
```

### 3. Run Locally
```bash
uvicorn main:app --reload
```
Visit `http://127.0.0.1:8000/chat` to start chatting.

## Production Deployment (Render)

1. **Environment Variables:**
   - `DOWNLOAD_MODEL`: `1`
   - `PYTHON_VERSION`: `3.10.0` (or higher)
2. **Build Command:**
   - `pip install -r requirements.txt`
3. **Start Command:**
   - `./start.sh`

### Render Environment Setup (Required)

To make the server work on Render, set these environment variables:

- **`DOWNLOAD_MODEL`**: `1`
  - Enables GGUF download at startup (via `model.py` `ensure_model_downloaded()`).
  - If set to `0` or missing, the app will fail with “Model file not found …”.

- **`PORT`**: (Render usually sets this automatically)
  - Used by `start.sh` to run Uvicorn: `uvicorn main:app --port $PORT`
  - You do not need to hardcode it, but it must exist.

- **`PYTHON_VERSION`**: `3.10.0` or higher
  - Required for compatibility with the app/runtime expectations.

Commands to configure in Render:

- **Build Command**:
  - `pip install -r requirements.txt`

- **Start Command**:
  - `./start.sh`

## API Reference

### GET `/`
Health check endpoint. Returns JSON status.

### POST `/generate`
Streams LLM tokens based on the provided prompt.
**Body:**
```json
{
  "text": "Hello, how are you?",
  "max_length": 128
}
```

### GET `/chat`
Serves the built-in web chat interface.
