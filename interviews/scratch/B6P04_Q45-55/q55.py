# Q55: uplift model "validated" by comparing treated top 20% with untreated rest (illustrative simulation)
import numpy as np
rng = np.random.default_rng(55)
N = 1_000_000; TOP = 200_000
print("naive claim from stated counts: top 20% =", TOP, " rest =", N - TOP)
# Scenario 1: the model really ranks by who buys anyway (propensity), true coupon uplift is ZERO for everyone
score = rng.random(N); top = np.zeros(N, bool); top[np.argsort(-score)[:TOP]] = True
base = np.where(top, 0.0575, 0.05)              # top users already convert a bit more
conv = rng.random(N) < base                      # coupon changes nothing
naive = conv[top].mean() / conv[~top].mean() - 1
print("coupon has NO effect, yet naive comparison reads", f"{100*naive:+.1f}%", " (top converts", round(conv[top].mean(), 4), "vs rest", round(conv[~top].mean(), 4), ")")
assert abs(naive - 0.15) < 0.02
# Scenario 2: randomised evaluation sample. Model has real uplift signal: uplift rises with score decile
M = 400_000
sc = rng.random(M); dec = np.minimum((sc * 10).astype(int), 9)          # decile 9 = model's top
base = 0.05 + 0.002 * (9 - dec)                        # high-score users are NOT the highest-baseline here
uplift = np.where(dec == 9, 0.020, np.where(dec == 8, 0.012, np.where(dec == 7, 0.006, 0.0)))
treat = rng.random(M) < 0.5                            # coupon assigned by coin flip, ignoring the score
y = rng.random(M) < base + uplift * treat
print("decile | n | treated conv | control conv | uplift (pts)")
up = []
for d in range(9, -1, -1):
    m = dec == d; t, c = y[m & treat].mean(), y[m & ~treat].mean(); up.append(t - c)
    print(f"{d:>6} | {m.sum():>6} | {t:.4f} | {c:.4f} | {100*(t-c):+.2f}")
# uplift (Qini-style) curve: cumulative incremental conversions if we treat the top k deciles
inc = []
tot = 0.0
for d in range(9, -1, -1):
    m = dec == d
    n_t, n_c = (m & treat).sum(), (m & ~treat).sum()
    tot += (y[m & treat].sum() / n_t - y[m & ~treat].sum() / n_c) * m.sum()
    inc.append(tot)
print("incremental conversions per 1,000,000 users if we treat top k deciles (scaled):",
      [round(v * 1_000_000 / M) for v in inc])
assert up[0] > up[2] > 0.0 and up[0] > 0.012 and abs(up[5]) < 0.006
# hold-out sizing: top 20% (200,000) with 10% randomly held out
n_h = 20_000; n_t = 180_000; p = 0.0575
se = np.sqrt(p*(1-p)*(1/n_t + 1/n_h))
print("SE of treated-minus-holdout with a 10% holdout of the top 200,000:", round(100*se, 3), "points -> detectable effect at 80% power about", round(100*2.8*se, 2), "points")
assert 0.0015 < se < 0.002
