# Standalone, numpy + stdlib. TOY corpus, from-scratch BM25, TOY hashed dense vectors, MOCK reranker. Each bug is run in isolation, then fixed and tested.
import math, re, zlib, numpy as np
DOCS = {"d1": "error code ERR-4021 means payment gateway timeout retry later",
        "d2": "payment failed troubleshooting guide for card declined and timeout",
        "d3": "refund policy damaged items within thirty days",
        "d4": "how to reset your password on the mobile app",
        "d5": "gateway timeout settings and retry policy for payments api",
        "d6": "shipping carriers and delivery times",
        "d7": "card declined reasons issuer bank",
        "d8": "app login problems and password reset email not arriving"}
tok = lambda s: re.findall(r"[a-z0-9]+", s.lower())
N = len(DOCS); AVG = np.mean([len(tok(t)) for t in DOCS.values()])
DF = {}
for t in DOCS.values():
    for w in set(tok(t)): DF[w] = DF.get(w, 0) + 1
def bm25(q, k1=1.5, b=0.75):                                   # from-scratch BM25 -> raw scores (unbounded scale)
    out = {}
    for d, t in DOCS.items():
        ws = tok(t); s = 0.0
        for w in set(tok(q)) & set(ws):
            idf = math.log(1 + (N - DF[w] + .5) / (DF[w] + .5)); f = ws.count(w)
            s += idf * f * (k1 + 1) / (f + k1 * (1 - b + b * len(ws) / AVG))
        out[d] = s
    return out
CONCEPT = {"credentials": "CRED", "login": "CRED", "password": "CRED", "rejected": "DECL", "declined": "DECL"}   # TOY synonym table
def dvec(t, dim=256):                                          # TOY dense: hashed bag-of-words plus a tiny synonym table, unit length
    v = np.zeros(dim)                                          # (it is only here so dense and BM25 can disagree; no real semantics)
    for w in tok(t):
        for x in {w, CONCEPT.get(w, w)}: v[zlib.crc32(x.encode()) % dim] += 1
    return v / (np.linalg.norm(v) or 1)
DV = {d: dvec(t) for d, t in DOCS.items()}
def dense(q): qv = dvec(q); return {d: float(DV[d] @ qv) for d in DOCS}
ranked = lambda sc: [d for d, s in sorted(sc.items(), key=lambda x: (-x[1], x[0])) if s > 0]

# ---------- BUG 1: RRF rank starts at 0 ----------
def rrf_buggy(lists, k=60):
    s = {}
    for L in lists:
        for r, d in enumerate(L): s[d] = s.get(d, 0) + 1 / (k + r)          # BUG: r starts at 0
    return sorted(s, key=lambda d: -s[d])
def rrf(lists, k=60):
    s = {}
    for L in lists:
        for r, d in enumerate(dict.fromkeys(L), 1): s[d] = s.get(d, 0) + 1 / (k + r)   # rank from 1; duplicates inside a list ignored
    return sorted(s, key=lambda d: (-s[d], d))
L1, L2 = ["A", "B", "X"], ["Y", "Z", "B"]       # A: rank 1 in one list; B: rank 2 and 3
print("BUG1 k=1 buggy:", rrf_buggy([L1, L2], k=1)[:2], "| fixed:", rrf([L1, L2], k=1)[:2])
try: rrf_buggy([["A"]], k=0)
except ZeroDivisionError: print("BUG1 k=0 with 0-based rank: ZeroDivisionError")
assert rrf([L1, L2], k=1)[0] == "B" and rrf_buggy([L1, L2], k=1)[0] == "A"

# ---------- BUG 2: mixing raw BM25 and dense scores ----------
q = "rejected card for the app"
bm, de = bm25(q), dense(q)
print("BUG2 score ranges: bm25 max %.2f, dense max %.2f" % (max(bm.values()), max(de.values())))
mixed = {d: 0.5 * bm[d] + 0.5 * de[d] for d in DOCS}
print("BUG2 'alpha=0.5' mix top-3:", ranked(mixed)[:3], "| bm25 alone:", ranked(bm)[:3], "| dense alone:", ranked(de)[:3])
def minmax(sc): lo, hi = min(sc.values()), max(sc.values()); return {d: (s - lo) / (hi - lo) if hi > lo else 0.0 for d, s in sc.items()}
fixed = {d: 0.5 * minmax(bm)[d] + 0.5 * minmax(de)[d] for d in DOCS}
print("FIX2 min-max normalised mix top-3:", ranked(fixed)[:3], "(gold = d2: a declined card)")
assert ranked(mixed)[:3] == ranked(bm)[:3] and ranked(fixed)[0] == "d2"

# ---------- BUG 3: reranking the wrong / truncated / unsorted list ----------
def mock_reranker(q, d): return len(set(tok(q)) & set(tok(DOCS[d]))) + (0.5 if tok(q)[0] in tok(DOCS[d]) else 0)   # MOCK cross-encoder
def rerank_buggy(q, bm_hits, fused, n=3):
    cand = bm_hits[:n]                                          # BUG: reranks the BM25 list, not the fused one, and only n=3
    return sorted(cand, key=lambda d: mock_reranker(q, d))      # BUG: ascending, worst first
def rerank(q, fused, n=50):
    return sorted(fused[:n], key=lambda d: (-mock_reranker(q, d), fused.index(d)))
q = "reset password login"
bm_hits, de_hits = ranked(bm25(q)), ranked(dense(q)); fused = rrf([bm_hits, de_hits])
print("BUG3 gold d8; fused:", fused[:4], "| buggy rerank:", rerank_buggy(q, bm_hits, fused), "| fixed rerank:", rerank(q, fused)[:3])
assert rerank(q, fused)[0] in ("d4", "d8") and rerank_buggy(q, bm_hits, fused)[0] != rerank(q, fused)[0]

# ---------- BUG 4: duplicates after fusion counted twice ----------
dup = ["d3", "d3", "d6"]                          # e.g. two multi-query variants returned d3; d6 is the better-placed unique hit elsewhere
other = ["d6", "d4"]
def fuse_buggy(lists, k=60):
    s = {}
    for L in lists:
        for r, d in enumerate(L, 1): s[d] = s.get(d, 0) + 1 / (k + r)
    return sorted(s, key=lambda d: -s[d])
print("BUG4 buggy fused:", fuse_buggy([dup, other])[:3], "| fixed:", rrf([dup, other])[:3])
assert fuse_buggy([dup, other])[0] == "d3" and rrf([dup, other])[0] == "d6"
chunks = ["d1", "d1", "d2"]; assert len(set(chunks)) < len(chunks); final = list(dict.fromkeys(chunks)); assert final == ["d1", "d2"]   # dedupe the final list too

# ---------- BUG 5: dropping the original query when rewriting ----------
def rewrite(q): return "what does this failure mean"             # MOCK rewriter: fluent but loses the identifier
def retrieve_buggy(q): return ranked(bm25(rewrite(q)))[:3]
def retrieve(q): return rrf([ranked(bm25(q))[:10], ranked(bm25(rewrite(q)))[:10]])[:3]   # keep the ORIGINAL query alongside the rewrite
print("BUG5 buggy (rewrite only):", retrieve_buggy("ERR-4021"), "| fixed (original + rewrite):", retrieve("ERR-4021"))
assert "d1" not in retrieve_buggy("ERR-4021") and retrieve("ERR-4021")[0] == "d1"
print("all checks passed")
