# TOY: tenant isolation in retrieval and caching. Hash-based 8-dim embeddings, numpy only.
import numpy as np, hashlib
def emb(text):
    v = np.zeros(8)
    for w in text.lower().split(): v[int(hashlib.md5(w.encode()).hexdigest(), 16) % 8] += 1
    return v / (np.linalg.norm(v) or 1)
corpus = [("A", "refund policy for acme enterprise customers is 30 days"), ("A", "acme confidential pricing sheet discount 40 percent"),
          ("B", "refund policy for globex customers is 14 days"), ("B", "globex confidential pricing sheet discount 10 percent"),
          ("B", "globex refund policy exceptions need vp sign off"), ("B", "refund policy faq globex retail")]
E = np.stack([emb(t) for _, t in corpus]); tenants = np.array([t for t, _ in corpus])
def search(q, tenant, mode, k=2):
    s = E @ emb(q)
    if mode == "post":                       # BUG pattern: take global top-k, then filter
        top = np.argsort(-s)[:k]; return [i for i in top if tenants[i] == tenant]
    if mode == "pre":                        # filter first, then rank inside the allowed set
        idx = np.where(tenants == tenant)[0]; return list(idx[np.argsort(-s[idx])][:k])
    if mode == "none": return list(np.argsort(-s)[:k])
q = "refund policy"
for mode in ["none", "post", "pre"]:
    r = search(q, "A", mode); leaked = [corpus[i][1][:28] for i in r if tenants[i] != "A"]
    print(f"{mode:5} tenant A got {len(r)} hits, cross-tenant leaks: {len(leaked)} {leaked}")

class Cache:
    def __init__(self, keyed): self.d, self.keyed, self.hits = {}, keyed, 0
    def key(self, q, tenant, scope): return (q, tenant, scope) if self.keyed else q
    def get_or_compute(self, q, tenant, scope, fn):
        k = self.key(q, tenant, scope)
        if k in self.d: self.hits += 1; return self.d[k]
        self.d[k] = fn(); return self.d[k]
answer = lambda tenant: f"answer built from {tenant}'s documents"
for keyed in [False, True]:
    c = Cache(keyed); a = c.get_or_compute("what is our discount?", "A", "all", lambda: answer("A"))
    b = c.get_or_compute("what is our discount?", "B", "all", lambda: answer("B"))
    print(f"cache key includes tenant={keyed}: tenant B received: '{b}'")

# leakage test: plant a unique marker per tenant, query as every tenant with many queries, assert no foreign marker
markers = {t: f"MARK-{t}-9f3" for t in "AB"}
corpus2 = corpus + [("A", f"acme note {markers['A']}"), ("B", f"globex note {markers['B']}")]
E2 = np.stack([emb(t) for _, t in corpus2]); ten2 = np.array([t for t, _ in corpus2])
def search2(q, tenant, mode, k=3):
    s = E2 @ emb(q); idx = np.where(ten2 == tenant)[0] if mode == "pre" else np.arange(len(s))
    return [corpus2[i][1] for i in idx[np.argsort(-s[idx])][:k]]
queries = ["note", "refund policy", "pricing sheet discount", "confidential", "customers", "faq", "vp sign off"]
for mode in ["none", "pre"]:
    viol = sum(markers["B" if t == "A" else "A"] in " ".join(search2(q, t, mode)) for t in "AB" for q in queries)
    print(f"leak test mode={mode}: violations in {2*len(queries)} tenant-query pairs = {viol}")
