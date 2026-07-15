# TODO — Run project in venv

## Steps
1. Create a Python virtual environment (.venv). ✅
2. Activate the venv (Windows instructions). ✅ (activation not required for our direct `.venv\Scripts\python.exe` commands)
3. Install dependencies: `pip install -r requirements.txt` ✅ (after removing `llama-cpp-python`)
   - Updated `requirements.txt` to remove `llama-cpp-python` because the server uses `subprocess` to run `llama.cpp/main`.
4. Verify the llama binary path used by `main.py` exists: `llama.cpp/main` ⏳
5. Start the FastAPI server:
   - `uvicorn main:app --reload` ✅ (server started)
6. Test:
   - Open `http://127.0.0.1:8000/` ⏳
   - Open `http://127.0.0.1:8000/chat` ⏳

## Current status (Windows)
- Venv created with `py -m venv .venv`.
- `pip install -r requirements.txt` initially failed due to building `llama-cpp-python`.
- Workaround applied: removed `llama-cpp-python` from `requirements.txt` and installed remaining deps successfully.
- Uvicorn running via: `.venv\Scripts\python.exe -m uvicorn main:app --host 127.0.0.1 --port 8000 --reload`

## Notes
- `start.sh` is bash-only; on Windows we’ll run uvicorn directly.
- Current `main.py` shells out to `llama.cpp/main`.
- If `llama.cpp/main` is missing/not built, `/generate` will fail (but the API startup will still succeed).
