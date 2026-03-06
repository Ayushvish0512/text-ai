# Render Deployment Fix

## Issue
Build succeeded but deployment failed with:
```
ModuleNotFoundError: No module named 'backend'
```

## Root Cause
Render was trying to run `uvicorn backend.main:app` instead of `uvicorn app:app`.

## Solution Applied

### Fixed render.yaml
Changed startCommand from:
```yaml
startCommand: bash start.sh
```

To:
```yaml
startCommand: uvicorn app:app --host 0.0.0.0 --port $PORT --workers 1 --limit-concurrency 2 --timeout-keep-alive 5 --log-level info --no-access-log
```

This explicitly tells Render to:
- Use `app:app` (the `app` variable in `app.py`)
- Not look for a `backend` module

## To Redeploy

### Option 1: Push the fix
```bash
git add render.yaml
git commit -m "Fix: Use app:app instead of backend.main:app"
git push origin main
```

Render will automatically rebuild and redeploy.

### Option 2: Manual redeploy
1. Go to Render Dashboard
2. Click on your service
3. Click "Manual Deploy" → "Clear build cache & deploy"

## Verification

Once deployed, test:
```bash
# Health check
curl https://your-app.onrender.com/

# Should return:
# {"status":"ok","model":"distilgpt2-82M-q4","memory_optimized":true}
```

## Why This Happened

Render has a default behavior where if it doesn't find explicit instructions, it tries common patterns like:
- `backend.main:app`
- `main:app`
- `app:app`

By explicitly setting `startCommand` in render.yaml, we override this behavior.

## Alternative: Use start.sh

If you prefer using start.sh, you can also fix it by ensuring Render uses it:

```yaml
startCommand: bash start.sh
```

And make sure start.sh has:
```bash
exec uvicorn app:app --host 0.0.0.0 --port $PORT ...
```

Both approaches work. The direct uvicorn command is simpler and more explicit.
