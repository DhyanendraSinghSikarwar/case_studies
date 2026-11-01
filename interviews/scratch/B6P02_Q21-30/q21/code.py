import numpy as np

# Part A: the prompt's arithmetic (illustrative levels)
ctr0, ctr1 = 0.0500, 0.0470
assert abs((ctr1 - ctr0) / ctr0 - (-0.06)) < 1e-9          # 6% relative slide
ndcg0, ndcg1 = 0.500, 0.515
assert abs((ndcg1 - ndcg0) / ndcg0 - 0.03) < 1e-9          # +3% relative
print("CTR 5.00% -> 4.70% = -6.0% relative; NDCG 0.500 -> 0.515 = +3.0% relative")

# Part B: toy feedback loop. Assumption (labelled): an item's appeal saturates with repeated
# exposure, p_eff = p * exp(-impressions / TAU).
rng = np.random.default_rng(21)
N, K, ROUNDS, USERS, TAU = 300, 5, 300, 200, 200000.0
true_p = rng.beta(2, 38, N)                       # mean about 5%
exam = np.array([1.0, 0.6, 0.4, 0.3, 0.2])        # position bias
head_start = rng.permutation(1.0 / np.arange(1, N + 1)) * 40  # legacy popularity, unrelated to true_p

def run(policy):
    clicks = rng.poisson(head_start).astype(float)
    imps = np.zeros(N)
    shown = set(); ctrs = []; imp_total = np.zeros(N)
    for r in range(ROUNDS):
        if policy == "popularity":
            slate = np.argsort(-clicks)[:K]
        else:                                        # rate-based, 1 of 5 slots is random exploration
            score = (clicks + 1) / (imps + 20)
            slate = list(np.argsort(-score)[:K - 1])
            rest = [i for i in range(N) if i not in slate]
            slate.append(int(rng.choice(rest)))
            slate = np.array(slate)
        p_eff = true_p[slate] * np.exp(-imp_total[slate] / TAU)
        c = rng.binomial(USERS, exam * p_eff)
        clicks[slate] += c; imps[slate] += USERS; imp_total[slate] += USERS
        shown.update(slate.tolist())
        ctrs.append((exam * p_eff).sum() / exam.sum())
    ctrs = np.array(ctrs)
    top5_share = np.sort(imp_total)[::-1][:5].sum() / imp_total.sum()
    return ctrs[:20].mean(), ctrs[-20:].mean(), len(shown), top5_share

for pol in ("popularity", "explore"):
    a, b, d, s = run(pol)
    print(f"{pol:10s} slate CTR first20={a:.4f} last20={b:.4f} ({(b-a)/a:+.1%}) distinct items shown={d} top5 impression share={s:.2f}")
    if pol == "popularity":
        pa, pb, pd, ps = a, b, d, s
    else:
        ea, eb, ed, es = a, b, d, s
assert pb < pa                  # greedy slate CTR slides
assert pd < ed                  # greedy shows fewer distinct items
assert ps > es                  # greedy concentrates impressions
assert eb > pb                  # exploring policy ends higher
print("asserts passed")
