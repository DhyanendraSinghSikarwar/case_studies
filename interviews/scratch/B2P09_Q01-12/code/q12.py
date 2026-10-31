# pass@k: Codex-paper unbiased estimator, brute-force check, bias of 1-(1-p_hat)^k, and pass^k.
import itertools, random
from math import comb
import numpy as np
random.seed(0)

def pass_at_k(n, c, k):                # numerically stable form (the Codex paper's Figure 3 script has this shape)
    if n - c < k: return 1.0
    return 1.0 - np.prod(1.0 - k / np.arange(n - c + 1, n + 1))
def pass_at_k_closed(n, c, k): return 1.0 - comb(n - c, k) / comb(n, k)
def pass_at_k_brute(n, c, k):          # average over every size-k subset of the n samples
    labels = [1]*c + [0]*(n - c)
    subs = list(itertools.combinations(range(n), k))
    return sum(any(labels[i] for i in s) for s in subs) / len(subs)

worst = 0
for n in range(1, 9):
    for c in range(n + 1):
        for k in range(1, n + 1):
            a, b, d = pass_at_k(n, c, k), pass_at_k_closed(n, c, k), pass_at_k_brute(n, c, k)
            worst = max(worst, abs(a - b), abs(a - d))
print("max abs diff, stable vs closed vs brute force (all n<=8):", f"{worst:.1e}")
print("n=10, c=3: pass@1 =", round(pass_at_k(10, 3, 1), 3), "pass@5 =", round(pass_at_k(10, 3, 5), 3))

# Bias: a problem whose TRUE per-sample pass rate is p. Draw n samples, estimate pass@k two ways.
p, n, k = 0.3, 10, 5
true = 1 - (1 - p)**k
pmf = [comb(n, c) * p**c * (1 - p)**(n - c) for c in range(n + 1)]
e_unb = sum(w * pass_at_k(n, c, k) for c, w in enumerate(pmf))
e_naive = sum(w * (1 - (1 - c / n)**k) for c, w in enumerate(pmf))
print(f"true pass@{k} = {true:.4f} | E[unbiased] = {e_unb:.4f} | E[1-(1-p_hat)^k] = {e_naive:.4f} (exact expectation over c)")

# pass@k vs pass^k on one problem with per-sample success 0.75, k=3 (independent trials assumed)
q = 0.75
print(f"per-trial {q}: pass@3 = {1-(1-q)**3:.3f}, pass^3 = {q**3:.3f}")
# pass^k estimator from n samples, c correct: C(c,k)/C(n,k); and an aggregate over 3 toy problems
def pass_hat_k(n, c, k): return comb(c, k) / comb(n, k)
problems = [(10, 10), (10, 7), (10, 2)]      # (n, c) -- synthetic
for k in (1, 3):
    print(f"k={k}: mean pass@k = {np.mean([pass_at_k(n, c, k) for n, c in problems]):.3f}"
          f" | mean pass^k = {np.mean([pass_hat_k(n, c, k) for n, c in problems]):.3f}")
