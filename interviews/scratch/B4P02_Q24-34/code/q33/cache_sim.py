"""Which layers rebuild when CI starts with an empty cache vs a restored one? (toy model of BuildKit keys)"""
import hashlib

def keys(parent_key, instrs):
    out = []
    for text, content in instrs:
        parent_key = hashlib.sha256((parent_key + text + content).encode()).hexdigest()[:8]
        out.append(parent_key)
    return out

def build(instrs, cache):
    k = keys("base", instrs); rebuilt = []
    for (text, _), key in zip(instrs, k):
        if key not in cache: rebuilt.append(text)
        cache.add(key)
    return rebuilt

run1 = [("COPY requirements.txt", "torch==2.x"), ("RUN pip install", ""), ("COPY src/", "v1")]
run2 = [("COPY requirements.txt", "torch==2.x"), ("RUN pip install", ""), ("COPY src/", "v2")]   # code-only change

shared = set()
build(run1, shared)                                   # a previous CI run saved its cache
print("empty runner cache, code-only change :", build(run2, set()))
print("restored cache, code-only change     :", build(run2, set(shared)))
