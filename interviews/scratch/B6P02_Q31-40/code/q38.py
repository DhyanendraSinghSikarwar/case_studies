# Q38: moderation recall measured only on reviewed items is biased (illustrative simulation)
import numpy as np

rng = np.random.default_rng(38)
N = 1_000_000
harm = rng.random(N) < 0.02                       # 2% harmful
new_type = harm & (rng.random(N) < 0.45)          # a new kind of harm the model has not seen (45% of harm)
# model score: old-type harm scores high, new-type harm scores like ordinary content, ordinary items score low
score = np.where(harm & ~new_type, rng.beta(8, 1.5, N), np.where(new_type, rng.beta(2, 4, N), rng.beta(1.2, 6, N)))
flagged = score >= 0.6
true_recall = (flagged & harm).sum() / harm.sum()

# Review policy: all flagged items go to reviewers, plus 30% of items with score 0.3-0.6 (borderline)
mid = (score >= 0.3) & (score < 0.6)
reviewed = flagged | (mid & (rng.random(N) < 0.30))
rep_recall = (reviewed & flagged & harm).sum() / (reviewed & harm).sum()
print(f"true recall {true_recall:.3f}   reported recall (reviewed items only) {rep_recall:.3f}   reviewed {reviewed.sum():,} of {N:,}")
assert rep_recall > true_recall + 0.25 and 0.88 < rep_recall < 0.91

caught = (flagged & harm).sum(); extra = (reviewed & ~flagged & harm).sum()
print(f"harmful total {harm.sum():,}  flagged harmful {caught:,}  harmful seen by reviewers but not flagged {extra:,}")
assert abs(caught - 11_300) < 300 and abs(extra - 1_350) < 150
# Unbiased estimate 1: simple random sample of 20,000 items, reviewed by humans
def srs_estimate(n, seed):
    r = np.random.default_rng(seed); idx = r.choice(N, n, replace=False)
    h = harm[idx]; f = flagged[idx]
    return (f & h).sum() / h.sum(), h.sum()
ests = [srs_estimate(20_000, s) for s in range(200)]
e = np.array([x[0] for x in ests]); nh = np.mean([x[1] for x in ests])
print(f"SRS 20,000: mean harmful found {nh:.0f}; recall estimate mean {e.mean():.3f}, sd across repeats {e.std():.3f}")
assert abs(e.mean() - true_recall) < 0.01

# Unbiased estimate 2: stratified sample with the same budget (20,000), inverse-probability weights
strata = {"flagged": flagged, "mid": mid, "low": score < 0.3}
alloc = {"flagged": 3_000, "mid": 5_000, "low": 12_000}
def strat_estimate(seed):
    r = np.random.default_rng(seed); caught = 0.0; harm_tot = 0.0
    for k, m in strata.items():
        idx = np.flatnonzero(m); take = r.choice(idx, alloc[k], replace=False)
        w = len(idx) / alloc[k]
        h = harm[take]
        harm_tot += w * h.sum()
        if k == "flagged": caught += w * h.sum()
    return caught / harm_tot
es = np.array([strat_estimate(s) for s in range(200)])
print(f"stratified 20,000: recall estimate mean {es.mean():.3f}, sd across repeats {es.std():.3f}")
assert abs(es.mean() - true_recall) < 0.01 and es.std() < e.std()

# How many items does a +-3 point 95% interval need under simple random sampling?
prev = harm.mean()
n_harm = 1.96 ** 2 * true_recall * (1 - true_recall) / 0.03 ** 2
print(f"harmful items needed {n_harm:.0f}; sampled items needed {n_harm / prev:,.0f}")
assert 1000 < n_harm < 1100
