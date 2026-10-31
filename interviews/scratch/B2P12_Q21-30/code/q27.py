# Q27 toy multi-tenant "chat with your data": shared index with tenant filter inside search, dedicated index for big tenants,
# canary isolation tests, token-bucket noisy-neighbour limit, cost attribution, offboarding with deletion proof. Embeddings are toy.
import numpy as np, hashlib, time
D = 16
def emb(text):
    v = np.zeros(D)
    for w in text.lower().split(): v[int(hashlib.md5(w.encode()).hexdigest(), 16) % D] += 1
    n = np.linalg.norm(v); return v / n if n else v
class Shared:
    def __init__(self): self.v, self.meta = np.zeros((0, D)), []
    def add(self, tenant, doc_id, text): self.v = np.vstack([self.v, emb(text)]); self.meta.append(dict(t=tenant, id=doc_id, text=text, dead=False))
    def search(self, tenant, q, k=3):
        mask = np.array([m["t"] == tenant and not m["dead"] for m in self.meta])      # filter INSIDE the search
        if not mask.any(): return []
        s = np.where(mask, self.v @ emb(q), -np.inf); idx = [i for i in np.argsort(-s)[:k] if np.isfinite(s[i])]
        return [self.meta[i]["id"] for i in idx]
    def delete_tenant(self, tenant):
        for m in self.meta:
            if m["t"] == tenant: m["dead"] = True; m["text"] = ""
        keep = [i for i, m in enumerate(self.meta) if not (m["t"] == tenant)]
        self.v = self.v[keep]; self.meta = [self.meta[i] for i in keep]
class Bucket:  # per-tenant token bucket (injected clock so the test is deterministic)
    def __init__(self, rate, cap): self.rate, self.cap, self.tok, self.t = rate, cap, cap, 0.0
    def allow(self, now, cost=1):
        self.tok = min(self.cap, self.tok + (now - self.t) * self.rate); self.t = now
        if self.tok >= cost: self.tok -= cost; return True
        return False
idx = Shared()
for t in ("acme", "beta", "gamma"):
    for i in range(30): idx.add(t, f"{t}-{i}", f"invoice report {i} for {t} quarterly revenue")
idx.add("beta", "beta-CANARY", "canary zebra secret invoice revenue")
# isolation test: another tenant must never see the canary, even with a query built from it
for t in ("acme", "gamma"):
    r = idx.search(t, "canary zebra secret invoice revenue", k=50)
    assert "beta-CANARY" not in r and all(x.startswith(t) for x in r), r
print("isolation test: acme and gamma never receive beta-CANARY across 50 results each")
# noisy neighbour: acme sends 100 req/s for 5 s; beta sends 1 req/s. Limit 10 req/s each, burst 20 (ASSUMED)
bk = {"acme": Bucket(10, 20), "beta": Bucket(10, 20)}
served = {"acme": 0, "beta": 0}; sent = {"acme": 0, "beta": 0}
for step in range(500):
    now = step * 0.01
    sent["acme"] += 1; served["acme"] += bk["acme"].allow(now)
    if step % 100 == 0: sent["beta"] += 1; served["beta"] += bk["beta"].allow(now)
print("served/sent:", served, sent)
# cost attribution (tokens logged per request; ASSUMED price 1.0 per 1k tokens, unit-less)
log = [("acme", 1200), ("acme", 900), ("beta", 400), ("gamma", 5000)]
bill = {}
for t, tk in log: bill[t] = bill.get(t, 0) + tk / 1000
print("cost units per tenant:", bill)
# shared vs dedicated break-even with ASSUMED numbers
fixed_dedicated, shared_per_1k_vec, vecs = 200.0, 0.02, [5_000, 100_000, 5_000_000, 20_000_000]
for n in vecs: print(f"tenant with {n:>10,} vectors: shared {n / 1000 * shared_per_1k_vec:8.1f} vs dedicated {fixed_dedicated:6.1f}  (ASSUMED monthly cost units)")
# offboarding
before = len(idx.meta); idx.delete_tenant("beta")
assert idx.search("beta", "invoice", 5) == [] and len(idx.meta) == 60 and all(m["t"] != "beta" for m in idx.meta)
print("offboarding: rows", before, "->", len(idx.meta), "; no beta vectors or text remain in this store (backups, caches and logs need their own deletion)")
