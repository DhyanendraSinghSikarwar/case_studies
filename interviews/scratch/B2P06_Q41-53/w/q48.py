# Standalone, numpy only. TOY: synthetic multi-topic text, bag-of-words sentence vectors (no real embeddings, no semantic quality claims).
import numpy as np
rng = np.random.default_rng(5)
topics = {t: [f"{t}{i}" for i in range(25)] for t in ["billing", "shipping", "login", "warranty"]}
common = ["the", "a", "is", "to", "and", "for"]
sent_per_topic = [7, 12, 5, 9]                      # uneven section lengths on purpose
sents, truth = [], []                               # truth = sentence indices where a new topic starts
for t, n in zip(topics, sent_per_topic):
    truth.append(len(sents))
    for _ in range(n): sents.append(list(rng.choice(topics[t], 7)) + list(rng.choice(common, 3)))
truth = set(truth[1:]); vocab = {w: i for i, w in enumerate(sorted({w for s in sents for w in s}))}
def vec(ws):
    v = np.zeros(len(vocab))
    for w in ws: v[vocab[w]] += 1
    return v / np.linalg.norm(v)
V = np.stack([vec(s) for s in sents])
W = np.stack([vec(sum(sents[max(0, i - 1):i + 2], [])) for i in range(len(sents))])      # window of 3 sentences smooths noise
def breakpoints(M, pct=15):
    sim = np.array([M[i] @ M[i + 1] for i in range(len(M) - 1)])    # similarity between neighbours i and i+1
    thr = np.percentile(sim, pct); return {i + 1 for i, s in enumerate(sim) if s <= thr}, sim
def f1(pred, truth, tol=1):
    tp = sum(any(abs(p - t) <= tol for p in pred) for t in truth); pr = sum(any(abs(p - t) <= tol for t in truth) for p in pred)
    P, R = pr / max(1, len(pred)), tp / len(truth); return 2 * P * R / (P + R) if P + R else 0
def sizes(bps, n): b = [0] + sorted(bps) + [n]; return [b[i + 1] - b[i] for i in range(len(b) - 1)]
print("true topic starts at sentences:", sorted(truth), "| sentences per topic:", sent_per_topic)
for name, M in [("sentence vectors", V), ("3-sentence windows", W)]:
    bp, _ = breakpoints(M, 8); print(f"semantic ({name}, 8th percentile): boundaries {sorted(bp)} F1(tol=1)={f1(bp, truth):.2f} chunk sizes {sizes(bp, len(sents))}")
fixed = set(range(7, len(sents), 7)); print(f"fixed 7-sentence chunks: boundaries {sorted(fixed)} F1(tol=1)={f1(fixed, truth):.2f} chunk sizes {sizes(fixed, len(sents))}")
