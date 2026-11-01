# Standalone, numpy only. TOY store and TOY hashed embeddings; each bug is shown in isolation, then the fixed version is tested.
import zlib, re, numpy as np

def embed_a(text, d=64):                       # "model A" (toy hashed bag-of-words), NOT normalised
    v = np.zeros(d)
    for w in re.findall(r"\w+", text.lower()): v[zlib.crc32(w.encode()) % d] += 1
    return v
def embed_b(text, d=64):                       # "model B": same dimension, different hash salt = different space
    v = np.zeros(d)
    for w in re.findall(r"\w+", text.lower()): v[zlib.crc32(b"salt" + w.encode()) % d] += 1
    return v
def unit(v): n = np.linalg.norm(v); return v / n if n else v

DOCS = {"d1": "refund policy for damaged items", "d2": "shipping times and carriers for international orders",
        "d3": "password reset steps for the mobile app", "d4": "invoice and tax details for business customers",
        "d5": "warranty claim process and repair centres"}
Q = {"d1": "refund damaged items", "d2": "international shipping carriers", "d3": "reset password mobile",
     "d4": "business tax invoice", "d5": "warranty repair claim"}

# ---------------- Bug 1: embedder mismatch between ingest and query ----------------
M = np.stack([embed_a(t) for t in DOCS.values()]); ids = list(DOCS)
def hit1(qfn, m=M):
    return np.mean([ids[int(np.argmax(m @ qfn(q)))] == d for d, q in Q.items()])
print("BUG1 same model recall@1:", hit1(embed_a), "| ingest A, query B (same dim):", hit1(embed_b))
try: M @ embed_a("x", d=32)
except ValueError as e: print("BUG1 dimension mismatch raises:", str(e)[:40], "...")
# FIX: store embedder name + dim next to the index and assert on every query
class Index:
    def __init__(self, name, dim): self.name, self.dim, self.vecs, self.ids = name, dim, [], []
    def add(self, i, v, name): assert name == self.name and len(v) == self.dim; self.ids.append(i); self.vecs.append(unit(v))
    def search(self, v, name, k=3):
        assert name == self.name and len(v) == self.dim, "embedder mismatch"
        s = np.stack(self.vecs) @ unit(v); o = np.argsort(-s)[:k]; return [(self.ids[j], float(s[j])) for j in o]
idx = Index("A-64", 64)
for d, t in DOCS.items(): idx.add(d, embed_a(t), "A-64")
try: idx.search(embed_b("refund"), "B-64")
except AssertionError as e: print("FIX1 rejects:", e)

# ---------------- Bug 2: dot product on unnormalised vectors, assumed cosine ----------------
short = "refund damaged items"; long_ = ("refund damaged items " + "warranty repair claim process centres ") * 6
cands = {"short_relevant": embed_a(short), "long_offtopic": embed_a(long_)}
q = embed_a("refund damaged items")
print("BUG2 dot:", {k: round(float(v @ q), 2) for k, v in cands.items()},
      "| cosine:", {k: round(float(unit(v) @ unit(q)), 2) for k, v in cands.items()})

# ---------------- Bug 3: filter applied after top-k ----------------
rng = np.random.default_rng(0); N = 2000
V = np.stack([unit(rng.normal(size=32)) for _ in range(N)]); tenant = rng.integers(0, 20, N)   # 5% of chunks per tenant
qv = unit(rng.normal(size=32)); k = 10
top = np.argsort(-(V @ qv))[:k]; post = [i for i in top if tenant[i] == 3]
s = V @ qv; s[tenant != 3] = -9; pre = np.argsort(-s)[:k]
print(f"BUG3 filter after top-{k}: {len(post)} results | filter before ranking: {len(pre)} results")

# ---------------- Bug 4: delete updates metadata table only ----------------
class Store:
    def __init__(self): self.meta, self.vecs, self.ids = {}, [], []
    def add(self, i, text, deleted_ok=False): self.meta[i] = {"text": text, "deleted": False}; self.ids.append(i); self.vecs.append(unit(embed_a(text)))
    def delete_buggy(self, i): self.meta[i]["deleted"] = True             # vector stays in the index
    def delete_fixed(self, i):
        j = self.ids.index(i); self.ids.pop(j); self.vecs.pop(j); self.meta.pop(i)
    def search(self, text): s = np.stack(self.vecs) @ unit(embed_a(text)); return self.ids[int(np.argmax(s))]
st = Store(); [st.add(d, t) for d, t in DOCS.items()]
st.delete_buggy("d1"); print("BUG4 after metadata-only delete, top hit for 'refund damaged items':", st.search("refund damaged items"))
st2 = Store(); [st2.add(d, t) for d, t in DOCS.items()]
st2.delete_fixed("d1"); print("FIX4 after real delete, top hit:", st2.search("refund damaged items"))

# ---------------- Bug 5: off-by-one overlap ----------------
def chunk_buggy(tokens, size, overlap):
    out, s = [], 0
    while s < len(tokens): out.append(tokens[s:s + size]); s += size - overlap + 1   # BUG: step too big by 1
    return out
def chunk_fixed(tokens, size, overlap):
    assert 0 <= overlap < size
    out, s = [], 0
    while True:
        out.append(tokens[s:s + size])
        if s + size >= len(tokens): break
        s += size - overlap
    return out
toks = list(range(20)); size = 8
for name, fn, ov in [("buggy ov=2", chunk_buggy, 2), ("fixed ov=2", chunk_fixed, 2), ("buggy ov=0", chunk_buggy, 0), ("fixed ov=0", chunk_fixed, 0)]:
    ch = fn(toks, size, ov); covered = set(t for c in ch for t in c)
    ovl = [len(set(a) & set(b)) for a, b in zip(ch, ch[1:])]
    print(f"BUG5 {name}: chunks={len(ch)} missing tokens={sorted(set(toks) - covered)} overlaps={ovl}")
f = chunk_fixed(toks, size, 2); assert set(t for c in f for t in c) == set(toks) and all(len(set(a) & set(b)) == 2 for a, b in zip(f, f[1:]))

# ---------------- Bug 6: chunk by characters, budget in tokens ----------------
def toy_tokens(s): return re.findall(r"[A-Za-z]{1,4}|\d|[^\sA-Za-z\d]", s)   # TOY tokenizer: <=4 letters, single digits, symbols
prose = "the cat sat on the mat. " * 40
code_ = "x=[1,2,3];y={'a':42};" * 40
for name, text in [("prose", prose), ("numbers/code", code_)]:
    c = text[:600]; print(f"BUG6 {name}: 600-char chunk = {len(toy_tokens(c))} toy tokens (budget 150)")
def chunk_by_tokens(text, budget): t = toy_tokens(text); return ["".join(t[i:i + budget]) for i in range(0, len(t), budget)]
assert all(len(toy_tokens(c)) <= 150 for c in chunk_by_tokens(code_, 150)); print("FIX6 token-based chunks all <= 150 toy tokens")
