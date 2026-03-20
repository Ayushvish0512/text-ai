# TinyLlama Optimization Guide
### Keep RAM under 400 MB · Prevent memory spikes · Reduce hallucinations

---

## 1. Memory Optimization (model.py)

The single most impactful place for RAM control is the `Llama()` constructor.

```python
llm = Llama(
    model_path=MODEL_PATH,
    n_ctx=512,          # context window — biggest RAM lever, do NOT increase
    n_threads=2,        # matches Render free tier CPU count (2 vCPUs)
    n_batch=8,          # small batch = less peak memory during inference
    use_mlock=False,    # do NOT lock model into RAM, let OS manage it
    use_mmap=True,      # memory-map the file instead of loading it fully
    verbose=False,      # no logging overhead
    f16_kv=True,        # store KV cache in float16 instead of float32 — halves KV RAM
)
```

### Why each setting matters

| Setting | Value | RAM impact |
|---|---|---|
| `n_ctx` | 512 | Largest single factor. Each 512 tokens of context uses ~50 MB extra. Never go above 512 on free tier. |
| `n_batch` | 8 | Controls how many tokens are processed per forward pass. Lower = less spike RAM. |
| `use_mmap` | True | Model weights are read from disk on demand instead of loaded into RAM all at once. Saves ~80–100 MB at startup. |
| `f16_kv` | True | KV cache stored as float16 not float32. Cuts KV RAM nearly in half. |
| `use_mlock` | False | Prevents the OS from being forced to keep all model pages in RAM at all times. |

---

## 2. Prevent Memory Spikes (main.py)

Concurrent requests are the #1 cause of RAM spikes. Each simultaneous inference adds ~50–80 MB on top of the base model RAM.

```python
from fastapi import FastAPI, Query
from fastapi.middleware.gzip import GZipMiddleware
import asyncio

app = FastAPI()
app.add_middleware(GZipMiddleware, minimum_size=500)

# Semaphore limits concurrent inferences to 1 at a time
# PRD allows up to 5 concurrent requests — but inference itself
# must be serialized to prevent RAM stacking on free tier
_inference_lock = asyncio.Semaphore(1)

llm = initialize_model()

@app.get("/chat")
async def chat(message: str = Query(...)):
    async with _inference_lock:
        reply = generate_response(llm, message)
    return {"user": message, "assistant": reply}
```

### Why a semaphore

Without it, 3 simultaneous `/chat` requests each load a KV cache. At 512 context that is roughly 3 × 50 MB = 150 MB spike on top of the 380 MB base, pushing you over 500 MB and crashing the free tier container. The semaphore queues requests so only one runs inference at a time. The others wait — they do not consume extra RAM while waiting.

---

## 3. Reduce Hallucinations (generate.py)

TinyLlama Q2_K is an aggressively compressed 1.1B model. Hallucination comes from high randomness in sampling. These settings constrain it:

```python
output = llm(
    prompt,
    max_tokens=200,
    temperature=0.1,    # very low — model picks most probable tokens only
    top_p=0.9,          # nucleus sampling — ignores the bottom 10% probability mass
    top_k=20,           # only sample from top 20 candidate tokens per step
    repeat_penalty=1.3, # strongly penalizes repeating the same phrase
    stop=["</s>", "<|user|>", "<|system|>", "<|im_end|>"],
    echo=False
)
```

### What each setting does to hallucination

| Setting | Value | Effect |
|---|---|---|
| `temperature` | 0.1 | Closest to greedy decoding. Model almost always picks the single most likely next token. Kills creative/random output. |
| `top_k` | 20 | At each step, only the 20 most probable tokens are considered. Foreign words, random names, off-topic tokens are ranked low and never selected. |
| `top_p` | 0.9 | Even within the top 20, cuts off the lowest probability tail. Double-filters garbage tokens. |
| `repeat_penalty` | 1.3 | Reduces the probability of any token the model has already generated. Prevents looping and padding. |
| `max_tokens` | 200 | Hard cap. Longer outputs = more chances for the model to drift off-topic. 200 is enough for factual answers. |

---

## 4. Prompt Engineering for TinyLlama Q2

The system prompt must be a list of hard prohibitions, not a polite description. This model is too small to infer what you want from tone alone.

```python
def build_prompt(user_input: str) -> str:
    return (
        "<|system|>\n"
        "You are a helpful assistant. "
        "Answer ONLY the user's question. "
        "Do NOT make up names, stories, or unrelated facts. "
        "Do NOT switch languages. "
        "Do NOT add greetings, signatures, or extra commentary. "
        "Be direct and factual.</s>\n"
        f"<|user|>\n{user_input}</s>\n"
        "<|assistant|>\n"
    )
```

**Key rules:**
- Always use `<|system|>` / `<|user|>` / `<|assistant|>` tags — TinyLlama was fine-tuned on the Zephyr format and ignores plain text system prompts.
- End every section with `</s>` — this is the separator token TinyLlama was trained on.
- Keep the system prompt under 50 tokens — every token in the prompt eats into your 512 `n_ctx` budget.
- Never ask multiple questions in one message. Split them client-side. The model sees a multi-question message as ambiguous and picks a random one to answer.

---

## 5. RAM Budget Breakdown

| Component | RAM usage |
|---|---|
| TinyLlama Q2_K model weights (mmap) | ~310 MB |
| KV cache at n_ctx=512, f16_kv=True | ~25 MB |
| FastAPI + uvicorn process | ~30 MB |
| One active inference (n_batch=8) | ~20 MB |
| **Total (single request)** | **~385 MB** |
| Safety headroom | ~15 MB |
| **Render free tier limit** | **512 MB** |

With `use_mmap=True` and `f16_kv=True` you stay comfortably under 400 MB for a single request. The semaphore ensures you never stack two inferences simultaneously.

---

## 6. Quick Checklist Before Deploy

- [ ] `n_ctx` is 512 or lower
- [ ] `use_mmap=True` in Llama constructor
- [ ] `f16_kv=True` in Llama constructor
- [ ] `n_batch` is 8 or lower
- [ ] Semaphore is set to 1 in main.py
- [ ] `temperature` is 0.1 or lower
- [ ] `top_k` is 20 or lower
- [ ] System prompt uses `<|system|>` tags and ends with `</s>`
- [ ] `max_tokens` is 200 or lower
- [ ] `verbose=False` in Llama constructor
