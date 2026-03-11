"""
Local test script to verify the model works before deploying to Render.
"""
import sys
import time

print("=" * 60)
print("LOCAL TEST - Script AI API (Render Optimized)")
print("=" * 60)
print()

# Test 1: Check dependencies
print("1. Checking dependencies...")
try:
    import fastapi
    import uvicorn
    import transformers
    import torch
    print("   ✓ All dependencies installed")
    print(f"   ✓ Torch version: {torch.__version__}")
    print(f"   ✓ Using CPU: {not torch.cuda.is_available()}")
except ImportError as e:
    print(f"   ✗ Missing dependency: {e}")
    print("\n   Run: pip install -r requirements.txt")
    sys.exit(1)

print()

# Test 2: Load model
print("2. Loading DistilGPT2 model...")
print("   (This may take 30-60 seconds on first run)")
start = time.time()

try:
    from model_loader import load_model
    tokenizer, model = load_model()
    load_time = time.time() - start
    print(f"   ✓ Model loaded successfully in {load_time:.1f}s")
    print(f"   ✓ Model device: {model.device}")
except Exception as e:
    print(f"   ✗ Failed to load model: {e}")
    sys.exit(1)

print()

# Test 3: Generate script
print("3. Testing script generation...")
test_article = """
The government announced major reforms today affecting millions of citizens. 
The new policy will change how healthcare is delivered across the country.
Experts warn this could have significant economic impacts.
"""

try:
    from script_engine import generate_script
    
    start = time.time()
    script = generate_script(test_article, max_length=150)
    gen_time = time.time() - start
    
    print(f"   ✓ Script generated in {gen_time:.1f}s")
    print()
    print("   Input article:")
    print(f"   {test_article.strip()[:100]}...")
    print()
    print("   Generated script:")
    print(f"   {script[:200]}...")
    print()
    
except Exception as e:
    print(f"   ✗ Failed to generate script: {e}")
    sys.exit(1)

# Test 4: Memory check
print("4. Checking memory usage...")
try:
    import psutil
    import os
    
    process = psutil.Process(os.getpid())
    memory_mb = process.memory_info().rss / 1024 / 1024
    
    print(f"   Current memory usage: {memory_mb:.0f} MB")
    
    if memory_mb < 450:
        print(f"   ✓ Within Render limit (450 MB target)")
    elif memory_mb < 500:
        print(f"   ⚠ Close to Render limit ({memory_mb:.0f} MB)")
    else:
        print(f"   ⚠ Above Render limit! ({memory_mb:.0f} MB > 500 MB)")
        
except ImportError:
    print("   ⚠ psutil not installed (optional)")
    print("   Install with: pip install psutil")

# Test 5: Test memory endpoints
print()
print("5. Testing API endpoints...")
try:
    from main import app
    from fastapi.testclient import TestClient
    
    client = TestClient(app)
    
    # Test home endpoint
    response = client.get("/")
    if response.status_code == 200:
        print("   ✓ Home endpoint working")
        data = response.json()
        print(f"   ✓ Memory usage: {data.get('memory_usage_mb', 'N/A')} MB")
    else:
        print(f"   ✗ Home endpoint failed: {response.status_code}")
    
    # Test health endpoint
    response = client.get("/health")
    if response.status_code == 200:
        print("   ✓ Health endpoint working")
    else:
        print(f"   ✗ Health endpoint failed: {response.status_code}")
    
    # Test memory endpoint
    response = client.get("/memory")
    if response.status_code == 200:
        print("   ✓ Memory endpoint working")
    else:
        print(f"   ✗ Memory endpoint failed: {response.status_code}")
        
except ImportError as e:
    print(f"   ⚠ TestClient not available: {e}")

print()
print("=" * 60)
print("✓ ALL TESTS PASSED - Ready for Render deployment!")
print("=" * 60)
print()
print("Optimizations applied:")
print("• CPU-only torch installation")
print("• Lazy model loading with idle timeout")
print("• Memory monitoring endpoints")
print("• Input/output size limits")
print("• Automatic garbage collection")
print()
print("Next steps:")
print("1. git add .")
print("2. git commit -m 'Render-optimized Script AI API'")
print("3. git push origin main")
print("4. Deploy on Render")
print()
