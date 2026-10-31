# SYNTHETIC drift demo. (1) input-length drift: KS (two implementations) and PSI. (2) a mock judge's bias on a "hallucination rate" proxy.
import math
import numpy as np
rng = np.random.default_rng(11)
def ks_fast(a, b):
    a, b = np.sort(a), np.sort(b); z = np.concatenate([a, b])
    return np.max(np.abs(np.searchsorted(a, z, side="right") / len(a) - np.searchsorted(b, z, side="right") / len(b)))
def ks_brute(a, b):                       # direct definition, O(n*m)
    return max(abs((a <= t).mean() - (b <= t).mean()) for t in np.concatenate([a, b]))
def ks_p(d, n, m):                        # asymptotic Kolmogorov tail
    en = math.sqrt(n * m / (n + m)); lam = (en + 0.12 + 0.11 / en) * d
    return min(1.0, 2 * sum((-1) ** (j - 1) * math.exp(-2 * j * j * lam * lam) for j in range(1, 101)))
def psi(a, b, bins=10):
    edges = np.quantile(a, np.linspace(0, 1, bins + 1)); edges[0], edges[-1] = -np.inf, np.inf
    pa = np.histogram(a, edges)[0] / len(a); pb = np.histogram(b, edges)[0] / len(b)
    pa, pb = np.clip(pa, 1e-4, None), np.clip(pb, 1e-4, None)
    return float(np.sum((pb - pa) * np.log(pb / pa)))
ref = rng.lognormal(4.0, 0.5, 2000)                         # last month's prompt lengths (tokens), SYNTHETIC
same = rng.lognormal(4.0, 0.5, 500)                         # this week, no change
shift = np.concatenate([rng.lognormal(4.0, 0.5, 350), rng.lognormal(5.2, 0.4, 150)])   # 30% new long-document queries
small, big = ref[:200], ref[200:400]
assert abs(ks_fast(small, big) - ks_brute(small, big)) < 1e-12
print("KS fast == brute force on a check sample: OK")
for name, cur in (("no change", same), ("30% long-doc queries", shift)):
    d = ks_fast(ref, cur)
    print(f"{name:22} KS={d:.3f} p~{ks_p(d, len(ref), len(cur)):.3g}  PSI={psi(ref, cur):.3f}")
# (2) proxy bias. Mock judge flags a bad answer with prob TPR=0.80, flags a good answer with prob FPR=0.10 (ASSUMED).
TPR, FPR = 0.80, 0.10
print("true bad rate -> expected judged rate (=FPR+(TPR-FPR)*q) -> simulated -> corrected (Rogan-Gladen)")
for q in (0.05, 0.10, 0.15):
    N = 20000
    bad = rng.random(N) < q
    flag = np.where(bad, rng.random(N) < TPR, rng.random(N) < FPR)
    obs = flag.mean(); corr = (obs - FPR) / (TPR - FPR)
    print(f"  q={q:.2f}  expected={FPR + (TPR - FPR) * q:.3f}  simulated={obs:.3f}  corrected={corr:.3f}")
# detection power of a sampled judge: can n=200 sampled traces see 10% -> 15% true bad rate through this noisy judge?
def z_detect(n, q0, q1, trials=2000):
    p0, p1 = FPR + (TPR - FPR) * q0, FPR + (TPR - FPR) * q1; hits = 0
    for _ in range(trials):
        a = rng.binomial(n, p0); b = rng.binomial(n, p1)
        pp = (a + b) / (2 * n); se = math.sqrt(2 * pp * (1 - pp) / n)
        hits += (b / n - a / n) / se > 1.645
    return hits / trials
for n in (200, 1000, 5000):
    print(f"power (one-sided z, alpha .05) to see judged-bad 10%->15% true with {n} judged traces per period: {z_detect(n, .10, .15):.2f}")
