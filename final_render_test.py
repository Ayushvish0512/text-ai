#!/usr/bin/env python3
"""
Final test for Render deployment.
"""
import sys
import time
import psutil
import os
import gc

print("=" * 60)
print("FINAL RENDER COMPATIBILITY TEST")
print("=" * 60)
print()

# Set cache to /tmp like Render
os.environ['TRANSFORMERS_CACHE'] = '/tmp/transformers_cache'
os.environ['HF_HOME'] = '/tmp/huggingface'

process = psutil.Process(os.getpid())

print("1. Testing server startup memory...")
# Simulate what happens when Render starts the server
# Only imports, no model loaded
import fastapi
import uvicorn

startup_memory = process.memory_info().rss / 1024 / 1024
print(f"   Memory after FastAPI imports: {startup_memory:.1f} MB")
print()

print("2. Testing first API request...")
print("   (Simulating /generate endpoint call)")

# Time the first request
start = time.time()

# Import our modules (this happens when endpoint is called)
from model_loader import load_model
from script_engine import generate_script

# Load model
tokenizer, model = load_model()
load_time = time.time() - start

memory_after_load = process.memory_info().rss / 1024 / 1024
print(f"   Model load time: {load_time:.1f}s")
print(f"   Memory after model load: {memory_after_load:.1f} MB")
print()

print("3. Testing script generation...")
test_article = "Breaking news: Scientists discover new renewable energy source that could revolutionize power generation worldwide."

start = time.time()
script = generate_script(test_article, max_length=150)
gen_time = time.time() - start

memory_after_gen = process.memory_info().rss / 1024 / 1024
print(f"   Generation time: {gen_time:.1f}s")
print(f"   Memory after generation: {memory_after_gen:.1f} MB")
print(f"   Script length: {len(script)} characters")
if script:
    print(f"   Script preview: {script[:100]}...")
print()

print("4. Testing memory limits...")
# Check against Render limits
render_limit = 500
safety_target = 450

peak_memory = max(startup_memory, memory_after_load, memory_after_gen)

print(f"   Startup memory: {startup_memory:.1f} MB")
print(f"   Model loaded: {memory_after_load:.1f} MB")
print(f"   Generation peak: {memory_after_gen:.1f} MB")
print(f"   Render limit: {render_limit} MB")
print(f"   Safety target: {safety_target} MB")
print()

# Force aggressive cleanup
print("5. Testing cleanup...")
from model_loader import unload_model
unload_model()

# Force garbage collection multiple times
for i in range(3):
    gc.collect()
    time.sleep(0.1)

final_memory = process.memory_info().rss / 1024 / 1024
print(f"   Memory after cleanup: {final_memory:.1f} MB")
print(f"   Memory reduction: {memory_after_gen - final_memory:.1f} MB")
print()

print("6. Render compatibility assessment...")
print()

if peak_memory < safety_target:
    print("   ✅ EXCELLENT - Well within safety limits")
    print(f"   Peak: {peak_memory:.1f} MB < Target: {safety_target} MB")
    print(f"   Safety margin: {safety_target - peak_memory:.1f} MB")
elif peak_memory < render_limit:
    print("   ⚠ ACCEPTABLE - Within Render limit but close")
    print(f"   Peak: {peak_memory:.1f} MB < Limit: {render_limit} MB")
    print(f"   Margin: {render_limit - peak_memory:.1f} MB")
    print("   Note: May work but monitor closely")
else:
    print("   ❌ PROBLEMATIC - Above Render limit")
    print(f"   Peak: {peak_memory:.1f} MB > Limit: {render_limit} MB")
    print(f"   Over by: {peak_memory - render_limit:.1f} MB")
    print("   May crash on Render free tier")

print()
print("=" * 60)
print("TEST COMPLETE")
print("=" * 60)
print()
print("Key optimizations in place:")
print("1. CPU-only torch (no CUDA)")
print("2. Float16 model weights (half precision)")
print("3. Lazy loading (model loads on first request only)")
print("4. Model unloading with garbage collection")
print("5. Input/output size limits")
print("6. Single worker configuration")
print()
print("Note: Actual Render memory may be 10-20% lower than")
print("local Windows test due to Linux container differences.")