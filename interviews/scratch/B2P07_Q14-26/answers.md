### Q14 ⭐⭐⭐ 🟡 How do you evaluate each advanced-RAG component (hybrid, reranker, rewriting) with ablations, and what do you report besides accuracy?
**Asked at:** product, GenAI startups, GCC, evaluation-focused rounds
**Say this first (1 line):** Freeze one golden set, switch one component on or off at a time, compare per query (paired), and report the quality gain with a confidence interval next to latency p50/p95 and cost per query, not accuracy alone.

**Then explain:**
- **One change at a time, same queries:** baseline, then +hybrid, +reranker, +rewriting, then the full stack, all on the same golden set (golden-set design: Part 6 Q40). If two things change together you cannot say which one helped.
- **Retrieval metrics first:** recall@k, MRR, nDCG at the stage each component touches (rewriting and hybrid move first-stage recall, the reranker moves ordering). Then answer-level faithfulness and correctness, because better retrieval does not always give better answers (depth: Part 9).
- **Failures fixed vs introduced:** a +4 point average can hide 30 queries fixed and 10 broken. List both; the broken ones show what the component hurts (for example rewriting hurting exact-ID queries).
- **Paired bootstrap:** resample queries (same indices for both variants), compute the mean difference each time, read a 95% interval. If it straddles zero, do not claim a win. Golden sets are small, so this matters.
- **Cost beside effect size:** p50 and p95 latency (p95 is what users feel), cost per query, and extra cost per extra query fixed. A 2-point gain that doubles p95 may not ship.
- **Interactions:** components overlap. A reranker may give less on top of hybrid than alone, because hybrid already fixed some of the same misses. Test the 2x2 grid, do not just add single gains.

**Example:** Everything below is SYNTHETIC. 200 queries, hybrid-only hit@5 is 0.565, hybrid plus reranker is 0.650: a gain of +0.085 with a 95% CI of [+0.035, +0.135], so it is probably real. The reranker fixed 22 queries and broke 5. It adds about 60 ms at p50 and costs an ASSUMED 0.0004 more per query. The 2x2 interaction of -0.04 says the two components partly fix the same queries.

**Code:** (run; synthetic per-query results, assumed costs, numpy only)
```python
import numpy as np
rng = np.random.default_rng(0)
N = 200  # queries in a SYNTHETIC golden set

# Per-query "hit@5" (1 = right chunk in top 5) for two pipelines, generated synthetically.
base = rng.random(N) < 0.62                       # variant A: hybrid only
fix  = (~base) & (rng.random(N) < 0.25)           # reranker fixes some misses
brk  = base & (rng.random(N) < 0.05)              # ...and breaks a few hits
B = (base | fix) & ~brk                           # variant B: hybrid + reranker
# Per-query latency (ms), synthetic lognormal; reranker adds a per-query cost
latA = rng.lognormal(np.log(120), 0.35, N)
latB = latA + rng.lognormal(np.log(60), 0.5, N)

def paired_bootstrap(a, b, n_boot=5000, seed=1):
    r = np.random.default_rng(seed); d = b.astype(float) - a.astype(float)
    idx = r.integers(0, len(d), (n_boot, len(d)))   # resample QUERIES, same indices for both variants
    means = d[idx].mean(1)
    return d.mean(), np.percentile(means, [2.5, 97.5])

delta, ci = paired_bootstrap(base, B)
print(f"hit@5  A={base.mean():.3f}  B={B.mean():.3f}  delta={delta:+.3f}  95% CI [{ci[0]:+.3f}, {ci[1]:+.3f}]")
print("failures fixed:", int((~base & B).sum()), " introduced:", int((base & ~B).sum()))
print("latency p50/p95 ms  A:", np.percentile(latA, [50, 95]).round(0), " B:", np.percentile(latB, [50, 95]).round(0))

# Cost table: ASSUMED per-query numbers (synthetic), not a real price list
cost = {"A: hybrid": 0.0010, "B: hybrid + reranker": 0.0014}   # assumed currency units per query
for name, hit in [("A: hybrid", base), ("B: hybrid + reranker", B)]:
    print(f"{name:22s} hit@5={hit.mean():.3f}  cost/query={cost[name]:.4f}")
extra = cost["B: hybrid + reranker"] - cost["A: hybrid"]
print(f"extra cost per extra hit: {extra / (B.mean() - base.mean()):.4f} per query-hit gained (assumed units)")

# Interaction: 2x2 grid (hybrid? rerank?) on synthetic hit rates
grid = {(0,0):0.50, (1,0):0.58, (0,1):0.60, (1,1):0.64}
inter = grid[(1,1)] - grid[(1,0)] - grid[(0,1)] + grid[(0,0)]
print("interaction (gain from both minus sum of single gains):", round(inter, 3))
```
Output (my run, synthetic):
```
hit@5  A=0.565  B=0.650  delta=+0.085  95% CI [+0.035, +0.135]
failures fixed: 22  introduced: 5
latency p50/p95 ms  A: [119. 207.]  B: [182. 278.]
A: hybrid              hit@5=0.565  cost/query=0.0010
B: hybrid + reranker   hit@5=0.650  cost/query=0.0014
extra cost per extra hit: 0.0047 per query-hit gained (assumed units)
interaction (gain from both minus sum of single gains): -0.04
```

**Follow-ups:**
- *How big a golden set?* Big enough that the interval is narrower than the gain you care about; with 200 queries the interval above is about +/-5 points. Stratify by query type so one type does not hide another.
- *Why paired, not two separate intervals?* Both variants see the same queries, so the per-query difference removes query difficulty and gives a tighter interval.
- *Offline win but no online win?* Check the golden set matches real traffic; confirm with an online test (Book 1 Part 10).

**Common mistakes:** changing two things at once; reporting only the mean with no interval; ignoring queries the change broke; ignoring p95 and cost; tuning on the golden set and reporting on it (keep a held-out slice); assuming gains add up across components.

### Q15 ⭐⭐⭐ 🟡 Code: implement hybrid retrieval from scratch (BM25 plus a toy dense retriever) with RRF and weighted fusion, and compare them on a toy query set.
**Asked at:** product, big tech, live-coding rounds
**Say this first (1 line):** Write BM25 and a dense scorer separately, then fuse either by ranks (RRF: sum of 1/(k + rank)) or by normalising scores (min-max) and taking a weighted sum, and measure recall@k and MRR per query type.

**Then explain:**
- **BM25:** IDF times a saturated term frequency with length normalisation. k1 = 1.5 and b = 0.75 are common defaults (from memory, not re-verified here).
- **Dense:** here a TOY (hashed bag-of-words, random projection, plus a hand-written synonym map that fakes paraphrase awareness). It shows the fusion mechanics only; it says nothing about real embedding quality.
- **RRF:** uses ranks only, so no calibration. Weakness: a ranker with no signal (BM25 scoring all zeros on a paraphrase query) still gets a rank order and votes.
- **Weighted fusion:** min-max each score list to [0,1], then alpha * sparse + (1 - alpha) * dense. It uses score gaps, so it can do better, but it needs normalisation and tuning of alpha (Part 7 Q4, Q17).
- **Report by query type:** exact-token queries and paraphrase queries behave differently; one overall number hides that.

**Example:** Toy set of 12 chunks and 10 queries (5 exact like "ZX-900", 5 paraphrase like "how do I get reimbursement"). BM25 gets all exact queries and almost none of the paraphrases; the toy dense is the reverse. Plain RRF recovered the exact queries but only 2 of 5 paraphrases in the top 3, because BM25's all-zero list still voted. Skipping a zero-signal ranker lifted it to 4 of 5. With 10 queries and a hand-built embedder, do not conclude that weighted beats RRF in general; the point is the mechanics and the per-type view.

**Code:** (run; numpy only; TOY dense, toy queries)
```python
import re, math, zlib
import numpy as np

def toks(t): return re.findall(r"[a-z0-9]+", t.lower())

# ---- Toy corpus: 12 support chunks ----
docs = [
 "Error E4021 means the payment gateway timed out",                  # 0
 "Error E4012 means the card was declined by the bank",              # 1
 "Error E4099 means the invoice could not be generated",             # 2
 "To get your money back submit a refund request within 30 days",    # 3
 "A password reset link is sent to your registered email",           # 4
 "Part ZX-900 is the replacement fan for the rack server",           # 5
 "Part ZX-901 is the replacement battery for the rack server",       # 6
 "You can change the plan or cancel the subscription in settings",   # 7
 "Two factor login codes expire after five minutes",                 # 8
 "The invoice is emailed on the first day of each month",            # 9
 "Contact support through chat for any billing dispute",             # 10
 "Delivery usually takes three to five working days",                # 11
]
# queries: (text, relevant doc, kind)
Q = [("E4021", 0, "exact"), ("E4099", 2, "exact"), ("ZX-900", 5, "exact"), ("ZX-901", 6, "exact"),
     ("E4012 declined", 1, "exact"),
     ("how do I get reimbursement", 3, "para"), ("forgot my login credentials", 4, "para"),
     ("stop my membership", 7, "para"), ("when will my parcel arrive", 11, "para"),
     ("complaint about charge", 10, "para")]

# ---- BM25 from scratch; k1=1.5, b=0.75 are common defaults (from memory) ----
D = [toks(d) for d in docs]; N = len(D); avg = sum(map(len, D)) / N
df = {}
for d in D:
    for w in set(d): df[w] = df.get(w, 0) + 1
def bm25(q, k1=1.5, b=0.75):
    out = np.zeros(N)
    for j, d in enumerate(D):
        for w in toks(q):
            if w not in df: continue
            idf = math.log(1 + (N - df[w] + 0.5) / (df[w] + 0.5))
            tf = d.count(w)
            out[j] += idf * tf * (k1 + 1) / (tf + k1 * (1 - b + b * len(d) / avg))
    return out

# ---- TOY dense: hashed bag-of-words -> fixed random projection. A hand-written synonym map
#      is applied before hashing to fake "paraphrase awareness". NOT a real embedding model. ----
SYN = {"reimbursement": "refund", "money": "refund", "back": "refund", "credentials": "password",
       "forgot": "password", "login": "password", "membership": "subscription", "stop": "cancel",
       "parcel": "delivery", "arrive": "delivery", "complaint": "dispute", "charge": "billing"}
H, DIM = 64, 24
P = np.random.default_rng(0).normal(size=(H, DIM))
def dense(text):
    v = np.zeros(H)
    for w in toks(text): v[zlib.crc32(SYN.get(w, w).encode()) % H] += 1
    e = v @ P; n = np.linalg.norm(e); return e / n if n else e
DE = np.stack([dense(d) for d in docs])

def ranks(s):  # rank dict, 1 = best
    o = np.argsort(-s, kind="stable"); r = np.empty(N, int); r[o] = np.arange(1, N + 1); return r
def rrf(sa, sb, k=60): return 1 / (k + ranks(sa)) + 1 / (k + ranks(sb))
def rrf_nz(sa, sb, k=60):  # skip a ranker that has no signal (all-zero scores)
    out = np.zeros(N)
    for s in (sa, sb):
        if s.max() > 0: out += 1 / (k + ranks(s))
    return out
def mm(s): return (s - s.min()) / (s.max() - s.min() + 1e-12)
def wfuse(sa, sb, alpha=0.5): return alpha * mm(sa) + (1 - alpha) * mm(sb)

def evaluate(score_fn, k=3):
    rec, rr = 0, 0.0
    for q, rel, _ in Q:
        order = np.argsort(-score_fn(q), kind="stable")
        pos = int(np.where(order == rel)[0][0]) + 1
        rec += pos <= k; rr += 1 / pos
    return rec / len(Q), rr / len(Q)

methods = {
 "BM25":     bm25,
 "dense(toy)": lambda q: DE @ dense(q),
 "RRF k=60": lambda q: rrf(bm25(q), DE @ dense(q)),
 "RRF skip-zero": lambda q: rrf_nz(bm25(q), DE @ dense(q)),
 "weighted a=0.5": lambda q: wfuse(bm25(q), DE @ dense(q), 0.5),
}
print(f"{'method':16s} recall@3   MRR   | exact: R@3 MRR | para: R@3 MRR")
for name, f in methods.items():
    r, m = evaluate(f)
    out = []
    for kind in ("exact", "para"):
        sub = [x for x in Q if x[2] == kind]; hit = rr = 0
        for q, rel, _ in sub:
            pos = int(np.where(np.argsort(-f(q), kind="stable") == rel)[0][0]) + 1
            hit += pos <= 3; rr += 1 / pos
        out.append((hit / len(sub), rr / len(sub)))
    print(f"{name:16s} {r:7.2f} {m:6.2f}   | {out[0][0]:.2f} {out[0][1]:.2f}   | {out[1][0]:.2f} {out[1][1]:.2f}")
```
Output (my run, toy data):
```
method           recall@3   MRR   | exact: R@3 MRR | para: R@3 MRR
BM25                0.60   0.65   | 1.00 1.00   | 0.20 0.29
dense(toy)          0.80   0.67   | 0.80 0.62   | 0.80 0.72
RRF k=60            0.70   0.63   | 1.00 1.00   | 0.40 0.26
RRF skip-zero       0.90   0.82   | 1.00 1.00   | 0.80 0.64
weighted a=0.5      1.00   0.90   | 1.00 1.00   | 1.00 0.80
```

**Follow-ups:**
- *Why did RRF lose to weighted here?* With zero BM25 scores, rank order is a tie-break artefact, yet it gets a full vote. Weighted min-max gives that list all-zero scores, so it adds nothing. Real BM25 on real text rarely scores exactly zero for every chunk, but sparse signals on short queries can be weak.
- *How do you choose alpha?* Sweep it on a labelled set (a guide cited in the research notes suggests 50+ labelled queries; treat that as a rule of thumb), and check per query type.
- *What next?* Rerank the fused top n (Q18).

**Common mistakes:** fusing raw BM25 and cosine scores; sorting ties arbitrarily and calling it signal; reporting one blended metric; tuning alpha and k on 10 queries; presenting a toy-embedding result as evidence about a real model.

### Q16 ⭐⭐ 🟡 What does learned sparse retrieval (SPLADE-style) add over BM25, and where does it fit in a hybrid stack?
**Asked at:** product, search teams, research-leaning teams
**Say this first (1 line):** A learned sparse model turns text into a sparse vector over the vocabulary with learned term weights, including expansion terms the text never said, so you keep an inverted index but can match "reimbursement" to a document that says "refund".

**Then explain:**
- **Caveat on sourcing:** this answer is from memory. In my research the term SPLADE appeared only by name in a hybrid-search explainer; I did not open a paper or docs page, so treat the details as unverified and check the original paper.
- **What the model does (as I recall):** a transformer scores, for each vocabulary term, how relevant it is to the text. After a non-linearity and a sparsity-encouraging penalty, most weights are zero. The remaining weights cover original words and expansion words, with learned importance rather than plain counts.
- **Why it helps:** BM25 only matches words that literally appear. Expansion terms bridge vocabulary mismatch while keeping exact-term behaviour and the cheap inverted-index machinery. Weights are also inspectable (you can see which terms fired).
- **Costs:** you need a model forward pass at index time and at query time, and expansion makes posting lists longer than plain BM25. Domain shift can matter, as for any learned model.
- **In a hybrid stack:** it can replace BM25 as the sparse leg, or sit beside it, then fuse with dense (Part 7 Q2, Q3). It does not remove the need to test exact identifiers like "E4021".

**Example:** Toy only. A refund chunk says "refund". The user types "reimbursement". Plain term matching finds nothing. If indexing adds "reimbursement" with weight 0.6 to the refund chunk, the query now matches with score 0.6. A real model learns such expansions from data; here I hand-wrote them.

**Code:** (run; TOY hand-written expansion map simulating the effect; this is NOT SPLADE and has no model)
```python
import re, math
from collections import defaultdict

def toks(t): return re.findall(r"[a-z0-9]+", t.lower())

# TOY: a hand-written expansion map stands in for a learned model. Real SPLADE-style models
# produce weights over the whole vocabulary from a transformer; this is NOT SPLADE.
EXPAND = {  # term -> {related term: weight}
 "refund": {"reimbursement": 0.6, "money": 0.4, "return": 0.3},
 "cancel": {"stop": 0.5, "terminate": 0.4, "membership": 0.3},
 "password": {"credentials": 0.5, "login": 0.5},
}
def sparse_vec(text, expand=True):
    v = defaultdict(float)
    for w in toks(text):
        v[w] += 1.0
        if expand:
            for t, wt in EXPAND.get(w, {}).items(): v[t] = max(v[t], wt)   # expansion terms
    return dict(v)

docs = ["Submit a refund request within thirty days",
        "You can cancel your plan in settings",
        "A password reset link is sent by email",
        "Delivery takes five working days"]
queries = [("reimbursement", 0), ("stop membership", 1), ("login credentials", 2)]

def build_index(expand):          # inverted index: term -> [(doc, weight)]
    idx = defaultdict(list)
    for i, d in enumerate(docs):
        for t, w in sparse_vec(d, expand).items(): idx[t].append((i, w))
    return idx
def search(q, idx):               # score = dot product over shared terms
    s = defaultdict(float)
    for t in toks(q):
        for i, w in idx.get(t, []): s[i] += w
    return sorted(s.items(), key=lambda x: -x[1])

for expand in (False, True):
    idx = build_index(expand)
    hits = 0
    for q, rel in queries:
        res = search(q, idx)
        top = res[0][0] if res else None
        hits += top == rel
        print(f"expand={expand!s:5} q={q!r:22} top={top} scores={[(i, round(s,2)) for i, s in res]}")
    print(f"  top-1 correct: {hits}/{len(queries)}")
print("doc 0 expanded vector:", {k: v for k, v in sparse_vec(docs[0]).items() if k in ('refund','reimbursement','money','return')})
```
Output (my run, toy):
```
expand=False q='reimbursement'        top=None scores=[]
expand=False q='stop membership'      top=None scores=[]
expand=False q='login credentials'    top=None scores=[]
  top-1 correct: 0/3
expand=True  q='reimbursement'        top=0 scores=[(0, 0.6)]
expand=True  q='stop membership'      top=1 scores=[(1, 0.8)]
expand=True  q='login credentials'    top=2 scores=[(2, 1.0)]
  top-1 correct: 3/3
doc 0 expanded vector: {'refund': 1.0, 'reimbursement': 0.6, 'money': 0.4, 'return': 0.3}
```

**Follow-ups:**
- *Learned sparse vs dense?* Sparse stays tied to vocabulary terms and uses an inverted index; dense is a compact semantic vector. They fail differently, which is why you can fuse them.
- *Do you need it?* Only if measured vocabulary-mismatch misses remain after BM25 plus dense plus reranking; it adds a model to index and serve.
- *Risk of expansion?* Bad expansion terms add false matches and bloat the index; check per-term effects on your golden set.

**Common mistakes:** claiming SPLADE is "just BM25 with synonyms" (the weights are learned, not a thesaurus); quoting benchmark numbers from memory; forgetting index-time model cost; assuming it solves exact identifiers; calling a hand-made map SPLADE.

### Q17 ⭐⭐ 🟡 Which score-normalisation methods exist for fusion (min-max, z-score, rank-based), and how does each fail?
**Asked at:** product, search teams
**Say this first (1 line):** BM25 and cosine scores live on different scales, so before a weighted sum you normalise (min-max, z-score, percentile) or drop scores and fuse ranks (RRF); each has a failure mode, mostly outliers and the size of the candidate set.

**Then explain:**
- **Min-max:** (s - min) / (max - min) per query. Simple, but one outlier squashes everyone else toward 0, and the result depends on which candidates are in the list (top-5 vs top-50 gives different values for the same document).
- **Z-score:** (s - mean) / std. Handles shift and scale, but assumes the scores are roughly bell-shaped; an outlier inflates the std and distorts it too, and results are unbounded and can be negative.
- **Rank-based (RRF):** sum of 1/(k + rank). Immune to outliers and scale. It throws away score gaps: a huge margin of victory counts the same as a tiny one, and a ranker with no signal still votes (Q15).
- **Percentile or empirical CDF:** map each score to its fraction of the list at or below it. Robust to outliers and keeps order, but it is effectively rank-based (it also discards gaps) and needs enough candidates.
- **Top-k truncation:** normalising over only the top-5 makes the 5th document get 0 by construction, whatever its real score. Normalise over a fixed, reasonably large candidate depth and keep it the same between tuning and serving.
- **Practical rule:** start with RRF, move to normalised weighted fusion only when a labelled set shows it wins (Part 7 Q4).

**Example:** All numbers SYNTHETIC. Ten candidates. In the normal case BM25 and a toy cosine list agree that doc 1 is best. Now doc 0 gets a BM25 score of 40 (an exact-ID hit) while others stay between 1.5 and 8.1. Min-max maps docs 1, 2, 3 to 0.16, 0.14, 0.12, so BM25 stops discriminating among them and doc 0 jumps to first. Z-score has the same problem. The percentile map and RRF keep doc 1 first. But note the trade-off: if that 40 really is a perfect exact match, ranks throw away the evidence that makes it special.

**Code:** (run; synthetic score lists, numpy only)
```python
import numpy as np
rng = np.random.default_rng(0)

# SYNTHETIC score lists for the same 10 candidates (doc ids 0..9).
# BM25-like scores (unbounded) and cosine-like scores (narrow band).
bm25 = np.array([8.1, 7.5, 7.0, 6.2, 5.0, 4.4, 3.9, 3.0, 2.2, 1.5])
cos  = np.array([0.55, 0.71, 0.62, 0.58, 0.80, 0.52, 0.50, 0.49, 0.47, 0.45])
bm25_out = bm25.copy(); bm25_out[0] = 40.0     # one outlier: an exact-ID match scoring huge

def minmax(s): return (s - s.min()) / (s.max() - s.min())
def zscore(s): return (s - s.mean()) / s.std()
def ranks(s):  o = np.argsort(-s); r = np.empty(len(s), int); r[o] = np.arange(1, len(s)+1); return r
def rrf(*lists, k=60): return sum(1 / (k + ranks(s)) for s in lists)
def ecdf(s):   return np.array([(s <= x).mean() for x in s])   # percentile mapping

def show(name, f, a, b):
    comb = 0.5 * f(a) + 0.5 * f(b)
    print(f"{name:8s} top3 of fused: {np.argsort(-comb)[:3].tolist()}  "
          f"normalised BM25 of docs 1,2,3: {np.round(f(a)[1:4], 2).tolist()}")

print("No outlier:")
for n, f in [("minmax", minmax), ("zscore", zscore), ("ecdf", ecdf)]: show(n, f, bm25, cos)
print("RRF      top3 of fused:", np.argsort(-rrf(bm25, cos))[:3].tolist())
print("With ONE BM25 outlier (doc 0 = 40.0):")
for n, f in [("minmax", minmax), ("zscore", zscore), ("ecdf", ecdf)]: show(n, f, bm25_out, cos)
print("RRF      top3 of fused:", np.argsort(-rrf(bm25_out, cos))[:3].tolist())

# Top-k truncation: normalise over only the top-5 BM25 candidates vs all 10
t5 = np.argsort(-bm25)[:5]
print("min-max of doc 4 (BM25=5.0): over 10 candidates =", round(minmax(bm25)[4], 2),
      "| over its own top-5 =", round(minmax(bm25[t5])[list(t5).index(4)], 2))
```
Output (my run, synthetic):
```
No outlier:
minmax   top3 of fused: [1, 4, 2]  normalised BM25 of docs 1,2,3: [0.91, 0.83, 0.71]
zscore   top3 of fused: [1, 4, 2]  normalised BM25 of docs 1,2,3: [1.21, 0.98, 0.61]
ecdf     top3 of fused: [1, 0, 2]  normalised BM25 of docs 1,2,3: [0.9, 0.8, 0.7]
RRF      top3 of fused: [1, 0, 4]
With ONE BM25 outlier (doc 0 = 40.0):
minmax   top3 of fused: [0, 4, 1]  normalised BM25 of docs 1,2,3: [0.16, 0.14, 0.12]
zscore   top3 of fused: [0, 4, 1]  normalised BM25 of docs 1,2,3: [-0.05, -0.1, -0.17]
ecdf     top3 of fused: [1, 0, 2]  normalised BM25 of docs 1,2,3: [0.9, 0.8, 0.7]
RRF      top3 of fused: [1, 0, 4]
min-max of doc 4 (BM25=5.0): over 10 candidates = 0.53 | over its own top-5 = 0.0
```

**Follow-ups:**
- *Can you clip outliers instead?* Yes: winsorise (cap at a percentile) before min-max, or use robust statistics (median and IQR). Tune the cap on labelled data.
- *Fixed bounds instead of per-query min-max?* For a bounded score like cosine you can use known bounds; BM25 has none, so people estimate them from a sample of queries.
- *Which is best?* No universal winner; compare on your golden set (Q14).

**Common mistakes:** min-maxing a list of 3 candidates; normalising on different depths in tuning and production; ignoring that one exact-match outlier can dominate; assuming z-score works on skewed score distributions; thinking RRF is always better (it discards margin information).

### Q18 ⭐⭐ 🟡 How do you choose the candidate counts in retrieve-then-rerank (n from the first stage, k after reranking)? What is the recall ceiling?
**Asked at:** product, GenAI startups, GCC
**Say this first (1 line):** The reranker can only reorder what stage 1 returned, so recall@n of the first stage is a hard ceiling; pick n from the recall@n-versus-n curve on your golden set and the per-candidate rerank latency, at the knee where extra candidates stop paying.

**Then explain:**
- **Ceiling:** if the right chunk is not in the top n, no reranker can surface it. Final recall@k is at most recall@n.
- **Choose n with data:** measure recall@n for several n on the golden set (Part 6 Q40), plot it, and note the marginal gain per extra candidate. Gains shrink fast (diminishing returns).
- **Choose k separately:** k is how many chunks go to the generator. It is limited by the context budget and by noise: more chunks cost tokens and can distract the model (Part 6 Q49).
- **Latency budget per stage:** reranker cost grows about linearly with n (setup + per-candidate time, reduced by batching, Q21). Split the end-to-end budget between first stage, reranker and generation, then take the largest n that fits, or the knee below it.
- **Reported example, not a rule:** the Contextual Retrieval post reports reranking the top 150 candidates down to 20 as its setting. Your best n depends on your corpus, chunk length and reranker.
- **Also check:** if recall@n is already high at small n, spend the budget on a better first stage or a stronger reranker instead of a bigger n.

**Example:** All numbers SYNTHETIC with an ASSUMED latency model (40 ms first stage, 15 ms reranker setup, 0.9 ms per candidate). Recall@n goes 0.805 (n=10), 0.908 (20), 0.952 (30), 0.979 (50), 0.995 (100). Going from 50 to 100 candidates adds 1.6 points of recall but 45 ms. With a 120 ms budget the largest n that fits is 50; the knee at 95% of that recall is n=30 at 82 ms. If the reranker then puts the relevant chunk in the top 5 in 80% of the cases where it is present (assumed), final recall@5 is about 0.76 at n=30.

**Code:** (run; synthetic first-stage ranks, assumed latency model, numpy only)
```python
import numpy as np
rng = np.random.default_rng(0)

# SYNTHETIC golden set: for each of 1000 queries, the rank at which stage 1 returns the
# relevant chunk (heavy-tailed: mostly near the top, sometimes very deep).
rank = np.ceil(rng.lognormal(mean=1.2, sigma=1.4, size=1000)).astype(int)

ns = [5, 10, 20, 30, 50, 75, 100, 150, 200, 300]
recall = {n: float((rank <= n).mean()) for n in ns}

# ASSUMED latency model (not measured): stage 1 = 40 ms fixed; reranker = 15 ms setup + 0.9 ms per candidate
def latency(n): return 40 + 15 + 0.9 * n
BUDGET_MS = 120   # assumed end-to-end retrieval budget

print(" n   recall@n  marginal gain  latency_ms(assumed)")
prev = 0.0
for n in ns:
    print(f"{n:3d}   {recall[n]:.3f}     {recall[n]-prev:+.3f}        {latency(n):6.1f}")
    prev = recall[n]

fits = [n for n in ns if latency(n) <= BUDGET_MS]
best_fit = max(fits)
knee = min(n for n in ns if recall[n] >= 0.95 * recall[best_fit])
print(f"largest n within {BUDGET_MS} ms budget: {best_fit} (recall@n = {recall[best_fit]:.3f})")
print(f"smallest n reaching 95% of that recall: {knee} (recall@n = {recall[knee]:.3f}, {latency(knee):.1f} ms)")

# The ceiling: even a good reranker can only return what stage 1 gave it.
p_top5_given_in = 0.8   # ASSUMED: reranker puts the relevant chunk in top 5 80% of the time when present
for n in (20, knee, best_fit):
    print(f"n={n:3d}: final recall@5 ~ recall@n * {p_top5_given_in} = {recall[n]*p_top5_given_in:.3f}")
```
Output (my run, synthetic and assumed):
```
 n   recall@n  marginal gain  latency_ms(assumed)
  5   0.634     +0.634          59.5
 10   0.805     +0.171          64.0
 20   0.908     +0.103          73.0
 30   0.952     +0.044          82.0
 50   0.979     +0.027         100.0
 75   0.989     +0.010         122.5
100   0.995     +0.006         145.0
150   0.998     +0.003         190.0
200   0.999     +0.001         235.0
300   1.000     +0.001         325.0
largest n within 120 ms budget: 50 (recall@n = 0.979)
smallest n reaching 95% of that recall: 30 (recall@n = 0.952, 82.0 ms)
n= 20: final recall@5 ~ recall@n * 0.8 = 0.726
n= 30: final recall@5 ~ recall@n * 0.8 = 0.762
n= 50: final recall@5 ~ recall@n * 0.8 = 0.783
```

**Follow-ups:**
- *Recall@n is 0.7 and will not rise?* Fix stage 1: hybrid, query rewriting, better chunking (Part 7 Q2, Q7), not a bigger n.
- *Fixed n or adaptive?* Some systems cut candidates by a score threshold or run a cheap reranker first (cascade, Q21); measure whether it keeps recall.
- *Is it per query type?* Yes, tail queries may need deeper n; look at the curve per slice.

**Common mistakes:** picking n = 100 by habit; tuning k and n together without isolating them; forgetting that final quality is bounded by recall@n; ignoring the p95 of the reranker; reading the vendor's 150 to 20 as a universal recipe.

### Q19 ⭐⭐ 🟡 LLM-based rerankers (pointwise, pairwise, listwise) vs cross-encoder rerankers for RAG: quality, cost, position bias and when to use each.
**Asked at:** product, GenAI startups, big tech
**Say this first (1 line):** A cross-encoder is the cheap, fast, stable default; an LLM reranker (pointwise, pairwise or listwise) can follow complex instructions and reason over candidates, but costs more tokens and latency and is noisy and sensitive to the order of candidates in the prompt.

**Then explain:**
- **Pointwise:** the LLM scores each (query, doc) alone, for example a 0-10 grade or the probability of "yes". n calls (parallelisable), stable per call, but scores are poorly calibrated across calls.
- **Pairwise:** the LLM picks the better of two documents. Comparisons are easier for the model, but a full sort needs many pairs (up to about n log n with a smart sort, n squared for all pairs), so it is expensive.
- **Listwise:** put the whole candidate list in one prompt, ask for a ranking. One call, sees candidates against each other, but long prompts, context limits, so sliding windows are used for long lists. Outputs can be malformed or drop items; check and repair.
- **Position bias and variance:** models often favour documents placed early (or sometimes late) in the prompt, and the same input can give different rankings across runs. Mitigations: shuffle the order across several passes and aggregate ranks, fix temperature to 0, validate output format. Each mitigation multiplies cost.
- **Versus a cross-encoder:** a cross-encoder scores pairs in one fast forward pass, is deterministic, and can be fine-tuned cheaply on your data (Q20). The LLM adds instruction-following (for example "prefer the newest policy"), but you pay in tokens and p95 latency. Measure the gain on your golden set against that cost (Q14); the recommender view is in B1P07-Q43, not repeated here.
- **When to use which:** cross-encoder by default. LLM listwise for a small final shortlist (say 10-20 chunks) when rules are subtle, quality matters more than latency, or you lack training data. Pointwise LLM when you need an explainable relevance grade. Pairwise rarely, for small tie-breaking sets.

**Example:** Everything MOCK (no real LLM). Ten candidates with known grades. The mock reranker scores each by true relevance plus noise plus a bonus for appearing early in the prompt. When the single best candidate sits in slot 0 it is ranked first 99% of the time, in slot 9 only 88%. In a harder test where the first stage puts the best documents last, one pass gives mean NDCG@3 of 0.902; eight shuffled passes aggregated give 0.999. But eight passes in the same order also give 0.993, so in this mock most of the gain is just averaging the noise, and shuffling adds the rest. The price is 8x the calls. These numbers are properties of my mock, not of any real model.

**Code:** (run; MOCK listwise reranker with built-in noise and position bias; numpy only)
```python
import numpy as np
rng = np.random.default_rng(0)

# MOCK listwise LLM reranker (no real model). It sees candidates in a given order and returns a
# ranking by a "perceived score" = true relevance + noise + a bonus for appearing early in the prompt.
def mock_listwise(true_rel, order, rng, noise=0.6, bias=0.8):
    m = len(order)
    pos_bonus = bias * (1 - np.arange(m) / (m - 1))            # first slot gets +bias, last gets 0
    perceived = true_rel[order] + rng.normal(0, noise, m) + pos_bonus
    return order[np.argsort(-perceived)]                        # candidate ids, best first

def dcg(rels): return sum((2**r - 1) / np.log2(i + 2) for i, r in enumerate(rels))
def ndcg_at(true_rel, ranking, k=3):
    ideal = np.sort(true_rel)[::-1]
    return dcg(true_rel[ranking][:k]) / dcg(ideal[:k])

M = 10
# 1) Position bias: the single best candidate (grade 3) placed at each input position.
print("P(best candidate ranked first) by its input position (mock):")
for pos in (0, 4, 9):
    wins = 0
    for _ in range(2000):
        rel = np.zeros(M); rel[:] = rng.integers(0, 2, M); best = 0; rel[best] = 3
        order = np.arange(M); order[[0, pos]] = order[[pos, 0]]      # move candidate 0 to slot 'pos'
        wins += mock_listwise(rel, order, rng)[0] == best
    print(f"  slot {pos}: {wins/2000:.2f}")

# 2) Mitigation: shuffle and aggregate. Mean rank over R random permutations.
def shuffle_aggregate(true_rel, rng, R=8, fixed_order=None):
    ranks = np.zeros(M)
    for _ in range(R):
        order = rng.permutation(M) if fixed_order is None else fixed_order
        out = mock_listwise(true_rel, order, rng)
        for r, c in enumerate(out): ranks[c] += r
    return np.argsort(ranks / R)

single, agg, same = [], [], []
for _ in range(1000):
    rel = rng.integers(0, 4, M).astype(float)
    # first stage puts the most relevant docs LAST (adversarial but plausible for a weak first stage)
    order0 = np.argsort(rel, kind="stable")
    single.append(ndcg_at(rel, mock_listwise(rel, order0, rng)))
    agg.append(ndcg_at(rel, shuffle_aggregate(rel, rng)))
    same.append(ndcg_at(rel, shuffle_aggregate(rel, rng, fixed_order=order0)))
print(f"mean NDCG@3, single pass in first-stage order: {np.mean(single):.3f}")
print(f"mean NDCG@3, shuffle+aggregate (8 passes):      {np.mean(agg):.3f}   (8x the LLM calls)")
print(f"mean NDCG@3, 8 passes in the SAME order (noise averaging only): {np.mean(same):.3f}")
```
Output (my run, mock):
```
P(best candidate ranked first) by its input position (mock):
  slot 0: 0.99
  slot 4: 0.96
  slot 9: 0.88
mean NDCG@3, single pass in first-stage order: 0.902
mean NDCG@3, shuffle+aggregate (8 passes):      0.999   (8x the LLM calls)
mean NDCG@3, 8 passes in the SAME order (noise averaging only): 0.993
```

**Follow-ups:**
- *Why a sliding window for listwise?* The list may not fit in context, and quality drops with long prompts. Rank windows from the bottom up so strong documents bubble to the top; stitch carefully because windows overlap.
- *Can you distil an LLM reranker?* Yes, train a cross-encoder on LLM judgments to get most of the signal at cross-encoder cost (Q20).
- *Cost?* Count prompt tokens (query plus all candidates) times calls times your model's rate; do not quote a price without checking the current pricing page.

**Common mistakes:** using an LLM reranker on 100+ candidates; trusting one pass; ignoring output-format failures; not randomising candidate order in evaluation; comparing an LLM reranker to a cross-encoder on quality alone without latency and cost; claiming position bias direction is fixed (it depends on the model and prompt, so test it).

### Q20 ⭐⭐ 🟡 How do you train or fine-tune a reranker (hard negatives from the first stage, distillation from an LLM, evaluation)?
**Asked at:** product, GenAI startups, research-leaning teams
**Say this first (1 line):** Build training groups of (query, positive, hard negatives mined from your own first stage), train a cross-encoder with a pointwise, pairwise or listwise loss, optionally using LLM judgments as labels, and evaluate on a held-out and a shifted slice with NDCG and recall, not training loss.

**Then explain:**
- **Data:** each example is a query, one or more relevant chunks, and negatives. Hard negatives come from the first stage (top-ranked but not relevant), because those are the mistakes the reranker will actually face. Random negatives are too easy.
- **False-negative risk:** a mined "negative" may really be relevant (duplicates, near-duplicates, an unlabelled second answer). Training on it teaches the model to demote good chunks. Mitigations: skip the very top-ranked negatives, filter with an LLM or human check on a sample, dedupe the corpus.
- **Losses:** pointwise BCE (each pair is relevant or not; simple, ignores ordering across candidates); pairwise (push the positive score above a negative; matches ranking, many pairs); listwise softmax (cross-entropy over a group: one positive against all negatives, closest to what you do at inference). Pick by validation NDCG; the differences are often small.
- **Distillation from an LLM:** have a strong LLM grade (query, chunk) pairs, then train the small cross-encoder on those grades. You get LLM-like judgment at cross-encoder cost, but you inherit the LLM's biases and labelling cost (Q19). Spot-check labels against humans.
- **Evaluation:** hold out queries (and ideally split by document or time, so no leakage), report NDCG@k and the end-to-end retrieval metrics, plus a slice from a different domain to see how it degrades. Compare to the off-the-shelf reranker as the baseline: fine-tuning must beat it (Q14). Related: embedding fine-tuning in Part 6 Q52, alignment-style preference data in Part 5 Q5.

**Example:** All SYNTHETIC. Each query has 20 candidates with 8 features, and relevance comes from a hidden linear rule plus noise. Random scores give NDCG@5 of 0.275 on held-out queries. A linear reranker trained with the pairwise loss reaches 0.952, and with the listwise softmax loss 0.954. On a second domain where relevance depends on other features, it drops to about 0.55 (random is 0.28). So held-out gains do not guarantee domain robustness, which is why you test a shifted slice.

**Code:** (run; torch CPU, single thread; synthetic features, not real text)
```python
import torch
torch.set_num_threads(1); torch.manual_seed(0)

D, C = 8, 20                                   # features per (query, doc) pair, candidates per query
w_true = torch.tensor([2.0, -1.0, 1.5, 0.0, 0.0, 0.5, 0.0, -0.5])   # hidden "true relevance" direction
w_shift = torch.tensor([0.5, -1.0, 1.0, 1.5, 1.5, 0.5, 0.0, -0.5])  # a DIFFERENT domain: relevance depends on other features

def make(nq, w=w_true):
    X = torch.randn(nq, C, D)                                                       # SYNTHETIC features
    s = X @ w + 0.8 * torch.randn(nq, C)                                            # noisy relevance signal
    rel = torch.zeros(nq, C)
    for t in (0.7, 1.7, 2.7): rel += (s > t).float() * 1.0                          # grades 0..3
    return X, rel

def ndcg(scores, rel, k=5):
    gain = 2 ** rel - 1
    disc = 1 / torch.log2(torch.arange(2, k + 2).float())
    top = scores.topk(k, dim=1).indices
    dcg = (torch.gather(gain, 1, top) * disc).sum(1)
    ideal = (gain.sort(dim=1, descending=True).values[:, :k] * disc).sum(1)
    ok = ideal > 0
    return (dcg[ok] / ideal[ok]).mean().item()

Xtr, Rtr = make(400); Xte, Rte = make(200); Xsh, Rsh = make(200, w_shift)   # held-out + shifted domain

def pairwise_loss(sc, rel):                     # logistic loss on all pairs where rel_i > rel_j
    diff = sc.unsqueeze(2) - sc.unsqueeze(1)                       # [q, i, j]
    mask = (rel.unsqueeze(2) > rel.unsqueeze(1)).float()
    return (torch.nn.functional.softplus(-diff) * mask).sum() / mask.sum().clamp(min=1)

def listwise_softmax_loss(sc, rel):             # cross-entropy between softmax(scores) and normalised gains
    p = torch.softmax(sc, 1); t = (2 ** rel - 1); t = t / t.sum(1, keepdim=True).clamp(min=1e-9)
    return -(t * torch.log(p + 1e-9)).sum(1).mean()

def train(loss_fn, steps=300):
    torch.manual_seed(1)
    w = torch.zeros(D, requires_grad=True); opt = torch.optim.Adam([w], lr=0.05)
    for _ in range(steps):
        opt.zero_grad(); loss_fn(Xtr @ w, Rtr).backward(); opt.step()
    return w.detach()

rand = lambda X: torch.randn(X.shape[0], C)
print(f"before training (random scores): NDCG@5 held-out = {ndcg(rand(Xte), Rte):.3f} | shifted domain = {ndcg(rand(Xsh), Rsh):.3f}")
for name, fn in [("pairwise", pairwise_loss), ("listwise softmax", listwise_softmax_loss)]:
    w = train(fn)
    print(f"{name:17s} NDCG@5 held-out = {ndcg(Xte @ w, Rte):.3f} | shifted domain = {ndcg(Xsh @ w, Rsh):.3f}")
print("learned w (listwise):", [round(x, 2) for x in w.tolist()])
```
Output (my run, synthetic):
```
before training (random scores): NDCG@5 held-out = 0.275 | shifted domain = 0.280
pairwise          NDCG@5 held-out = 0.952 | shifted domain = 0.546
listwise softmax  NDCG@5 held-out = 0.954 | shifted domain = 0.552
learned w (listwise): [1.03, -0.54, 0.79, -0.01, -0.01, 0.25, -0.01, -0.25]
```
The learned weights point in the same direction as the hidden rule (their scale differs, which does not matter for ranking). A real cross-encoder is a transformer over the concatenated query and chunk; this linear stand-in only shows the losses and the evaluation protocol.

**Follow-ups:**
- *How many examples?* Depends on domain and base model; start from a pretrained reranker and judge by the learning curve on your held-out set, not a fixed number.
- *Where do queries come from?* Real logs (best), or LLM-generated synthetic questions per chunk (check them for leakage and for being too easy).
- *Fine-tune the embedder or the reranker first?* Measure where the failures are: recall@n low means first stage (Q18); good recall but poor ordering means the reranker.

**Common mistakes:** random negatives only; trusting mined negatives blindly; evaluating on training queries or near-duplicate chunks; looking at loss instead of NDCG; skipping the off-the-shelf baseline; training on LLM labels without checking them against humans.

### Q21 ⭐⭐ 🟡 How do you serve a reranker at production latency (batching, truncation, caching, early exit, hardware)?
**Asked at:** product, platform teams, GCC
**Say this first (1 line):** Score all candidates in one or a few batches, truncate chunks to a sensible max length, cache repeated pairs, use a cheap-then-expensive cascade, and measure p95 latency on your hardware, because the reranker cost scales with candidates times tokens.

**Then explain:**
- **Batching:** do not score pairs one by one. A batch uses the device much better: the same forward pass overhead is shared. Batch all n candidates if memory allows, sort by length or pad carefully to avoid wasting compute on padding. Dynamic batching across users helps throughput but can add queueing delay.
- **Truncation:** cost grows with sequence length (roughly linearly for short inputs, faster for long). Cap the max length, but check that the truncated part is not where the answer lives. Fix chunk sizes upstream if chunks are routinely too long (Part 6).
- **Caching:** cache (query, chunk) scores only where queries repeat (FAQ-style traffic, popular searches). For unique long-tail queries the hit rate is low and a cache adds cost without benefit; measure the hit rate first.
- **Cascade or early exit:** a cheap model (or the first-stage score) trims 150 candidates to 30 and the expensive reranker scores only those. Early-exit variants stop when confident. Both risk dropping a relevant chunk: re-measure recall (Q18).
- **Quantisation and hardware:** lower-precision weights and a GPU (or optimised CPU runtime) cut per-pair time; accuracy impact must be tested. Details on quantisation and serving stacks: Part 10.
- **Budget it:** the reranker gets a slice of the end-to-end latency budget. Watch p95, cold starts, and what happens when the reranker times out (fall back to first-stage order).

**Example:** All numbers ASSUMED (synthetic latency model: 12 ms fixed per batch plus 0.4 ms per pair at length 256, flat up to 16 pairs because the device is under-used). For 50 candidates, one at a time takes 920 ms; batches of 16 take 73.6 ms; a single batch of 50 takes 32 ms. At batch 50, halving the length from 256 to 128 cuts 32 ms to 22 ms. A 30% cache hit rate cuts it to 26 ms. A cascade that scores 150 candidates cheaply (assumed 0.05 ms each) and then 30 expensively costs 31.5 ms, against 96 ms for the expensive model on all 150. Your real numbers will differ; the shape of the argument is the point.

**Code:** (run; pure-Python latency model with ASSUMED constants, not a benchmark of any model or hardware)
```python
import math

# ASSUMED latency model (synthetic, not measured on any hardware):
#   one forward pass over a batch of B (query, chunk) pairs of length L tokens takes
#   t(B, L) = 12 ms fixed + 0.4 ms * max(B, 16) * (L / 256)
#   i.e. small batches under-use the device (time is flat up to B=16), big batches are linear.
def t_batch(B, L): return 12 + 0.4 * max(B, 16) * (L / 256)

def query_latency(n, B, L):                 # serial batches for one query's n candidates
    return math.ceil(n / B) * t_batch(min(B, n), L)

n = 50
print("A) batch size, n=50 candidates, L=256 (ASSUMED model)")
print("   B   query_latency_ms  pairs/s")
for B in (1, 4, 16, 32, 50):
    lat = query_latency(n, B, 256)
    print(f"  {B:3d}   {lat:8.1f}        {n / lat * 1000:7.0f}")

print("B) truncation, B=50 (ASSUMED): latency scales with L")
for L in (512, 256, 128):
    print(f"   L={L}: {query_latency(n, 50, L):.1f} ms")

print("C) cache of repeated (query, chunk) pairs, B=50, L=256 (ASSUMED hit rates)")
for hit in (0.0, 0.3, 0.6):
    m = round(n * (1 - hit)); lat = query_latency(m, 50, 256) if m else 0
    print(f"   hit rate {hit:.0%}: scores {m} pairs -> {lat:.1f} ms")

print("D) cascade (ASSUMED): cheap model 0.05 ms/pair on 150, expensive on top 30 only")
cheap = 150 * 0.05; exp = query_latency(30, 30, 256)
print(f"   cascade: {cheap:.1f} + {exp:.1f} = {cheap + exp:.1f} ms  vs expensive on all 150: {query_latency(150, 50, 256):.1f} ms")
print("   (the cascade drops any relevant chunk the cheap model ranks outside its top 30: measure recall)")
```
Output (my run, assumed model):
```
A) batch size, n=50 candidates, L=256 (ASSUMED model)
   B   query_latency_ms  pairs/s
    1      920.0             54
    4      239.2            209
   16       73.6            679
   32       49.6           1008
   50       32.0           1562
B) truncation, B=50 (ASSUMED): latency scales with L
   L=512: 52.0 ms
   L=256: 32.0 ms
   L=128: 22.0 ms
C) cache of repeated (query, chunk) pairs, B=50, L=256 (ASSUMED hit rates)
   hit rate 0%: scores 50 pairs -> 32.0 ms
   hit rate 30%: scores 35 pairs -> 26.0 ms
   hit rate 60%: scores 20 pairs -> 20.0 ms
D) cascade (ASSUMED): cheap model 0.05 ms/pair on 150, expensive on top 30 only
   cascade: 7.5 + 24.0 = 31.5 ms  vs expensive on all 150: 96.0 ms
   (the cascade drops any relevant chunk the cheap model ranks outside its top 30: measure recall)
```

**Follow-ups:**
- *Reranker times out?* Return the first-stage order and log it; never fail the request. Set a timeout near your p95 budget.
- *CPU only?* Use a smaller reranker, fewer candidates, shorter chunks and an optimised runtime; accept a smaller n and re-measure the recall ceiling.
- *Where are the real numbers?* Benchmark your own model, sequence lengths and hardware under realistic concurrency; load tests matter more than single-request timings.

**Common mistakes:** one request per pair; measuring only average latency; caching without checking hit rate; truncating away the answer; cascade without a recall check; benchmarking on idle hardware with short toy inputs.

### Q22 ⭐⭐ 🟡 What is step-back prompting for retrieval, and how does it differ from HyDE and decomposition?
**Asked at:** product, GenAI startups
**Say this first (1 line):** Step-back means asking the LLM to turn a very specific question into a more general one ("what are the upload limits per plan?"), retrieving background for that too, and answering with both; it moves up in abstraction, where HyDE writes a fake answer and decomposition splits into sub-questions.

**Then explain:**
- **Idea:** specific questions contain details (IDs, dates, names) that match specific passages, but the answer often needs a principle or policy that is written in general terms and shares few words with the question. A step-back query reaches that background.
- **Versus HyDE (Part 7 Q8):** HyDE generates a hypothetical answer document and embeds that, aiming at answer-shaped text. Step-back generates a more abstract question, aiming at background and principles.
- **Versus decomposition (Q10):** decomposition splits one question into several sub-questions that each need their own evidence (multi-hop). Step-back produces one broader question and keeps the original.
- **Evidence level:** the idea comes from the prompting literature and is described in practitioner blogs, which I only saw as search snippets. I did not open a paper, so I would not quote gains; test it on your golden set.
- **Practical use:** run the original and the step-back query, fuse (RRF, Part 7 Q3), and keep the original as a fallback. Cost: one extra LLM call plus one extra retrieval, so use it when a router sees a "specific question that needs a rule" shape (Q23), not on every query.
- **Failure modes:** a too-abstract query pulls generic text that crowds out the specific chunk; the rewriter can drift to a different topic; it adds latency.

**Example:** MOCK, toy keyword retrieval. User asks "Why did my 2 GB video upload return 413 on the Basic plan?" The chunk that explains plan-wise size limits never says "413" or "video". A mocked step-back "What are the upload size limits for each plan?" puts the limits chunk at rank 1. Over three toy questions, background recall@1 is 0/3 for the original, 3/3 for step-back alone (by construction of my hand-written mock), and 2/3 when fusing both, with recall@2 reaching 3/3 for the fused list. The fused list kept the specific chunk too, which a step-back-only strategy would lose.

**Code:** (run; BM25 from scratch on a tiny toy corpus; the step-back "LLM" is a hand-written lookup, i.e. MOCK)
```python
import re, math
from collections import Counter

STOP = set("a an the of to in on is are was for and or my why did how what does do with by at it this that".split())
def toks(t): return [w for w in re.findall(r"[a-z0-9]+", t.lower()) if w not in STOP]

docs = {
 "bg_limits":  "Upload size limits depend on the plan. Free plans allow small files, paid plans allow larger files.",
 "ex_413":     "Error 413 payload too large was returned to a customer uploading a video.",
 "bg_refunds": "Refund policy: purchases can be returned within thirty days if unused.",
 "ex_refund_ph": "Order 5521 for the Zephyr phone was delivered on 3 May.",
 "bg_security":"Account security principles: use strong passwords and enable two factor authentication.",
 "ex_lock":    "User ravi99 was locked out after five failed attempts on Tuesday.",
 "noise1":     "Delivery usually takes three to five working days across the country.",
 "noise2":     "The mobile app supports dark mode and offline reading.",
}
names = list(docs)
D = {n: toks(t) for n, t in docs.items()}; N = len(D); avg = sum(map(len, D.values())) / N
df = Counter(w for d in D.values() for w in set(d))
def bm25(q, k1=1.5, b=0.75):
    sc = {}
    for n, d in D.items():
        s = 0.0
        for w in toks(q):
            if w in df:
                tf = d.count(w); idf = math.log(1 + (N - df[w] + .5) / (df[w] + .5))
                s += idf * tf * (k1 + 1) / (tf + k1 * (1 - b + b * len(d) / avg))
        sc[n] = s
    return [n for n in sorted(names, key=lambda n: -sc[n]) if sc[n] > 0]   # drop zero-score (no-signal) docs

# MOCK step-back "LLM": a hand-written lookup from specific question to a more general one.
MOCK_STEP_BACK = {
 "Why did my 2 GB video upload return 413 on the Basic plan": "What are the upload size limits for each plan",
 "Can I return the Zephyr phone from order 5521 delivered on 3 May": "What is the refund policy for returns",
 "Why was ravi99 locked out on Tuesday": "What are the account security principles",
}
queries = [(q, bg) for q, bg in zip(MOCK_STEP_BACK, ["bg_limits", "bg_refunds", "bg_security"])]

def rrf(lists, k=60):
    s = Counter()
    for l in lists:
        for r, n in enumerate(l): s[n] += 1 / (k + r + 1)
    return [n for n, _ in s.most_common()]

def recall_at(rank, bg, k): return bg in rank[:k]
for k in (1, 2):
    o = sb = both = 0
    for q, bg in queries:
        ro = bm25(q); rs = bm25(MOCK_STEP_BACK[q])
        o += recall_at(ro, bg, k); sb += recall_at(rs, bg, k); both += recall_at(rrf([ro, rs]), bg, k)
    print(f"background doc recall@{k}: original={o}/3  step-back only={sb}/3  original+step-back (RRF)={both}/3")
for q, bg in queries:
    print(f"- {q!r}\n    step-back (mock): {MOCK_STEP_BACK[q]!r}\n    original top2: {bm25(q)[:2]}  step-back top2: {bm25(MOCK_STEP_BACK[q])[:2]}  fused top2: {rrf([bm25(q), bm25(MOCK_STEP_BACK[q])])[:2]}")
```
Output (my run, toy and mock):
```
background doc recall@1: original=0/3  step-back only=3/3  original+step-back (RRF)=2/3
background doc recall@2: original=2/3  step-back only=3/3  original+step-back (RRF)=3/3
- 'Why did my 2 GB video upload return 413 on the Basic plan'
    step-back (mock): 'What are the upload size limits for each plan'
    original top2: ['ex_413', 'bg_limits']  step-back top2: ['bg_limits']  fused top2: ['bg_limits', 'ex_413']
- 'Can I return the Zephyr phone from order 5521 delivered on 3 May'
    step-back (mock): 'What is the refund policy for returns'
    original top2: ['ex_refund_ph', 'bg_refunds']  step-back top2: ['bg_refunds']  fused top2: ['bg_refunds', 'ex_refund_ph']
- 'Why was ravi99 locked out on Tuesday'
    step-back (mock): 'What are the account security principles'
    original top2: ['ex_lock']  step-back top2: ['bg_security']  fused top2: ['ex_lock', 'bg_security']
```

**Follow-ups:**
- *When does it hurt?* On simple lookups where the specific chunk is the answer: the abstract query adds noise and cost. Gate it with a router (Q23).
- *Difference from multi-query (Part 7 Q9)?* Multi-query makes paraphrases at the same level; step-back changes the abstraction level.
- *How do you evaluate it?* Ablation on the golden set (Q14): recall@k and answer quality with and without, split by query type, plus the added latency.

**Common mistakes:** replacing the original query with the step-back one; using it on every query; quoting blog-level gains as facts; confusing it with HyDE; letting the LLM rewrite drift off-topic without a check.

### Q23 ⭐⭐ 🟡 How do you route queries to different retrieval strategies (FAQ lookup, multi-hop, global summary), and how do you evaluate the router?
**Asked at:** product, GenAI startups, platform teams
**Say this first (1 line):** A router looks at the query and picks a pipeline (cheap lookup, multi-step, or whole-corpus summary), with a confidence threshold and a safe default, and you evaluate it both as a classifier (accuracy, confusion matrix) and end to end (answer quality, latency, cost).

**Then explain:**
- **Why:** expensive techniques (decomposition, agent loops, GraphRAG-style global search) are wasted on a "what is the refund window?" question, and a plain lookup fails on "summarise the main themes". Routing spends compute only where needed (see also Part 7 Q7, and the agent-loop trade-off in Q13).
- **Router types:** (1) rules (regex, keywords, query length): fast and transparent, brittle; (2) a trained classifier on labelled queries: cheap at serve time, needs labels; (3) an LLM that picks a route: flexible with no training data, but adds latency and cost and can be inconsistent; (4) embedding similarity to route prototypes (average of example queries per route): no training, easy to extend, quality depends on the embedder and the examples.
- **Routes:** for example FAQ/lookup (hybrid + rerank), multi-hop (decomposition, Q10), global summary (hierarchical or graph-based retrieval, Part 7 Q12, Q27).
- **Threshold and fallback:** if the best route similarity is below a threshold, or the router is unsure, use a default (typically the robust hybrid-plus-rerank path), not a random route. Log fallbacks to find new route types.
- **Evaluate:** label a few hundred real queries by route; report per-route precision and recall and the confusion matrix, focusing on costly mistakes (for example global queries sent to a plain lookup). Then run end-to-end ablations: router vs always-default vs always-expensive on answer quality, p95 latency and cost (Q14).

**Example:** TOY, all synthetic. A prototype router with a toy hashed embedding (no semantics) on 96 held-out-phrased queries: 5 FAQ, 4 multi-hop, 4 global templates and 3 off-topic ones ("tell me a joke"), 6 copies each. With no threshold it sends everything to some route (accuracy 0.72; off-topic queries get forced into routes). At threshold 0.35, off-topic all go to the fallback and accuracy is 0.82, but 10 of 30 FAQ queries also fell back (a cost, not an error: they still get an answer from the default path). At 0.6 almost everything falls back (accuracy 0.42). So the threshold is a tuned knob trading precision of routes against how much goes to the default.

**Code:** (run; numpy only; TOY embedder and synthetic queries; accuracy counts "other" as correct only when sent to fallback)
```python
import re, zlib
import numpy as np

def toks(t): return re.findall(r"[a-z0-9]+", t.lower())
H, DIM = 128, 32
P = np.random.default_rng(0).normal(size=(H, DIM))
def emb(text):      # TOY embedding: hashed bag-of-words + random projection (no semantics)
    v = np.zeros(H)
    for w in toks(text): v[zlib.crc32(w.encode()) % H] += 1
    e = v @ P; n = np.linalg.norm(e); return e / n if n else e

ROUTES = ["faq", "multihop", "global"]
# route prototypes: a few example utterances each (written by hand), averaged into one vector
PROTO_TEXT = {
 "faq":      ["what is the refund window", "how do I reset my password", "what is the support phone number"],
 "multihop": ["who founded the company that acquired the startup", "which supplier of the part used in the product had a recall",
              "compare the policy before and after the merger for the manager of the team"],
 "global":   ["summarise the main themes across all documents", "what are the overall trends in the whole collection",
              "give an overview of the key topics in the corpus"],
}
PROTO = {r: np.mean([emb(t) for t in ts], 0) for r, ts in PROTO_TEXT.items()}
PROTO = {r: v / np.linalg.norm(v) for r, v in PROTO.items()}

# SYNTHETIC labelled queries: templates + random fillers
rng = np.random.default_rng(1)
fill = ["billing", "shipping", "warranty", "login", "invoice", "contract", "security", "pricing"]
templates = {   # held-out phrasing: different wording from the prototypes, partial overlap only
 "faq":      ["how long do I have to ask for a refund on {}", "where can I reset the {} password", "what number do I call for {} help",
               "can I change my {} email address", "what is the {} fee"],
 "multihop": ["who runs the firm that bought the {} startup and what did they say about it",
              "which supplier of the {} part also had a recall and who owns it",
              "compare the {} policy before and after the merger for the head of the team",
              "what did the person who wrote the {} report say about the company that audited it"],
 "global":   ["give me the big picture of what the {} documents say overall", "what are the recurring themes about {} throughout the corpus",
              "summarise everything in the collection about {}", "overall what trends appear in the {} files"],
 "other":    ["hello there how are you", "tell me a joke about {}", "thanks that is all"],   # should fall back
}
data = [(t.format(rng.choice(fill)), r) for r, ts in templates.items() for t in ts for _ in range(6)]

def route(q, thr):
    sims = {r: float(PROTO[r] @ emb(q)) for r in ROUTES}
    best = max(sims, key=sims.get)
    return best if sims[best] >= thr else "fallback"   # fallback = default hybrid + rerank path

TRUE = ROUTES + ["other"]; PRED = ROUTES + ["fallback"]
for thr in (0.0, 0.35, 0.6):
    M = np.zeros((4, 4), int)
    for q, y in data: M[TRUE.index(y), PRED.index(route(q, thr))] += 1
    # correct = right route for real routes; "other" is correct only when sent to fallback
    ok = np.trace(M[:3, :3]) + M[3, 3]
    print(f"threshold={thr}: accuracy={ok / M.sum():.2f}  fallback rate={M[:, 3].sum() / M.sum():.2f}")
    print("  confusion (rows=true, cols=" + ",".join(PRED) + ")")
    for r, row in zip(TRUE, M): print(f"  {r:9s}", row.tolist())
```
Output (my run, toy and synthetic):
```
threshold=0.0: accuracy=0.72  fallback rate=0.00
  confusion (rows=true, cols=faq,multihop,global,fallback)
  faq       [21, 5, 4, 0]
  multihop  [0, 24, 0, 0]
  global    [0, 0, 24, 0]
  other     [10, 2, 6, 0]
threshold=0.35: accuracy=0.82  fallback rate=0.29
  confusion (rows=true, cols=faq,multihop,global,fallback)
  faq       [13, 3, 4, 10]
  multihop  [0, 24, 0, 0]
  global    [0, 0, 24, 0]
  other     [0, 0, 0, 18]
threshold=0.6: accuracy=0.42  fallback rate=0.77
  confusion (rows=true, cols=faq,multihop,global,fallback)
  faq       [0, 0, 0, 30]
  multihop  [0, 18, 0, 6]
  global    [0, 0, 4, 20]
  other     [0, 0, 0, 18]
```
Note: the "accuracy" here treats a real-route query sent to fallback as wrong, although fallback is a safe default; in practice track fallback separately from outright misroutes (the off-diagonal cells inside the first three columns).

**Follow-ups:**
- *LLM router or embedding router?* Start with prototypes or rules if the routes are few and stable; use an LLM when routes are many or fuzzy, and measure its latency and consistency.
- *How do you handle a query that needs two routes?* Allow multi-label routing, or send it to the more general strategy; log such cases.
- *Cost of a misroute?* Weight the confusion matrix by cost: global-as-FAQ gives a poor answer, FAQ-as-multihop only wastes compute.

**Common mistakes:** no fallback; routing without measuring end-to-end quality; training the router on the same templates you test on; ignoring queries that fit no route; a router that costs more than it saves; treating the toy embedder results as evidence about real models.

### Q24 ⭐⭐ 🟡 Conversational RAG: how do you handle coreference, history compression and query rewriting across turns, and how do you evaluate it?
**Asked at:** product, GenAI startups, customer-facing teams
**Say this first (1 line):** Rewrite each follow-up into a standalone query (resolve "it", "that", ellipsis) using a compressed history, retrieve with the rewritten query, and evaluate both the rewrite (is it faithful?) and the retrieval (recall with vs without rewriting).

**Then explain:**
- **Why:** the retriever sees only text. "How much does it cost?" has no entity, so the retriever returns generic cost chunks. Basics are in Part 6 Q28; this answer goes into evaluation and failure modes.
- **Coreference and ellipsis:** the rewriter must replace pronouns and restore dropped parts ("and the warranty?" becomes "what is the warranty of the Nimbus laptop?"). Resolve to the right entity, which is usually the most recently discussed one, but not always.
- **History compression:** sending the whole chat is slow and noisy. Options: last N turns, a rolling summary updated each turn, or a small memory of tracked entities and constraints. Summaries can drop details or add errors, so keep recent turns verbatim.
- **Evaluate the rewrite:** build small dialogues with a human-written standalone gold query. Score fidelity (exact match or token overlap, or an LLM/human judge for meaning), and check it did not add facts that were not in the conversation.
- **Evaluate retrieval:** recall@k and MRR of the gold chunk, with the raw follow-up, with the rewrite, and with both fused (Q14). Add answer-level checks (Part 9).
- **Pitfalls:** (1) rewriter hallucination: it invents an entity or detail; (2) wrong referent after a topic switch; (3) over-rewriting a query that was already standalone; (4) added latency and cost for an extra LLM call every turn (skip it for first turns or already-standalone queries); (5) rewriting that drops a user constraint such as a date.

**Example:** MOCK rewriters on six SYNTHETIC dialogues about two products. Without rewriting, retrieval gets the right chunk first for 3 of 6 (the follow-up "What is its battery life" matches the phone and the laptop equally). A recency rule that resolves "it" to the most recently mentioned product gets 6 of 6, with perfect fidelity to the gold standalone query. A buggy rewriter that resolves to the first product mentioned gets 4 of 6 and a fidelity of 0.83: after the user switches from the phone to the laptop it answers about the phone ("How long is the zephyr phone warranty"). That is the topic-switch failure, and only the fidelity check on a topic-switch slice catches it.

**Code:** (run; mock rule-based rewriters, toy corpus, BM25 from scratch; not an LLM)
```python
import re, math
from collections import Counter

STOP = set("a an the of to in on is are was for and or my how what does do with by at it its this that about can i you".split())
def toks(t): return re.findall(r"[a-z0-9]+", t.lower())
def ctoks(t): return [w for w in toks(t) if w not in STOP]

docs = {
 "zephyr_price":  "The Zephyr phone costs 24999 rupees and ships with a charger.",
 "zephyr_batt":   "The Zephyr phone battery lasts about two days and charges fully in an hour.",
 "zephyr_wty":    "The Zephyr phone warranty covers one year of defects.",
 "nimbus_price":  "The Nimbus laptop costs 58999 rupees including a sleeve.",
 "nimbus_batt":   "The Nimbus laptop battery lasts about ten hours of browsing.",
 "nimbus_wty":    "The Nimbus laptop warranty covers two years including battery.",
 "app_dark":      "The mobile app supports dark mode and offline reading.",
 "delivery":      "Delivery usually takes three to five working days.",
}
names = list(docs)
D = {n: ctoks(t) for n, t in docs.items()}; N = len(D); avg = sum(map(len, D.values())) / N
df = Counter(w for d in D.values() for w in set(d))
def search(q, k1=1.5, b=0.75):
    sc = {}
    for n, d in D.items():
        s = 0.0
        for w in ctoks(q):
            if w in df:
                tf = d.count(w); idf = math.log(1 + (N - df[w] + .5) / (df[w] + .5))
                s += idf * tf * (k1 + 1) / (tf + k1 * (1 - b + b * len(d) / avg))
        sc[n] = s
    return sorted(names, key=lambda n: -sc[n])

ENTITIES = ["zephyr phone", "nimbus laptop"]
PRON = r"\b(it|its|that|this one)\b"
def entities_in(text): return [e for e in ENTITIES if e in text.lower()]

# MOCK rewriters (rule-based stand-ins for an LLM rewriter)
def rewrite_recent(history, q):      # resolve the pronoun to the MOST RECENT entity mentioned
    ents = [e for h in history for e in entities_in(h)]
    if not ents or entities_in(q): return q
    return re.sub(PRON, "the " + ents[-1], q, count=1, flags=re.I)
def rewrite_first(history, q):       # buggy: resolves to the FIRST entity (ignores topic switch)
    ents = [e for h in history for e in entities_in(h)]
    if not ents or entities_in(q): return q
    return re.sub(PRON, "the " + ents[0], q, count=1, flags=re.I)

# SYNTHETIC dialogues: (history, follow-up, gold standalone, gold doc)
dialogs = [
 (["Tell me about the Zephyr phone"], "How much does it cost", "How much does the Zephyr phone cost", "zephyr_price"),
 (["Tell me about the Zephyr phone"], "What is its battery life", "What is the Zephyr phone battery life", "zephyr_batt"),
 (["Tell me about the Zephyr phone", "And the Nimbus laptop?"], "How long is its warranty", "How long is the Nimbus laptop warranty", "nimbus_wty"),
 (["Tell me about the Zephyr phone", "And the Nimbus laptop?"], "How much does it cost", "How much does the Nimbus laptop cost", "nimbus_price"),
 (["Tell me about the Nimbus laptop"], "What is its battery life", "What is the Nimbus laptop battery life", "nimbus_batt"),
 (["Tell me about the Zephyr phone"], "Does the app support dark mode", "Does the app support dark mode", "app_dark"),  # topic switch, no pronoun
]

def f1(a, b):
    a, b = Counter(ctoks(a)), Counter(ctoks(b)); ov = sum((a & b).values())
    if not ov: return 0.0
    p, r = ov / sum(a.values()), ov / sum(b.values()); return 2 * p * r / (p + r)

for name, rw in [("no rewrite", lambda h, q: q), ("rewrite: most-recent entity", rewrite_recent), ("rewrite: first entity (buggy)", rewrite_first)]:
    hit = fid = 0
    for hist, q, gold_q, gold_doc in dialogs:
        rq = rw(hist, q); hit += search(rq)[0] == gold_doc; fid += f1(rq, gold_q)
    print(f"{name:30s} recall@1 = {hit}/{len(dialogs)}   mean rewrite fidelity (token F1 vs gold) = {fid/len(dialogs):.2f}")
print("example:", repr(rewrite_first(dialogs[2][0], dialogs[2][1])), "<- wrong entity carried over")
```
Output (my run, mock and synthetic):
```
no rewrite                     recall@1 = 3/6   mean rewrite fidelity (token F1 vs gold) = 0.72
rewrite: most-recent entity    recall@1 = 6/6   mean rewrite fidelity (token F1 vs gold) = 1.00
rewrite: first entity (buggy)  recall@1 = 4/6   mean rewrite fidelity (token F1 vs gold) = 0.83
example: 'How long is the zephyr phone warranty' <- wrong entity carried over
```
Six dialogues is far too small for real conclusions; it demonstrates the metrics, not a result.

**Follow-ups:**
- *Rewrite or pass history to the generator only?* Retrieval needs the standalone query; the generator can still see the conversation. Do both.
- *Rolling summary risks?* Errors compound across turns; keep key entities and user constraints in a structured memory and the last few turns verbatim.
- *Should you retrieve with both original and rewrite?* Often yes: fuse them (RRF) so that a bad rewrite does not remove the original signal.

**Common mistakes:** rewriting with no evaluation set of dialogues; no topic-switch cases; trusting an LLM rewrite without a fidelity check; rewriting every turn even when standalone; dropping constraints (dates, names) during rewriting; summarising away the entity that the next turn refers to.

### Q25 ⭐⭐ 🟡 What is index-time enrichment (hypothetical questions per chunk, summaries, entity and keyword extraction, metadata), and what are its trade-offs?
**Asked at:** product, GenAI startups, GCC
**Say this first (1 line):** Index-time enrichment means paying once, at ingestion, to attach extra text or fields to each chunk (likely questions, a summary, entities, keywords, metadata) so that user queries match it better; the trade-off is index cost, storage, staleness and the risk of wrong generated content.

**Then explain:**
- **Hypothetical questions per chunk (doc2query-style, from memory, not re-verified here):** an LLM writes questions the chunk could answer, and you index them with the chunk (or as separate vectors pointing back to it). User questions are question-shaped, so they match question text better than statement text. This is related to HyDE (Part 7 Q8) but done offline instead of at query time.
- **Summaries:** a short summary per chunk or section helps matching for long or dense chunks, and feeds hierarchical retrieval (Q27). The Contextual Retrieval post reported that generic document summaries gave little gain, so test it.
- **Entities and keywords:** extracted names, IDs and terms support exact matching and filtering (hybrid, Q15).
- **Metadata:** title, section path, date, source, access tags. Cheap, deterministic, and gives filters and freshness rules. Lighter than LLM-generated context (Q26).
- **Trade-offs:** one LLM call per chunk at ingestion (the cost multiplies with corpus size and every re-index); more storage (more text and vectors); staleness (when a chunk changes, regenerate its enrichment); hallucinated questions or summaries can attract wrong queries; duplicate questions across chunks hurt precision.
- **Evaluate as an ablation (Q14):** same golden set with and without each enrichment; check recall, and read a sample of generated text for errors.

**Example:** MOCK and toy. Eight HR-policy chunks and eight user questions phrased differently from the chunk text ("how many vacation days do I get" vs a chunk about "paid leave"). BM25 on chunk text alone gets the right chunk first for 3 of 8 (hit@1 0.38). Adding mock "generated" questions raises it to 8 of 8, but I wrote those mock questions with the test queries in mind, so that lift is an optimistic illustration, not an estimate of what a real LLM gives. When one chunk gets a hallucinated question that belongs to another chunk, hit@1 falls to 0.88 and MRR to 0.94: bad enrichment steals queries. Index text doubled in size (89 to 178 words).

**Code:** (run; BM25 from scratch; the "generated" questions are hand-written MOCK data, no LLM call)
```python
import re, math
from collections import Counter

STOP = set("a an the of to in on is are was for and or my how what does do with by at it its this that about can i you be when where who".split())
def ctoks(t): return [w for w in re.findall(r"[a-z0-9]+", t.lower()) if w not in STOP]

chunks = [
 "Employees accrue 1.5 days of paid leave per month, capped at 30 days.",
 "Reimbursement claims must be filed within 45 days with original receipts.",
 "The VPN client must be updated to version 5 before connecting from home.",
 "Laptops are replaced every four years by the IT asset team.",
 "Notice period for resignation is 60 days for managers.",
 "Meals during official travel are covered up to 1200 rupees per day.",
 "Passwords expire every 90 days and cannot reuse the last five.",
 "Parental leave is 26 weeks for the primary caregiver.",
]
# MOCK "LLM" generated questions per chunk (hand-written; stands in for doc2query-style generation, not run on a model)
mock_questions = {
 0: ["How many vacation days do I earn each month", "Is there a limit on leave balance"],
 1: ["By when must I submit an expense claim", "What proof do I need to get my money back"],
 2: ["What do I need before I can connect to the company network from home"],
 3: ["How often do I get a new work computer"],
 4: ["How long must I serve after I quit"],
 5: ["How much can I spend on food while travelling for work"],
 6: ["How often must I change my login secret"],
 7: ["How long is maternity leave"],
}
# one BAD mock enrichment (hallucinated): chunk 3 gets a question about vacation days it does not answer
bad_questions = dict(mock_questions); bad_questions[3] = mock_questions[3] + ["How many vacation days do I earn each month"]

queries = [("how many vacation days do I get", 0), ("by when should I submit my expense claim", 1),
           ("what do I need to connect to the network from home", 2), ("how often do I get a new work computer", 3),
           ("how long must I serve after I quit", 4), ("how much can I spend on food while travelling", 5),
           ("how often must I change my login secret", 6), ("how long is maternity leave", 7)]
# CAUTION: the mock questions were written with these queries in mind, so the lift below is an optimistic illustration, not an estimate

def build(texts):
    D = [ctoks(t) for t in texts]; N = len(D); avg = sum(map(len, D)) / N
    df = Counter(w for d in D for w in set(d))
    def score(q, k1=1.5, b=0.75):
        out = []
        for d in D:
            s = 0.0
            for w in ctoks(q):
                if w in df:
                    tf = d.count(w); idf = math.log(1 + (N - df[w] + .5) / (df[w] + .5))
                    s += idf * tf * (k1 + 1) / (tf + k1 * (1 - b + b * len(d) / avg))
            out.append(s)
        return out
    return score

def evaluate(texts):
    sc = build(texts); hit1 = rr = 0
    for q, rel in queries:
        s = sc(q); order = sorted(range(len(s)), key=lambda i: (-s[i], i))
        pos = order.index(rel) + 1 if s[rel] > 0 else len(s)   # zero score = not retrieved
        hit1 += pos == 1; rr += 1 / pos
    return hit1 / len(queries), rr / len(queries)

plain = chunks
enriched = [c + " " + " ".join(mock_questions[i]) for i, c in enumerate(chunks)]
bad = [c + " " + " ".join(bad_questions[i]) for i, c in enumerate(chunks)]
for name, texts in [("chunk text only", plain), ("chunk + mock questions", enriched), ("chunk + questions incl. 1 hallucinated", bad)]:
    h, m = evaluate(texts); print(f"{name:40s} hit@1={h:.2f}  MRR={m:.2f}")
print("index size (words): plain =", sum(len(c.split()) for c in plain), " enriched =", sum(len(c.split()) for c in enriched))
```
Output (my run, mock and toy):
```
chunk text only                          hit@1=0.38  MRR=0.45
chunk + mock questions                   hit@1=1.00  MRR=1.00
chunk + questions incl. 1 hallucinated   hit@1=0.88  MRR=0.94
index size (words): plain = 89  enriched = 178
```

**Follow-ups:**
- *Embed the questions separately?* A common design: one vector per generated question, each pointing back to the parent chunk, so the question text is matched directly. It multiplies vector count; measure whether it beats appending questions to the chunk.
- *When not to bother?* Small corpus, queries already match chunk wording, or the corpus changes constantly so regeneration cost dominates.
- *How to control hallucination?* Constrain the prompt to the chunk text, keep questions answerable from the chunk, sample-check, and drop near-duplicates across chunks.

**Common mistakes:** enriching without an ablation; ignoring regeneration cost on updates; letting the LLM add facts that are not in the chunk; writing the test set after seeing the generated questions (leakage); quoting a percentage gain for doc2query from memory; forgetting that enriched text can also dilute exact matching.

### Q26 ⭐⭐ 🟡 Contextual retrieval in practice: how do you generate chunk context cheaply (prompt caching, lighter alternatives) and what can go wrong?
**Asked at:** product, GenAI startups, platform teams
**Say this first (1 line):** Generate a short context for every chunk from its whole document, make it cheap by caching the document prompt once across that document's chunks (as the original post describes) or by using lighter options like title and section path, and prove it pays off with an ablation before running it on the full corpus.

**Then explain:**
- **What the post describes (opened page, Anthropic, Sep 2024):** an LLM reads the whole document plus one chunk and writes a short chunk-specific context (50-100 tokens) that is prepended before embedding and before BM25 indexing (basics and reported gains: Part 7 Q11). Prompt caching lets the document be loaded once and reused for all its chunks, which is what makes this practical. The post's cost estimate depends on its own assumptions; do not treat it as a price.
- **Caching mechanics:** put the document at the start of the prompt (the cacheable prefix) and the chunk and instruction at the end. Each call then pays a cheap cached read for the document instead of the full input price. Details (cache lifetime, minimum sizes, discount rates) are provider-specific and change: check the current documentation.
- **Lighter alternatives:** prepend the document title and section path (free, deterministic, no hallucination risk); prepend a short generated document-level summary (one call per document, not per chunk; the post reported that generic summaries gave little gain, so test it); or generate context only for chunk types that need it (tables, numbered clauses, pronoun-heavy text).
- **Batch generation:** run ingestion as an asynchronous batch job if the provider offers a batch mode, group chunks by document so the cache is reused, and checkpoint so failures do not repeat work.
- **What goes wrong:** the context hallucinates a fact (it is then indexed and retrieved as if true: sample and review); longer chunks dilute the embedding or push chunks over the embedder's max length; duplicated boilerplate context across chunks makes them look alike; documents change so contexts go stale; cost at 100M chunks is large even with caching (below); very long documents do not fit in the prompt.
- **Evaluate as an ablation (Q14):** same golden set, with and without context, with context in embeddings only, BM25 only, or both; report recall gain against ingestion cost and index growth.

**Example:** Everything here is ASSUMED. 5M documents, 8,000 tokens each, 20 chunks per document (100M chunks), 400-token chunks, 100-token prompt, 75-token generated context, output priced at 5x input, cache write at 1.25x, cached read at 0.1x. Cost in abstract units (1 unit = one million uncached input tokens): without caching 887,500 units, with caching 213,500 (ratio 0.24), and with an assumed 50% batch discount on top, 106,750. The saving comes from not re-sending the 8,000-token document 20 times. For short documents (1,000 tokens) the ratio is 0.55, so caching matters less. Plug in your provider's rates and your own corpus shape.

**Code:** (run; pure Python; all constants are ASSUMPTIONS, costs are in abstract units, no real prices)
```python
# Cost calculator for LLM-generated chunk context. EVERY number below is an ASSUMPTION for illustration.
# Costs are in abstract "units" where 1 unit = the assumed cost of 1 million uncached input tokens.
# (No real price is used; plug in your provider's current rates.)
A = dict(
    docs=5_000_000,            # ASSUMED number of documents
    doc_tokens=8_000,          # ASSUMED tokens per document
    chunks_per_doc=20,         # ASSUMED -> 5M x 20 = 100M chunks
    chunk_tokens=400,          # ASSUMED tokens per chunk
    prompt_tokens=100,         # ASSUMED instruction text per call
    ctx_out_tokens=75,         # ASSUMED generated context length per chunk
    out_price=5.0,             # ASSUMED output token price = 5x an uncached input token
    cache_write_mult=1.25,     # ASSUMED premium for writing the document into the cache once
    cache_read_mult=0.10,      # ASSUMED cached-read price = 10% of an uncached input token
    batch_mult=0.5,            # ASSUMED discount factor if the provider offers an asynchronous batch mode
)
def cost(a, cached, batch=False):
    chunks = a["docs"] * a["chunks_per_doc"]
    per_doc_tok = a["doc_tokens"]
    if cached:   # document written to cache once per document, then read for every chunk of it
        doc_cost = per_doc_tok * a["cache_write_mult"] + per_doc_tok * a["cache_read_mult"] * (a["chunks_per_doc"] - 1)
    else:        # whole document re-sent as normal input on every call
        doc_cost = per_doc_tok * a["chunks_per_doc"]
    other_in = (a["chunk_tokens"] + a["prompt_tokens"]) * a["chunks_per_doc"]
    out = a["ctx_out_tokens"] * a["out_price"] * a["chunks_per_doc"]
    total_per_doc = doc_cost + other_in + out
    total = total_per_doc * a["docs"] / 1e6
    return total * (a["batch_mult"] if batch else 1.0)

chunks = A["docs"] * A["chunks_per_doc"]
print(f"chunks: {chunks:,}")
for label, c, b in [("no caching", False, False), ("prompt caching", True, False), ("caching + batch discount", True, True)]:
    print(f"{label:26s} {cost(A, c, b):10,.0f} units")
print(f"ratio caching / no caching: {cost(A, True) / cost(A, False):.2f}")
print("lighter alternative: title + section path prepended = 0 LLM calls (string concatenation at ingestion)")
# sensitivity: shorter documents shrink the benefit of caching
for dt in (1_000, 8_000, 50_000):
    a = dict(A, doc_tokens=dt)
    print(f"doc_tokens={dt:6d}: caching/no-caching = {cost(a, True) / cost(a, False):.2f}")
```
Output (my run, assumed inputs):
```
chunks: 100,000,000
no caching                    887,500 units
prompt caching                213,500 units
caching + batch discount      106,750 units
ratio caching / no caching: 0.24
lighter alternative: title + section path prepended = 0 LLM calls (string concatenation at ingestion)
doc_tokens=  1000: caching/no-caching = 0.55
doc_tokens=  8000: caching/no-caching = 0.24
doc_tokens= 50000: caching/no-caching = 0.17
```

**Follow-ups:**
- *Is it worth it?* Only if the ablation shows a recall gain on your golden set that justifies the ingestion cost; the post's reported gains (35%, 49%, 67% fewer failures in its setting) are one vendor's measurements, not a promise.
- *Under about 200k tokens of knowledge base?* The post suggests putting everything in the prompt and skipping RAG; weigh that against per-query cost and latency (Part 6 Q49).
- *Re-index cost?* Context depends on the whole document, so any edit to the document invalidates the contexts of its chunks; budget for regeneration.

**Common mistakes:** generating context before running a small ablation; putting the chunk before the document in the prompt (breaks the cacheable prefix); ignoring that the cost scales with documents times chunks per document; no review of generated context for hallucination; forgetting to re-embed and re-index BM25 after adding context; quoting a vendor dollar estimate as a price.
