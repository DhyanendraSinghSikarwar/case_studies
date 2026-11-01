# BM25 from scratch vs a TOY dense retriever (hand-made synonym clusters + hashed unknown tokens).
# The "dense" model is a toy, NOT a real embedding model; it only shows complementary failures.
import re, math, zlib
import numpy as np

def toks(t): return re.findall(r"[a-z0-9]+", t.lower())
docs = {
 "d1": "Error E4021 means the payment gateway timed out",
 "d2": "Error E4012 means the card was declined by the bank",
 "d3": "To get your money back submit a refund request within 30 days",
 "d4": "A password reset link is sent to your registered email",
 "d5": "Error E4099 means the invoice could not be generated",
 "d6": "Our cancellation policy lets you terminate the subscription any time",
}
ids = list(docs)

def bm25(q, k1=1.5, b=0.75):
    D = [toks(docs[i]) for i in ids]; N = len(D); avg = sum(map(len, D)) / N
    df = {}
    for d in D:
        for w in set(d): df[w] = df.get(w, 0) + 1
    out = []
    for d in D:
        s = 0.0
        for w in toks(q):
            if w not in df: continue
            idf = math.log(1 + (N - df[w] + 0.5) / (df[w] + 0.5))
            tf = d.count(w)
            s += idf * tf * (k1 + 1) / (tf + k1 * (1 - b + b * len(d) / avg))
        out.append(s)
    return np.array(out)

CONCEPTS = [{"refund", "reimbursement", "money", "back", "repay"},
            {"password", "login", "credentials", "reset"},
            {"payment", "gateway", "card", "invoice", "bank"},
            {"error", "failure", "problem", "code", "means"},
            {"cancellation", "cancel", "terminate", "unsubscribe", "subscription"}]
def dense(text, hdim=16):
    v = np.zeros(len(CONCEPTS) + hdim)
    for w in toks(text):
        hit = [i for i, c in enumerate(CONCEPTS) if w in c]
        for i in hit: v[i] += 1
        if not hit: v[len(CONCEPTS) + zlib.crc32(w.encode()) % hdim] += 0.3
    n = np.linalg.norm(v); return v / n if n else v
DE = np.stack([dense(docs[i]) for i in ids])

tests = [("E4021", "d1"), ("reimbursement please", "d3"), ("unsubscribe", "d6"), ("payment gateway error E4021", "d1")]
def rank_map(sc, drop_zero=False):
    order = [j for j in np.argsort(-sc, kind="stable") if not (drop_zero and sc[j] <= 0)]
    return {ids[j]: r + 1 for r, j in enumerate(order)}   # docs a ranker did not return are absent
def rrf_top1(q, k=60, drop_zero=True):
    rb, rd = rank_map(bm25(q), drop_zero), rank_map(DE @ dense(q))
    return max(ids, key=lambda i: sum(1 / (k + m[i]) for m in (rb, rd) if i in m))
for q, gold in tests:
    sb = bm25(q); sd = DE @ dense(q)
    rb = [ids[j] for j in np.argsort(-sb, kind="stable")][0] if sb.max() > 0 else "none (all scores 0)"
    rd = ids[int(np.argmax(sd))]
    print(f"q={q!r:32} gold={gold}  BM25 top1={rb:20} dense top1={rd}  RRF top1={rrf_top1(q)}")
print("trap: if BM25 zero-score ties are ranked anyway, RRF top1 for 'unsubscribe' =", rrf_top1("unsubscribe", drop_zero=False))
