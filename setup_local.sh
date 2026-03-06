#!/bin/bash
set -e

echo "=========================================="
echo "Tiny LLM API - Local Setup"
echo "=========================================="

# Check prerequisites
echo ""
echo "Checking prerequisites..."

if ! command -v python3 &> /dev/null; then
    echo "❌ Python 3 not found. Please install Python 3.11+"
    exit 1
fi
echo "✅ Python 3 found: $(python3 --version)"

if ! command -v git &> /dev/null; then
    echo "❌ Git not found. Please install Git"
    exit 1
fi
echo "✅ Git found"

if ! command -v make &> /dev/null; then
    echo "❌ Make not found. Please install build tools"
    exit 1
fi
echo "✅ Make found"

if ! command -v curl &> /dev/null; then
    echo "❌ curl not found. Please install curl"
    exit 1
fi
echo "✅ curl found"

# Install Python dependencies
echo ""
echo "Installing Python dependencies..."
pip install --no-cache-dir -r requirements.txt
echo "✅ Dependencies installed"

# Download model
echo ""
echo "Downloading model (35MB)..."
mkdir -p models

if [ -f "models/distilgpt2-q4_k_m.gguf" ]; then
    echo "⚠️  Model already exists, skipping download"
else
    curl -L -o models/distilgpt2-q4_k_m.gguf \
        https://huggingface.co/Crataco/distilgpt2-82M-GGUF/resolve/main/distilgpt2-q4_k_m.gguf
    echo "✅ Model downloaded"
fi

# Clone and build llama.cpp
echo ""
echo "Setting up llama.cpp..."

if [ -d "llama.cpp" ]; then
    echo "⚠️  llama.cpp directory exists, skipping clone"
else
    git clone --depth 1 https://github.com/ggerganov/llama.cpp.git
    echo "✅ llama.cpp cloned"
fi

echo ""
echo "Building llama.cpp (this may take 2-3 minutes)..."
cd llama.cpp
make clean || true
make llama-cli LLAMA_NO_ACCELERATE=1 LLAMA_NO_METAL=1 LLAMA_OPENBLAS=0
cd ..

if [ -f "llama.cpp/llama-cli" ]; then
    echo "✅ llama-cli built successfully"
else
    echo "❌ Build failed - llama-cli not found"
    exit 1
fi

# Verify setup
echo ""
echo "=========================================="
echo "Setup Complete!"
echo "=========================================="
echo ""
echo "Files created:"
ls -lh models/distilgpt2-q4_k_m.gguf
ls -lh llama.cpp/llama-cli
echo ""
echo "To start the server:"
echo "  python app.py"
echo ""
echo "Or use:"
echo "  bash start.sh"
echo ""
echo "Then test with:"
echo "  python test_generate.py"
echo ""
echo "API will be available at: http://localhost:8000"
echo "=========================================="
