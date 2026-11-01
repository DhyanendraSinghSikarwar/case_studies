# Standalone, numpy only. SYNTHETIC corpus, TOY hashed bag-of-words retrieval; shows experiment design and metric pitfalls, not real chunking quality.
import zlib, numpy as np
rng = np.random.default_rng(3)
D, NDOC, DOCLEN, K = 4096, 150, 240, 3
filler = [f"f{i}" for i in range(400)]
def emb(ws):
    v = np.zeros(D)
    for w in ws: v[zlib.crc32(w.encode()) % D] += 1
    n = np.linalg.norm(v); return v / n if n else v
docs, queries = [], []                                   # each doc hides one answer sentence containing 3 rare words; the query uses 2 of them
for d in range(NDOC):
    ws = list(rng.choice(filler, DOCLEN)); rare = [f"r{d}_{j}" for j in range(3)]
    pos = int(rng.integers(0, DOCLEN - 6)); ws[pos:pos + 3] = rare
    docs.append((ws, pos)); queries.append((d, [rare[0], rare[1]] + list(rng.choice(filler, 1))))

def evaluate(size, overlap):
    step = size - overlap; chunks = []                   # (doc, start, end, vec)
    for d, (ws, _) in enumerate(docs):
        for s in range(0, max(1, len(ws) - overlap), step): chunks.append((d, s, min(len(ws), s + size), emb(ws[s:s + size])))
    M = np.stack([c[3] for c in chunks]); span_hit, doc_hit, chunk_recall, ctx = [], [], [], []
    for d, q in queries:
        top = np.argsort(-(M @ emb(q)))[:K]; pos = docs[d][1]
        span_hit.append(float(any(chunks[i][0] == d and chunks[i][1] <= pos and pos + 3 <= chunks[i][2] for i in top)))
        doc_hit.append(float(any(chunks[i][0] == d for i in top)))
        gold = [i for i, c in enumerate(chunks) if c[0] == d]                      # NAIVE gold: every chunk of the gold doc
        chunk_recall.append(len(set(top) & set(gold)) / len(gold))
        ctx.append(sum(chunks[i][2] - chunks[i][1] for i in top))
    return np.array(span_hit), np.array(doc_hit), np.array(chunk_recall), np.mean(ctx), len(chunks)

print(f"{'size/overlap':>12} {'#chunks':>8} {'span-hit@3':>10} {'doc-hit@3':>10} {'naive chunk-recall@3':>21} {'ctx words':>10}")
R = {}
for size, ov in [(20, 0), (60, 10), (120, 20)]:
    sh, dh, cr, ctx, n = evaluate(size, ov); R[size] = sh
    print(f"{size:>6}/{ov:<5} {n:>8} {sh.mean():>10.3f} {dh.mean():>10.3f} {cr.mean():>21.3f} {ctx:>10.0f}")

def paired_bootstrap(a, b, n=5000, seed=0):             # resample QUERIES, keep each query's pair together
    r = np.random.default_rng(seed); idx = r.integers(0, len(a), (n, len(a)))
    diffs = (a[idx] - b[idx]).mean(1); return (a - b).mean(), np.percentile(diffs, [2.5, 97.5])
for x, y in [(60, 20), (120, 60)]:
    d, ci = paired_bootstrap(R[x], R[y]); print(f"span-hit {x}-word vs {y}-word chunks: diff {d:+.3f}, 95% paired-bootstrap CI [{ci[0]:+.3f}, {ci[1]:+.3f}]")
