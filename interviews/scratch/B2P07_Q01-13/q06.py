# MaxSim from scratch with TOY token vectors (hashed random unit vectors; synonyms share a base vector + noise).
# Not a real ColBERT model: it only shows the scoring rule and the storage arithmetic.
import re, zlib
import numpy as np
D = 32
SYN = {"car": "auto", "automobile": "auto", "repair": "fix", "mend": "fix"}
def tok_vec(w):
    base = SYN.get(w, w)
    r = np.random.default_rng(zlib.crc32(base.encode())).normal(size=D)
    if w != base: r = r + 0.35 * np.random.default_rng(zlib.crc32(w.encode())).normal(size=D)
    return r / np.linalg.norm(r)
def enc(text): return np.stack([tok_vec(w) for w in re.findall(r"[a-z]+", text.lower())])   # (tokens, D)
def maxsim(Q, Dm): return (Q @ Dm.T).max(axis=1).sum()      # sum over query tokens of best doc-token match

docs = {"A": "how to mend an automobile engine quickly", "B": "engine oil and car paint colors list",
        "C": "repair guide for the washing machine"}
doc_mats = {k: enc(v) for k, v in docs.items()}             # precomputed offline, one matrix per doc
q = enc("fix car engine")
print("MaxSim :", {k: round(float(maxsim(q, m)), 2) for k, m in doc_mats.items()})
# single-vector (mean-pooled) comparison, still the same toy vectors
def pool(m): v = m.mean(0); return v / np.linalg.norm(v)
print("pooled :", {k: round(float(pool(q) @ pool(m)), 2) for k, m in doc_mats.items()})
# per-query-token view: which doc token did each query token pick in doc A?
print("doc A best match per query token:", [(w, docs["A"].split()[int(j)]) for w, j in zip(["fix", "car", "engine"], (q @ doc_mats["A"].T).argmax(1))])

# storage arithmetic (small example): 10,000 docs x 200 tokens x 128 dims, fp16 = 2 bytes
n_docs, toks, dim = 10_000, 200, 128
col = n_docs * toks * dim * 2
bi = n_docs * 768 * 4
print(f"ColBERT-style: {col/1e9:.2f} GB (tokens x dim x bytes)   single-vector 768-d fp32: {bi/1e6:.1f} MB   ratio {col/bi:.0f}x")
