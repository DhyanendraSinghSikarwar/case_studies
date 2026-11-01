import numpy as np

n, share = 500_000, 0.032
diff_n = round(n * share)
assert diff_n == 16_000
rng = np.random.default_rng(16)
thr = 0.50                                         # decision threshold, as stated
prod = rng.beta(2, 5, n)                           # production scores
cand = prod.copy()
idx = rng.choice(n, diff_n, replace=False)
sign = rng.choice([-1, 1], diff_n); mag = rng.uniform(0.051, 0.30, diff_n)
new = prod[idx] + sign * mag
sign = np.where((new < 0) | (new > 1), -sign, sign)       # flip direction instead of clipping
cand[idx] = prod[idx] + sign * mag
big = np.abs(cand - prod) > 0.05
assert big.sum() == diff_n
print("requests differing by more than 0.05:", int(big.sum()), f"({big.mean()*100:.2f}%)")
flip = (cand >= thr) != (prod >= thr)
print("decision flips at threshold 0.5:", int(flip.sum()), f"= {flip.sum()/n*100:.2f}% of all requests, {flip.sum()/big.sum()*100:.0f}% of the big diffs")
assert flip.sum() < big.sum()
up = (cand - prod)[big] > 0
print("candidate higher on", int(up.sum()), "| lower on", int((~up).sum()))
# Review sample: 400 of the 16,000 gives a margin of error of about 4.9 points at p = 0.5
m = 1.96 * (0.25 / 400) ** 0.5
print("margin of error for a 400-request review:", round(m * 100, 1), "points")
assert round(m * 100, 1) == 4.9
# Stratified plan: review the flips first (these change what the user sees)
print("review plan: 200 from the", int(flip.sum()), "flips + 200 from the", int(big.sum() - flip.sum()), "non-flip big diffs")
assert 200 < flip.sum() and 200 < big.sum() - flip.sum()
