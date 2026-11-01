# Q13: undersampling and probability correction (illustrative numbers)
import numpy as np
rng = np.random.default_rng(13)
# arithmetic from the prompt
fraud, legit, beta = 10_000, 990_000, 0.10
kept = fraud + beta * legit
print(f"training rows {kept:,.0f}, training fraud share {fraud / kept:.2%}, true base rate {fraud / (fraud + legit):.2%}")
assert kept == 109_000 and round(fraud / kept, 3) == 0.092
def correct(ps, beta): return beta * ps / (beta * ps + (1 - ps))
p = correct(0.50, beta); print("score 0.50 ->", round(p, 4)); assert round(p, 4) == 0.0909
print("odds view: 0.50 is odds 1.0; times beta 0.1 gives odds 0.1; prob", round(0.1 / 1.1, 4))
# base-rate shift check: mean raw score level versus the 1% truth

# simulation: one feature, true model known, population with a 1% fraud rate
def sig(z): return 1 / (1 + np.exp(-z))
n = 1_000_000
x = rng.normal(size=n)
lo, hi = -10.0, 0.0
for _ in range(60):
    mid = (lo + hi) / 2
    if sig(mid + 2 * x).mean() > 0.01: hi = mid
    else: lo = mid
b0 = (lo + hi) / 2
y = rng.random(n) < sig(b0 + 2 * x)
print("simulated population fraud rate:", f"{y.mean():.3%}")
keep = y | (rng.random(n) < beta)
xs, ys = x[keep], y[keep].astype(float)
print("training rows:", keep.sum(), " fraud share:", f"{ys.mean():.2%}")
w = np.zeros(2); X = np.c_[np.ones(len(xs)), xs]
for _ in range(25):                                    # Newton / IRLS
    pr = sig(X @ w); g = X.T @ (ys - pr); H = (X * (pr * (1 - pr))[:, None]).T @ X
    w += np.linalg.solve(H, g)
print("fitted intercept", round(w[0], 3), " true intercept", round(b0, 3), " shift", round(w[0] - b0, 3), " ln(1/beta)=", round(np.log(1 / beta), 3))
assert abs((w[0] - b0) - np.log(1 / beta)) < 0.25 and abs(w[1] - 2) < 0.2
raw = sig(w[0] + w[1] * x); cor = correct(raw, beta)
print(f"mean score on the full population: raw {raw.mean():.3%}  corrected {cor.mean():.3%}  truth {y.mean():.3%}")
assert raw.mean() > 0.05 and abs(cor.mean() - y.mean()) < 0.0015
# calibration by raw-score band, full population
edges = [0, 0.1, 0.3, 0.5, 0.7, 0.9, 1.0]
print("band        n        raw_mean  corrected_mean  actual")
for a, b in zip(edges[:-1], edges[1:]):
    m = (raw >= a) & (raw < b + (1e-12 if b == 1 else 0))
    if m.sum() > 200:
        print(f"{a:.1f}-{b:.1f}  {m.sum():9,d}   {raw[m].mean():.3f}     {cor[m].mean():.3f}         {y[m].mean():.3f}")
m = (raw > 0.45) & (raw < 0.55)
print("raw scores near 0.50: corrected", round(cor[m].mean(), 3), " actual fraud rate", round(y[m].mean(), 3))
assert abs(cor[m].mean() - y[m].mean()) < 0.01 and abs(y[m].mean() - 0.0909) < 0.01
