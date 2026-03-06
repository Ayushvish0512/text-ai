# Production Deployment Checklist

Use this checklist before deploying to Render.

## Pre-Deployment

### Code Review
- [ ] All files committed to Git
- [ ] `.gitignore` excludes models/ and llama.cpp/
- [ ] No sensitive data in code (API keys, passwords)
- [ ] `requirements.txt` has pinned versions
- [ ] `runtime.txt` specifies Python 3.11.0

### Configuration Review
- [ ] `render.yaml` configured correctly
- [ ] `start.sh` has execute permissions (`chmod +x start.sh`)
- [ ] Model URL in `render.yaml` is accessible
- [ ] `MODEL_PATH` in `app.py` matches download location
- [ ] `LLAMA_BIN` path in `app.py` is correct

### Memory Optimization
- [ ] Only 2 dependencies (fastapi, uvicorn)
- [ ] No numpy, torch, or heavy libraries
- [ ] `--ctx-size` set to 128 (not higher)
- [ ] `--workers` set to 1
- [ ] `--limit-concurrency` set to 2
- [ ] `--threads` set to 1 in llama.cpp call

### Error Handling
- [ ] Health check endpoint works
- [ ] Input validation on `/generate`
- [ ] Timeout protection (30s)
- [ ] Proper error responses (400, 500, 504)
- [ ] Logging configured

## Deployment

### GitHub
- [ ] Repository is public or Render has access
- [ ] Latest code pushed to main branch
- [ ] No large files committed (models, binaries)

### Render Setup
- [ ] Render account created
- [ ] GitHub connected to Render
- [ ] Repository selected
- [ ] `render.yaml` detected automatically
- [ ] Plan set to "Free"
- [ ] Region selected (Oregon recommended)

### Build Process
- [ ] Build started successfully
- [ ] Python dependencies installed
- [ ] Model downloaded (35MB)
- [ ] llama.cpp cloned
- [ ] llama-cli compiled
- [ ] No build errors

### Deployment Verification
- [ ] Service shows "Live" status
- [ ] Health endpoint responds: `curl https://your-app.onrender.com/`
- [ ] Generate endpoint works (may be slow)
- [ ] No error logs in Render dashboard
- [ ] Memory usage under 300MB

## Post-Deployment

### Monitoring
- [ ] Check Render Metrics tab
- [ ] Memory usage: ~150-200MB (safe)
- [ ] CPU usage: Low (expected)
- [ ] No crash loops in logs

### Testing
- [ ] Health check returns 200 OK
- [ ] Generate with short prompt works
- [ ] Generate with longer prompt works
- [ ] Error handling works (empty text returns 400)
- [ ] Response time acceptable (slow on 0.1 CPU is normal)

### Documentation
- [ ] README.md updated with deployment URL
- [ ] API documentation clear
- [ ] Troubleshooting guide available

## Performance Expectations

### Memory
✅ **Expected**: 150-200MB  
⚠️ **Warning**: 250-350MB (still safe)  
❌ **Critical**: >380MB (will crash)

### Response Time
✅ **Expected**: 5-30 seconds per request  
⚠️ **Slow**: 30-60 seconds (reduce max_length)  
❌ **Timeout**: >60 seconds (prompt too long)

### Availability
✅ **Free tier sleeps after 15 min inactivity**  
✅ **First request after sleep: ~30s wake time**  
✅ **750 hours/month runtime (enough for 24/7)**

## Troubleshooting

### Build Fails
- [ ] Check build logs for specific error
- [ ] Verify model URL is accessible
- [ ] Ensure llama.cpp compiles (check for make errors)
- [ ] Try manual deploy from Render dashboard

### Memory Issues
- [ ] Switch to smaller model (TinyStories 15M)
- [ ] Reduce `--ctx-size` to 64
- [ ] Lower `--limit-concurrency` to 1
- [ ] Check for memory leaks in logs

### Timeout Issues
- [ ] Reduce `max_length` in requests
- [ ] Use shorter prompts
- [ ] Check if service is sleeping (first request slow)
- [ ] Verify llama.cpp is running

### Service Crashes
- [ ] Check logs for OOM (Out of Memory) errors
- [ ] Verify model file exists
- [ ] Check llama-cli binary exists
- [ ] Review error logs in Render dashboard

## Optimization Tips

### For Better Performance
- Upgrade to paid tier (0.5 CPU minimum)
- Use smaller model (TinyStories 15M)
- Implement response caching
- Add request queuing

### For Lower Memory
- Use Q2 quantization instead of Q4
- Reduce context size to 64
- Limit max_length to 30
- Single concurrent request only

### For Production Use
- Add rate limiting
- Implement API authentication
- Add request logging
- Set up monitoring alerts
- Use CDN for static assets

## Success Criteria

✅ **Deployment Successful**
- Service is "Live" on Render
- Health endpoint returns 200
- Generate endpoint produces text
- Memory under 300MB
- No crash loops

✅ **Production Ready**
- Error handling works
- Logging configured
- Documentation complete
- Monitoring in place
- Performance acceptable

## Next Steps

After successful deployment:

1. **Monitor for 24 hours**
   - Check memory usage stays stable
   - Verify no crashes
   - Test during different times

2. **Document API URL**
   - Update README with live URL
   - Share with team/users
   - Add to API documentation

3. **Set up alerts** (optional)
   - Render webhook for downtime
   - Memory usage alerts
   - Error rate monitoring

4. **Plan for scale** (if needed)
   - Consider paid tier for better performance
   - Implement caching layer
   - Add load balancing

---

**Last Updated**: Check this list before each deployment  
**Status**: Ready for production ✅
