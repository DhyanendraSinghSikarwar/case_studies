# SYNTHETIC request stream and ASSUMED compile/serve times (not measurements of any engine).
import json, hashlib, random
from collections import OrderedDict

def schema_hash(schema):
    return hashlib.sha256(json.dumps(schema, sort_keys=True, separators=(",", ":")).encode()).hexdigest()

class LRU:
    def __init__(self, cap): self.cap, self.d, self.hits, self.miss = cap, OrderedDict(), 0, 0
    def get_or_compile(self, schema, compile_fn):
        k = schema_hash(schema)
        if k in self.d: self.d.move_to_end(k); self.hits += 1; return self.d[k], True
        self.miss += 1; self.d[k] = compile_fn(schema)
        if len(self.d) > self.cap: self.d.popitem(last=False)
        return self.d[k], False

def make_schema(i, shuffle_rng=None):
    props = {f"f{j}": {"type": "string"} for j in range(3)} | {"kind": {"enum": [f"k{i}", "other"]}}
    items = list(props.items())
    if shuffle_rng: shuffle_rng.shuffle(items)            # same schema, different key order
    return {"type": "object", "properties": dict(items), "required": ["kind"]}

rng = random.Random(0)
N, TEMPLATES = 5000, 20
weights = [1 / (i + 1) for i in range(TEMPLATES)]          # a few templates dominate (Zipf-like)
stream = []
for n in range(N):
    if rng.random() < 0.05: stream.append(make_schema(10_000 + n))     # 5% truly unique schemas
    else: stream.append(make_schema(rng.choices(range(TEMPLATES), weights)[0], rng))

COMPILE_MS, SERVE_MS = 800.0, 40.0                           # ASSUMED, for illustration only
def pct(xs, p): xs = sorted(xs); return xs[min(len(xs) - 1, int(p / 100 * len(xs)))]

for cap in (0, 5, 20, 100):
    cache, lat = LRU(cap), []
    for s in stream:
        if cap == 0: cache.miss += 1; lat.append(COMPILE_MS + SERVE_MS); continue
        _, hit = cache.get_or_compile(s, lambda s: object())
        lat.append(SERVE_MS if hit else COMPILE_MS + SERVE_MS)
    tot = cache.hits + cache.miss
    print(f"cap {cap:3d}: hit rate {cache.hits/tot:6.1%}  p50 {pct(lat,50):6.1f} ms  p99 {pct(lat,99):6.1f} ms")
print("distinct canonical schemas in stream:", len({schema_hash(s) for s in stream}))
