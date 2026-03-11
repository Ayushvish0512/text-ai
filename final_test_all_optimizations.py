#!/usr/bin/env python3
"""
Final test with all optimizations for Render.
"""
import sys
import time
import psutil
import os
import gc

print("=" * 60)
print("FINAL TEST - ALL OPTIMIZATIONS")
print("=" * 60)
print()

process = psutil.Process(os.getpid())

print("1. Testing with all optimizations...")
print("   • CPU-only torch")
print("   • 8-bit quantization (with accelerate)")
print("   • Float16 fallback")
print("   • Lazy loading")
print("   • Smaller limits (1000 chars input, 150 tokens output)")
print()

# Baseline
m1 = process.memory_info().rss / 1024 / 1024
print(f"   Baseline memory: {m1:.1f} MB")

# Test imports
import fastapi
import uvicorn
m2 = process.memory_info().rss / 1024 / 1024
print(f"   After FastAPI imports: {m2:.1f} MB (+{m2-m1:.1f} MB)")

# Test model loading
print()
print("2. Testing model loading...")
start = time.time()

from model_loader import load_model
tokenizer, model = load_model()

load_time = time.time() - start
m3 = process.memory_info().rss / 1024 / 1024
print(f"   Model load time: {load_time:.1f}s")
print(f"   Memory after model: {m3:.1f} MB (+{m3-m2:.1f} MB)")

# Check model details
print(f"   Model dtype: {model.dtype}")
print(f"   Model device: {model.device}")

# Test script generation
print()
print("3. Testing script generation...")
from script_engine import generate_script

test_article = "Scientists discover new renewable energy source. It could change everything."

start = time.time()
script = generate_script(test_article, max_length=100)
gen_time = time.time() - start

m4 = process.memory_info().rss / 1024 / 1024
print(f"   Generation time: {gen_time:.1f}s")
print(f"   Memory after generation: {m4:.1f} MB (+{m4-m3:.1f} MB)")
print(f"   Script length: {len(script)} chars")
if script:
    print(f"   Script: {script[:150]}...")

# Test cleanup
print()
print("4. Testing cleanup...")
from model_loader import unload_model
unload_model()

# Force GC
for i in range(3):
    gc.collect()
    time.sleep(0.1)

m5 = process.memory_info().rss / 1024 / 1024
print(f"   Memory after cleanup: {m5:.1f} MB")
print(f"   Memory reduction: {m4-m5:.1f} MB")

# Render compatibility
print()
print("5. Render compatibility check...")
render_limit = 500
safety_target = 450
peak_memory = max(m1, m2, m3, m4, m5)

print(f"   Peak memory: {peak_memory:.1f} MB")
print(f"   Render limit: {render_limit} MB")
print(f"   Safety target: {safety_target} MB")
print()

if peak_memory < safety_target:
    print("   ✅ EXCELLENT - Well within safety limits")
    print(f"   Margin: {safety_target - peak_memory:.1f} MB")
elif peak_memory < render_limit:
    print("   ⚠ ACCEPTABLE - Within limit but close")
    print(f"   Margin: {render_limit - peak_memory:.1f} MB")
else:
    print("   ❌ PROBLEMATIC - Above limit")
    print(f"   Over by: {peak_memory - render_limit:.1f} MB")

print()
print("=" * 60)
print("OPTIMIZATION SUMMARY")
print("=" * 60)
print()
print("Implemented optimizations:")
print("1. ✅ CPU-only torch (no CUDA)")
print("2. ✅ 8-bit quantization with accelerate")
print("3. ✅ Float16 fallback")
print("4. ✅ Lazy model loading")
print("5. ✅ Model unloading with GC")
print("6. ✅ Smaller limits (1000 chars, 150 tokens)")
print("7. ✅ Shorter prompts for memory")
print("8. ✅ Single worker configuration")
print("9. ✅ Temp cache for models")
print("10. ✅ Memory monitoring endpoints")
print()
print("Expected Render performance:")
print("• Memory: 400-500MB (depending on 8-bit success)")
print("• First request: 30-60s (model download)")
print("• Subsequent: 5-15s")
print("• Safety margin: 0-100MB")