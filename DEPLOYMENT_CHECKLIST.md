# Render Deployment Checklist

## ✅ Pre-Deployment Checks

### 1. Dependencies
- [x] CPU-only torch installed (`torch==2.1.0 --index-url https://download.pytorch.org/whl/cpu`)
- [x] Only 5 packages in requirements.txt
- [x] No heavy ML libraries (TensorFlow, PyTorch with CUDA, etc.)

### 2. Memory Optimizations
- [x] Lazy model loading implemented
- [x] 5-minute idle timeout for model unloading
- [x] Memory monitoring endpoints (`/memory`, `/health`)
- [x] Input limits: 2000 characters max
- [x] Output limits: 300 tokens max
- [x] Target memory: < 450MB (500MB Render limit)

### 3. Render Configuration
- [x] Free tier plan specified
- [x] Single worker only (`--workers 1`)
- [x] Temp cache for model storage (`/tmp/transformers_cache`)
- [x] Health check endpoint configured
- [x] Environment variables for memory optimization

### 4. Code Optimizations
- [x] Automatic garbage collection
- [x] Tensor cleanup after generation
- [x] Model unloading on idle
- [x] Error handling with memory cleanup

## 🚀 Deployment Steps

1. **Commit changes**
   ```bash
   git add .
   git commit -m "Render-optimized Script AI API"
   git push origin main
   ```

2. **Deploy to Render**
   - Go to [render.com](https://render.com)
   - Create new Web Service
   - Connect your GitHub repository
   - Render will automatically detect `render.yaml`
   - Wait for build (~5 minutes)

3. **Monitor deployment**
   - Check build logs for any issues
   - Wait for "Live" status
   - Test endpoints:
     - `GET /` - Service info
     - `GET /health` - Health check
     - `GET /memory` - Memory usage
     - `POST /generate` - Script generation

## 📊 Expected Performance

- **Cold start**: 30-60 seconds (model downloads on first request)
- **Response time**: 5-15 seconds
- **Memory usage**: 300-400MB
- **Model**: DistilGPT2 (82M params, CPU-only)
- **Safety margin**: 100-200MB under Render limit

## 🔧 Troubleshooting

### High Memory Usage
1. Check `/memory` endpoint
2. Model might be loaded - wait 5 minutes for idle timeout
3. Force garbage collection via restart

### Slow Response
1. First request loads model (30-60s)
2. Subsequent requests faster (5-15s)
3. Check Render logs for timeouts

### Model Not Loading
1. Check `/tmp` has write permissions
2. Verify internet connectivity in Render
3. Check Hugging Face token if using private models

## 📈 Monitoring

### Key Metrics to Watch
1. **Memory usage** (should stay < 450MB)
2. **Response time** (should be < 30s)
3. **Error rate** (should be < 1%)
4. **Uptime** (Render free tier has limits)

### Alert Thresholds
- Memory > 450MB: Warning
- Memory > 480MB: Critical
- Response time > 30s: Warning
- Health check fails: Critical

## 🔄 Maintenance

### Regular Checks
1. Weekly: Test all endpoints
2. Monthly: Update dependencies
3. Quarterly: Review memory usage patterns

### Scaling Considerations
If you need more capacity:
1. Upgrade to Render Pro tier ($7/month)
2. Add more memory/CPU
3. Consider model optimization (quantization)

## 📞 Support

- Render Docs: https://render.com/docs
- Hugging Face: https://huggingface.co/docs
- FastAPI: https://fastapi.tiangolo.com

---

**Last verified**: All optimizations applied and verified
**Ready for deployment**: ✅ Yes