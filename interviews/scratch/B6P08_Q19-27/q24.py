# Q24: finding a leaky feature (ticket_reopened). Synthetic, seeded, illustrative.
import numpy as np
rng = np.random.default_rng(24)
N = 40_000
y = (rng.random(N) < 0.3).astype(int)
def auc(y, s):
    r = s.argsort(kind="stable").argsort() + 1
    n1 = y.sum(); n0 = len(y) - n1
    return float((r[y == 1].sum() - n1 * (n1 + 1) / 2) / (n1 * n0))
# 8 legitimate features known before the decision; one strong but legitimate; one leaky binary
names = [f"f{i}" for i in range(7)] + ["prior_refunds", "ticket_reopened"]
X = np.column_stack([rng.normal(0.42 * y, 1) for _ in range(7)] + [rng.normal(0.9 * y, 1)] +
                    [(rng.random(N) < np.where(y == 1, 0.70, 0.07)).astype(float)])
# when each feature becomes available, relative to the decision (minutes; negative = before the decision)
avail = np.column_stack([np.full(N, -60.0)] * 8 + [rng.uniform(300, 5000, N)])   # reopen happens days later
def fit_auc(cols):
    tr, te = slice(0, 30_000), slice(30_000, N)
    A = np.column_stack([np.ones(N), X[:, cols]])
    w = np.zeros(A.shape[1])
    for _ in range(12):                                      # IRLS for logistic regression
        p = 1 / (1 + np.exp(-A[tr] @ w)); W = p * (1 - p)
        w += np.linalg.solve(A[tr].T @ (A[tr] * W[:, None]) + 1e-6 * np.eye(len(w)), A[tr].T @ (y[tr] - p))
    return auc(y[te], A[te] @ w)
all_cols = list(range(9)); no_leak = list(range(8))
a_all, a_clean = fit_auc(all_cols), fit_auc(no_leak)
print(f"AUC all features = {a_all:.3f}; without ticket_reopened = {a_clean:.3f}; drop = {a_all - a_clean:.3f}")
assert abs(a_all - 0.93) < 0.015 and abs(a_clean - 0.84) < 0.015
# test 1: single-feature AUC (flags suspicious, does not prove leakage)
single = {n: auc(y, X[:, i]) for i, n in enumerate(names)}
for n, v in sorted(single.items(), key=lambda kv: -kv[1])[:3]: print(f"single-feature AUC {n:16} {v:.3f}")
# test 2: drop-one ablation (how much does each feature carry on top of the rest)
drops = {n: a_all - fit_auc([c for c in all_cols if c != i]) for i, n in enumerate(names)}
worst = max(drops, key=drops.get)
print(f"largest drop-one loss: {worst} ({drops[worst]:.3f}); next: {sorted(drops.values())[-2]:.3f}")
assert worst == "ticket_reopened" and drops[worst] > 2.5 * sorted(drops.values())[-2]
# test 3: the definitive check, availability time versus decision time (the automatic gate)
late = {n: float((avail[:, i] > 0).mean()) for i, n in enumerate(names)}
flagged = [n for n, v in late.items() if v > 0.01]
print("features with values arriving after the decision:", flagged)
assert flagged == ["ticket_reopened"]
# prior_refunds is strong on its own but legitimate: test 1 alone would wrongly accuse it too
assert single["prior_refunds"] > 0.68 and "prior_refunds" not in flagged
# arithmetic quoted in the text
assert round(0.93 - 0.81, 2) == 0.12 and round(0.93 - 0.84, 2) == 0.09 and round(0.84 - 0.81, 2) == 0.03
print("offline minus online: 0.12 before the fix; 0.03 remains after the fix and still needs an explanation")
