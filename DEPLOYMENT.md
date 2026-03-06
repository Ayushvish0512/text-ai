# Deployment Guide - Render Free Tier

Step-by-step guide to deploy Tiny LLM API on Render with 400MB RAM.

## Pre-Deployment Checklist

- [ ] Code pushed to GitHub repository
- [ ] All files committed (app.py, requirements.txt, render.yaml, start.sh, runtime.txt)
- [ ] GitHub repository is public or Render has access

## Deployment Steps

### 1. Create Render Account
- Go to https://render.com
- Sign up with GitHub account (recommended)
- Verify email

### 2. Create New Web Service

1. Click **"New +"** button (top right)
2. Select **"Web Service"**
3. Connect your GitHub repository
4. Select your repository from the list

### 3. Configure Service

Render will auto-detect `render.yaml`. Verify these settings:

- **Name**: `tiny-llm-api` (or your choice)
- **Environment**: `Python 3`
- **Region**: `Oregon` (or closest to you)
- **Branch**: `main` (or your default branch)
- **Plan**: `Free`

### 4. Environment Variables (Auto-configured)

These are set in `render.yaml`:
```
PYTHONUNBUFFERED=1
MALLOC_TRIM_THRESHOLD_=100000
PYTHONDONTWRITEBYTECODE=1
```

### 5. Deploy

1. Click **"Create Web Service"**
2. Build will start automatically
3. Monitor build logs

### 6. Build Process (5-10 minutes)

Watch for these steps in logs:
```
Installing Python dependencies...
Creating models directory...
Downloading distilgpt2 model (35MB)...
Cloning llama.cpp...
Building llama.cpp (minimal config)...
Build complete!
```

### 7. Verify Deployment

Once deployed, you'll get a URL like: `https://tiny-llm-api.onrender.com`

Test it:
```bash
# Health check
curl https://your-app.onrender.com/

# Generate text
curl -X POST https://your-app.onrender.com/generate \
  -H "Content-Type: application/json" \
  -d '{"text": "Hello world", "max_length": 20}'
```

## Expected Build Output

```
==> Installing Python dependencies...
Successfully installed fastapi-0.109.0 uvicorn-0.27.0

==> Creating models directory...

==> Downloading distilgpt2 model (35MB)...
  % Total    % Received
100 35.2M  100 35.2M    0     0  10.2M      0  0:00:03  0:00:03

==> Cloning llama.cpp...
Cloning into 'llama.cpp'...

==> Building llama.cpp (minimal config)...
g++ -O3 -std=c++11 -o llama-cli ...
Build complete!
-rwxr-xr-x 1 render render 2.1M llama-cli

==> Build successful!
```

## Post-Deployment

### Monitor Service

1. Go to Render Dashboard
2. Click on your service
3. Check **"Logs"** tab for runtime logs
4. Check **"Metrics"** tab for memory usage

### Expected Memory Usage

In Render Metrics, you should see:
- **Memory**: ~150-200MB (well under 400MB limit)
- **CPU**: Low usage (0.1 CPU is limited)

### First Request

⚠️ **Important**: First request after deployment may take 10-20 seconds as the model loads into memory. Subsequent requests will be faster.

## Troubleshooting

### Build Fails

**Error: "make: command not found"**
- Render should have make installed. Contact support if missing.

**Error: "curl: command not found"**
- Use `wget` instead in render.yaml

**Error: "Model download failed"**
- Check HuggingFace URL is accessible
- Try alternative mirror or smaller model

### Deployment Fails

**Error: "Port already in use"**
- Render sets `$PORT` automatically, ensure start.sh uses it

**Error: "Model file not found"**
- Check build logs to ensure model downloaded
- Verify path in app.py matches downloaded location

**Error: "llama-cli not found"**
- Check llama.cpp compiled successfully
- Verify binary path in app.py

### Runtime Issues

**Error: "Out of memory"**
- Switch to smaller model (TinyStories 15M)
- Reduce `--ctx-size` to 64 in app.py
- Lower `--limit-concurrency` to 1 in start.sh

**Error: "Request timeout"**
- Reduce `max_length` in API requests
- Increase timeout in app.py (carefully)
- Expected on 0.1 CPU - responses will be slow

**Service sleeps after inactivity**
- Free tier services sleep after 15 minutes of inactivity
- First request after sleep takes ~30 seconds to wake up
- Consider paid tier for always-on service

## Updating Deployment

### Push Updates

```bash
git add .
git commit -m "Update configuration"
git push origin main
```

Render will automatically rebuild and redeploy.

### Manual Redeploy

1. Go to Render Dashboard
2. Click on your service
3. Click **"Manual Deploy"** → **"Deploy latest commit"**

### Rollback

1. Go to Render Dashboard
2. Click on your service
3. Go to **"Events"** tab
4. Find previous successful deploy
5. Click **"Rollback to this version"**

## Cost Optimization

### Free Tier Limits

- **750 hours/month** of runtime (enough for 24/7)
- **400MB RAM** (we use ~155MB)
- **0.1 CPU** (shared, limited)
- **Sleeps after 15 min inactivity**

### Staying Within Limits

✅ **Good practices:**
- Use minimal dependencies
- Single worker process
- Limited concurrency
- Small context window
- Efficient model (Q4 quantization)

❌ **Avoid:**
- Multiple workers
- Large models (>100MB)
- High concurrency
- Large context windows (>256)
- Heavy Python ML libraries

## Monitoring

### Check Logs

```bash
# Via Render Dashboard
Dashboard → Your Service → Logs

# Look for:
INFO:     Started server process
INFO:     Waiting for application startup.
INFO:     Application startup complete.
INFO:     Uvicorn running on http://0.0.0.0:10000
```

### Check Memory

```bash
# Via Render Dashboard
Dashboard → Your Service → Metrics

# Should show:
Memory: ~150-200MB / 400MB (safe)
```

### Test Endpoint

```bash
# Health check (should be fast)
curl https://your-app.onrender.com/

# Generate (will be slow on 0.1 CPU)
time curl -X POST https://your-app.onrender.com/generate \
  -H "Content-Type: application/json" \
  -d '{"text": "Hello", "max_length": 20}'
```

## Support

- **Render Docs**: https://render.com/docs
- **Render Community**: https://community.render.com
- **llama.cpp Issues**: https://github.com/ggerganov/llama.cpp/issues

## Success Criteria

✅ Deployment successful if:
- Build completes without errors
- Service shows "Live" status
- Health endpoint returns `{"status": "ok"}`
- Generate endpoint returns text (even if slow)
- Memory usage stays under 300MB

🎉 **Congratulations! Your Tiny LLM API is live!**
