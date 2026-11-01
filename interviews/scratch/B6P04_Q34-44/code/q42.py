# Q42: CUPED with a post-treatment covariate (first 3 days of the experiment). Illustrative, seeded.
import numpy as np

rho = 0.9
print("variance kept with covariate correlation 0.9:", round(1 - rho**2, 2), " -> SE shrinks to", round(np.sqrt(1 - rho**2), 2), "of its size")
assert round(1 - rho**2, 2) == 0.19 and round(np.sqrt(1 - rho**2), 2) == 0.44

rng = np.random.default_rng(42)
n = 50_000
TAU_Y, TAU_X = 2.0, 1.5     # true effect on 28-day sessions; treatment also raises early (3-day) sessions by 1.5

def sim(n, reps):
    out = {"naive": [], "bad": [], "good": []}
    se = {"naive": [], "bad": [], "good": []}
    for _ in range(reps):
        T = rng.integers(0, 2, n)
        L = rng.normal(100, 20, n)                           # latent engagement
        pre = L + rng.normal(0, 6, n)                        # sessions in the 28 days BEFORE the test
        early = L + rng.normal(0, 6, n) + TAU_X * T          # sessions in the first 3 days (post-treatment)
        Y = L + rng.normal(0, 6, n) + TAU_Y * T              # 28-day sessions
        for name, x in (("naive", None), ("bad", early), ("good", pre)):
            if x is None:
                a, b = Y[T == 1], Y[T == 0]
                est = a.mean() - b.mean(); s = np.sqrt(a.var(ddof=1) / len(a) + b.var(ddof=1) / len(b))
            else:
                th = np.cov(Y, x)[0, 1] / x.var(ddof=1)      # pooled theta, the standard CUPED recipe
                Z = Y - th * (x - x.mean())
                a, b = Z[T == 1], Z[T == 0]
                est = a.mean() - b.mean(); s = np.sqrt(a.var(ddof=1) / len(a) + b.var(ddof=1) / len(b))
            out[name].append(est); se[name].append(s)
    return {k: (np.mean(v), np.mean(se[k]), np.mean([abs(e - TAU_Y) < 1.96 * s for e, s in zip(v, se[k])])) for k, v in out.items()}

res = sim(n, 100)
Tt = rng.integers(0, 2, n); L = rng.normal(100, 20, n)
print("corr(early, 28-day) in the simulation ~",
      round(np.corrcoef(L + rng.normal(0, 6, n), L + rng.normal(0, 6, n))[0, 1], 2))
print(f"true effect on 28-day sessions: {TAU_Y}")
for k, (m, s, cov) in res.items():
    print(f"{k:6s} mean estimate {m:5.2f}   mean SE {s:.3f}   95% CI covers the truth in {cov:.0%} of runs")
assert abs(res["naive"][0] - TAU_Y) < 0.1 and abs(res["good"][0] - TAU_Y) < 0.1
assert res["bad"][0] < TAU_Y - 0.8                           # biased toward zero
assert res["bad"][1] < res["naive"][1] and res["good"][1] < res["naive"][1]
assert res["bad"][2] < 0.5 and res["naive"][2] > 0.9
