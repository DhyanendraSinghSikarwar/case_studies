# TOY two-stage retrieval on synthetic text. Stage 1: bag-of-words overlap (cheap, whole corpus).
# Stage 2: a hand-written pair scorer using term proximity (stand-in for a cross-encoder; NOT a learned model).
import random, math
random.seed(1)
vocab = [f"w{i}" for i in range(200)]
queries, docs, gold = [], [], []
for _ in range(60):
    q = random.sample(vocab, 3); queries.append(q)
    # gold doc: the 3 query words appear close together
    g = random.choices(vocab, k=25); pos = random.randrange(20); g[pos:pos+3] = q
    gi = len(docs); docs.append(g); gold.append(gi)
    # hard negatives: same 3 words but far apart (identical bag-of-words overlap)
    for _ in range(15):
        d = random.choices(vocab, k=25)
        for w, p in zip(q, (1, 12, 23)): d[p] = w
        docs.append(d)
order = list(range(len(docs))); random.shuffle(order)       # ties in stage 1 are broken by this random order
pos_in = {d: p for p, d in enumerate(order)}
def stage1(q, d): return sum(w in d for w in q)                      # bag-of-words overlap
def stage2(q, d):                                                    # proximity: tightest window holding all terms
    pos = [[i for i, x in enumerate(d) if x == w] for w in q]
    if any(not p for p in pos): return -1.0
    best = min(max(c) - min(c) for c in ((a, b, c) for a in pos[0] for b in pos[1] for c in pos[2]))
    return stage1(q, d) + 3.0 / (1 + best)
def rank_of(lst, t): return lst.index(t) + 1 if t in lst else None

def evaluate(n_cand):
    rr1, rr2, nd1, nd2, rec = [], [], [], [], 0
    for q, g in zip(queries, gold):
        s1 = sorted(order, key=lambda i: (-stage1(q, docs[i]), pos_in[i]))     # full-corpus first stage
        cand = s1[:n_cand]
        r1 = rank_of(cand, g)
        if r1 is None: rr1.append(0); rr2.append(0); nd1.append(0); nd2.append(0); continue
        rec += 1
        re = sorted(cand, key=lambda i: -stage2(q, docs[i])); r2 = rank_of(re, g)
        rr1.append(1 / r1); rr2.append(1 / r2)
        nd1.append(1 / math.log2(r1 + 1) if r1 <= 10 else 0); nd2.append(1 / math.log2(r2 + 1) if r2 <= 10 else 0)
    m = lambda x: round(sum(x) / len(x), 3)
    print(f"n={n_cand:3}: shortlist recall={rec/len(queries):.2f} | MRR {m(rr1)} -> {m(rr2)} | nDCG@10 {m(nd1)} -> {m(nd2)}")
print("corpus size:", len(docs))
for n in (5, 20, 50): evaluate(n)
print("ASSUMED per-pair cost (not measured), serial, no batching:")
for ms in (2, 10):
    print(f"  {ms} ms/pair: n=50 -> {50*ms} ms, n=200 -> {200*ms} ms; batching/GPU would cut this")
