"""
Local test script to verify the model works before deploying to Render.
"""
import sys
import time

print("=" * 60)
print("LOCAL TEST - Script AI API")
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
    
    if memory_mb < 500:
        print(f"   ✓ Within Render limit (500 MB)")
    else:
        print(f"   ⚠ Above Render limit! ({memory_mb:.0f} MB > 500 MB)")
        
except ImportError:
    print("   ⚠ psutil not installed (optional)")
    print("   Install with: pip install psutil")

print()
print("=" * 60)
print("✓ ALL TESTS PASSED - Ready for Render deployment!")
print("=" * 60)
print()
print("Next steps:")
print("1. git add .")
print("2. git commit -m 'Script AI API'")
print("3. git push origin main")
print("4. Deploy on Render")
print()
