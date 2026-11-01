import math, numpy as np
# toy 2-step "language model": P(w1), then P(w2 | w1). Hand-set probabilities (illustrative).
p1 = {"A": 0.5, "B": 0.4, "C": 0.1}
p2 = {"A": {"x": 0.4, "y": 0.3, "z": 0.3},       # after A: flat, no great continuation
      "B": {"x": 0.9, "y": 0.05, "z": 0.05},     # after B: one confident continuation
      "C": {"x": 0.5, "y": 0.5}}
# greedy
w1 = max(p1, key=p1.get); w2 = max(p2[w1], key=p2[w1].get)
print("greedy:", w1, w2, "joint p =", round(p1[w1]*p2[w1][w2], 3))
# exhaustive best sequence
seqs = {(a, b): p1[a]*pb for a in p1 for b, pb in p2[a].items()}
best = max(seqs, key=seqs.get); print("best sequence:", best, round(seqs[best], 3))
# beam search width 2
beam = sorted(((math.log(p), (a,)) for a, p in p1.items()), reverse=True)[:2]
cand = [(lp + math.log(p), s + (b,)) for lp, s in beam for b, p in p2[s[-1]].items()]
beam = sorted(cand, reverse=True)[:2]
print("beam(2):", [(s, round(math.exp(lp), 3)) for lp, s in beam])
# sampling
rng = np.random.default_rng(0)
draws = [(rng.choice(list(p1), p=list(p1.values()))) for _ in range(10000)]
print("sampled first token freq:", {k: draws.count(k)/10000 for k in p1})
