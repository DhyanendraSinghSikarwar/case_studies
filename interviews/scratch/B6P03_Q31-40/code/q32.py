import numpy as np
from scipy.stats import beta

rng = np.random.default_rng(32)
N = 20000
y = (rng.random(N) < 0.25).astype(int)            # 1 = spam, invented prevalence 25%
cover = [0.20, 0.35, 0.50]
acc = [0.90, 0.75, 0.65]                          # true accuracy of each rule where it fires (hidden from the model)
L = np.full((N, 3), -1)                           # -1 = abstain
for j in range(3):
    fires = rng.random(N) < cover[j]
    right = rng.random(N) < acc[j]
    L[:, j] = np.where(fires, np.where(right, y, 1 - y), -1)

print("coverage per rule:", [round(float((L[:, j] >= 0).mean()), 3) for j in range(3)])
union = (L >= 0).any(1)
print("posts with at least one vote:", round(float(union.mean()), 3))
assert abs(union.mean() - (1 - 0.8 * 0.65 * 0.5)) < 0.01

# agreement on overlaps (no labels needed)
def agree(i, j):
    both = (L[:, i] >= 0) & (L[:, j] >= 0)
    return both.sum(), (L[both, i] == L[both, j]).mean()
for i, j in [(0, 1), (0, 2), (1, 2)]:
    n, a = agree(i, j)
    print(f"rules {i+1},{j+1}: overlap n={n}, agree={a:.3f}")

# triplet method: with conditionally independent rules, m_i = 2*acc_i - 1 and E[l_i l_j] = m_i m_j (votes as +-1)
def m_ij(i, j):
    both = (L[:, i] >= 0) & (L[:, j] >= 0)
    return np.mean((2 * L[both, i] - 1) * (2 * L[both, j] - 1))
m = [np.sqrt(m_ij(0, 1) * m_ij(0, 2) / m_ij(1, 2)),
     np.sqrt(m_ij(0, 1) * m_ij(1, 2) / m_ij(0, 2)),
     np.sqrt(m_ij(0, 2) * m_ij(1, 2) / m_ij(0, 1))]
est = [(1 + x) / 2 for x in m]
print("estimated accuracy (no labels):", [round(float(a), 3) for a in est], " true:", acc)
assert all(abs(e - a) < 0.05 for e, a in zip(est, acc))

# combine: majority vote versus accuracy-weighted vote (weights = log-odds of estimated accuracy)
w = np.log(np.array(est) / (1 - np.array(est)))
score = np.zeros(N)
for j in range(3):
    score += np.where(L[:, j] >= 0, w[j] * (2 * L[:, j] - 1), 0.0)
mv = np.where(L >= 0, 2 * L - 1, 0).sum(1)
wv_lab = np.where(score > 0, 1, 0); mv_lab = np.where(mv > 0, 1, 0)
dec_w = union & (score != 0); dec_m = union & (mv != 0)
print("majority vote: decided", round(float(dec_m.mean()), 3), " accuracy", round(float((mv_lab[dec_m] == y[dec_m]).mean()), 3))
print("weighted vote: decided", round(float(dec_w.mean()), 3), " accuracy", round(float((wv_lab[dec_w] == y[dec_w]).mean()), 3))
accw = (wv_lab[dec_w] == y[dec_w]).mean(); accm = (mv_lab[dec_m] == y[dec_m]).mean()
common = dec_m & dec_w
am = (mv_lab[common] == y[common]).mean(); aw = (wv_lab[common] == y[common]).mean()
print("same posts both decide:", round(float(common.mean()), 3), " majority", round(float(am), 3), " weighted", round(float(aw), 3))
assert aw > am
conflict = ((L == 1).sum(1) > 0) & ((L == 0).sum(1) > 0) & dec_w
print("posts where rules vote both ways:", int(conflict.sum()), " weighted vote accuracy there:", round(float((wv_lab[conflict] == y[conflict]).mean()), 3))
assert (wv_lab[conflict] == y[conflict]).mean() > 0.6

# the 300 hand labels: how well can they measure each rule alone?
hand = rng.choice(N, 300, replace=False)
for j in range(3):
    f = hand[L[hand, j] >= 0]
    k = int((L[f, j] == y[f]).sum()); n = len(f)
    lo, hi = beta.ppf(0.025, k, n - k + 1), beta.ppf(0.975, k + 1, n - k)
    print(f"rule {j+1}: hand-labelled posts where it fires n={n}, accuracy {k/n:.2f}, 95% CI {lo:.2f}-{hi:.2f}")
# the width on rule 1 (about 60 posts) is wide: that is why the hand set validates, it does not fit the weights
n1 = int((L[hand, 0] >= 0).sum())
assert 40 <= n1 <= 80
