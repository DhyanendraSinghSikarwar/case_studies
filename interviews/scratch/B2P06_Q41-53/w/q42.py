# Standalone, numpy only. TOY store: hashed bag-of-words "embeddings" (no semantic quality), synthetic tenants.
import zlib, numpy as np
D = 256
def embed(text):                                   # TOY hashed bag-of-words, L2-normalised
    v = np.zeros(D)
    for w in text.lower().split(): v[zlib.crc32(w.encode()) % D] += 1
    n = np.linalg.norm(v); return v / n if n else v

DOCS = [("t1", "refund policy for tenant one orders"), ("t1", "shipping times for tenant one"),
        ("t2", "refund policy for tenant two secret pricing"), ("t2", "tenant two internal roadmap refund notes"),
        ("t3", "refund policy tenant three")]
chunks = [{"id": f"c{i}", "tenant": t, "text": x, "vec": embed(x)} for i, (t, x) in enumerate(DOCS)]

def search_no_filter(caller, q, k=3):              # BUG: nothing ties results to the caller
    qv = embed(q); s = sorted(chunks, key=lambda c: -float(c["vec"] @ qv)); return s[:k]

def search_filter(caller, q, k=3):                 # tenant predicate applied BEFORE ranking (pre-filter)
    qv = embed(q); pool = [c for c in chunks if c["tenant"] == caller]
    return sorted(pool, key=lambda c: -float(c["vec"] @ qv))[:k]

NAMESPACES = {}                                    # one index per tenant: no cross-tenant path exists
for c in chunks: NAMESPACES.setdefault(c["tenant"], []).append(c)
def search_namespace(caller, q, k=3):
    qv = embed(q); return sorted(NAMESPACES.get(caller, []), key=lambda c: -float(c["vec"] @ qv))[:k]

def assert_no_leak(search_fn, queries, callers):    # the test harness
    leaks = []
    for caller in callers:
        for q in queries:
            for c in search_fn(caller, q):
                if c["tenant"] != caller: leaks.append((caller, q, c["id"], c["tenant"]))
    return leaks

QUERIES = ["refund policy", "tenant two internal roadmap", "secret pricing", "shipping"]
for name, fn in [("no filter (buggy)", search_no_filter), ("pre-filter", search_filter), ("namespace", search_namespace)]:
    leaks = assert_no_leak(fn, QUERIES, ["t1", "t2", "t3", "unknown"])
    print(f"{name:18s} leaks={len(leaks)}", leaks[:2])
assert assert_no_leak(search_filter, QUERIES, ["t1", "t2", "t3", "unknown"]) == []
assert assert_no_leak(search_namespace, QUERIES, ["t1", "t2", "t3", "unknown"]) == []
print("tests passed for pre-filter and namespace")
