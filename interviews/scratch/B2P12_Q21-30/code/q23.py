# Q23 toy legal RAG: structure-aware chunks, hybrid (BM25 + char-ngram "dense"), supersession, abstention. Synthetic statute text.
import math, re
from collections import Counter
DOCS = [
 dict(id="Act-A/s5(v1)", sec="Section 5 Notice period", text="Section 5. The notice period for termination is 30 days.", eff="2018-01-01", sup=None),
 dict(id="Act-A/s5(v2)", sec="Section 5 Notice period", text="Section 5 as amended. The notice period for termination is 60 days.", eff="2023-04-01", sup=None),
 dict(id="Act-A/s9", sec="Section 9 Penalty", text="Section 9. A late filing attracts a fixed penalty set by the schedule.", eff="2018-01-01", sup=None),
 dict(id="Act-A/s12", sec="Section 12 Appeals", text="Section 12. An appeal must be filed within 45 days of the order.", eff="2018-01-01", sup=None),
]
DOCS[0]["sup"] = "Act-A/s5(v2)"
STOP = {"what", "is", "the", "a", "of", "for", "on", "an", "are", "to", "in"}
def tok(s): return [w for w in re.findall(r"[a-z0-9]+", s.lower()) if w not in STOP]
def bm25(q, docs, k1=1.5, b=0.75):
    N = len(docs); avg = sum(len(tok(d["text"])) for d in docs) / N
    df = Counter(w for d in docs for w in set(tok(d["text"])))
    sc = {}
    for d in docs:
        tf = Counter(tok(d["text"])); L = len(tok(d["text"])); s = 0
        for w in tok(q):
            if w in tf: s += math.log(1 + (N - df[w] + .5) / (df[w] + .5)) * tf[w] * (k1 + 1) / (tf[w] + k1 * (1 - b + b * L / avg))
        sc[d["id"]] = s
    return sc
def ngrams(s, n=3): s = " ".join(tok(s)); return Counter(s[i:i + n] for i in range(len(s) - n + 1))
def cos(a, b):
    dot = sum(v * b.get(k, 0) for k, v in a.items()); return dot / (math.sqrt(sum(v * v for v in a.values())) * math.sqrt(sum(v * v for v in b.values())) + 1e-9)
def dense(q, docs): qn = ngrams(q); return {d["id"]: cos(qn, ngrams(d["sec"] + " " + d["text"])) for d in docs}
def rrf(rank_lists, k=60):
    f = Counter()
    for r in rank_lists:
        for i, d in enumerate(r): f[d] += 1 / (k + i + 1)
    return f
def search(q, as_of=None, include_superseded=False, abstain_below=0.02):
    docs = [d for d in DOCS if include_superseded or d["sup"] is None]
    if as_of: docs = [d for d in docs if d["eff"] <= as_of]
    b, e = bm25(q, docs), dense(q, docs)
    fused = rrf([sorted(b, key=b.get, reverse=True), sorted(e, key=e.get, reverse=True)])
    top = fused.most_common(2)
    if not top or max(b.values()) < 1.0 and max(e.values()) < 0.25: return "ABSTAIN: no passage supports an answer; refer to a lawyer", []
    return None, [(i, round(s, 4)) for i, s in top]
for q, kw in [("what is the notice period for termination", {}),
              ("what is the notice period for termination", dict(include_superseded=True)),
              ("notice period for termination", dict(as_of="2020-01-01", include_superseded=True)),
              ("what is the tax rate on crypto gifts", {})]:
    msg, res = search(q, **kw); print(q[:42], kw, "->", msg or res)
# tests
assert search("what is the notice period for termination")[1][0][0] == "Act-A/s5(v2)"
assert search("notice period for termination", as_of="2020-01-01", include_superseded=True)[1][0][0] == "Act-A/s5(v1)"
assert search("what is the tax rate on crypto gifts")[0].startswith("ABSTAIN")
print("tests passed: current version by default; as-of date returns the then-valid version; out-of-corpus question abstains")
