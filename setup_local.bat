@echo off
setlocal enabledelayedexpansion

echo ==========================================
echo Tiny LLM API - Local Setup (Windows)
echo ==========================================
echo.

REM Check Python
echo Checking prerequisites...
python --version >nul 2>&1
if errorlevel 1 (
    echo X Python not found. Please install Python 3.11+
    exit /b 1
)
echo [OK] Python found
python --version

REM Check Git
git --version >nul 2>&1
if errorlevel 1 (
    echo X Git not found. Please install Git
    exit /b 1
)
echo [OK] Git found

REM Check curl
curl --version >nul 2>&1
if errorlevel 1 (
    echo X curl not found. Please install curl
    exit /b 1
)
echo [OK] curl found

REM Install Python dependencies
echo.
echo Installing Python dependencies...
pip install --no-cache-dir -r requirements.txt
if errorlevel 1 (
    echo X Failed to install dependencies
    exit /b 1
)
echo [OK] Dependencies installed

REM Download model
echo.
echo Downloading model (35MB)...
if not exist models mkdir models

if exist models\distilgpt2-q4_k_m.gguf (
    echo [SKIP] Model already exists
) else (
    curl -L -o models\distilgpt2-q4_k_m.gguf https://huggingface.co/Crataco/distilgpt2-82M-GGUF/resolve/main/distilgpt2-q4_k_m.gguf
    if errorlevel 1 (
        echo X Failed to download model
        exit /b 1
    )
    echo [OK] Model downloaded
)

REM Clone llama.cpp
echo.
echo Setting up llama.cpp...

if exist llama.cpp (
    echo [SKIP] llama.cpp directory exists
) else (
    git clone --depth 1 https://github.com/ggerganov/llama.cpp.git
    if errorlevel 1 (
        echo X Failed to clone llama.cpp
        exit /b 1
    )
    echo [OK] llama.cpp cloned
)

REM Build instructions for Windows
echo.
echo ==========================================
echo IMPORTANT: Building llama.cpp on Windows
echo ==========================================
echo.
echo Windows requires Visual Studio or MinGW to build llama.cpp.
echo.
echo Option 1: Visual Studio (Recommended)
echo   1. Install Visual Studio 2022 Community
echo   2. Open "Developer Command Prompt for VS 2022"
echo   3. cd llama.cpp
echo   4. cmake -B build
echo   5. cmake --build build --config Release
echo   6. copy build\bin\Release\llama-cli.exe llama-cli.exe
echo.
echo Option 2: Pre-built Binary
echo   Download from: https://github.com/ggerganov/llama.cpp/releases
echo   Extract llama-cli.exe to llama.cpp\ folder
echo.
echo Option 3: Use WSL (Windows Subsystem for Linux)
echo   1. Install WSL: wsl --install
echo   2. Run setup_local.sh in WSL
echo.
echo After building, run:
echo   python app.py
echo.
echo ==========================================

pause
