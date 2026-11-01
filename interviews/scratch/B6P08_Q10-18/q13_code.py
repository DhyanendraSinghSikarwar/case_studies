import numpy as np

assert 52 - 35 == 17 and round(52 / 35, 2) == 1.49    # absolute points, relative growth
rng = np.random.default_rng(13)
N, weeks, imps = 1000, 6, 200_000                    # 1,000 items, 200k impressions a week
top = N // 100                                       # top 1% = 10 items
quality = rng.beta(400, 6000, N)                         # TRUE click appeal, independent of popularity
quality /= quality.mean() / 0.06                     # average CTR about 6%
pop = rng.gamma(0.1, 1.0, N)                         # initial popularity (clicks last week)
EXPLORE = 0.02                                       # 2% of impressions shown uniformly at random (logged)

def week(pop, power=1.12):
    p = pop ** power; p /= p.sum()
    p = (1 - EXPLORE) * p + EXPLORE / N              # mix random exposure
    shown = rng.multinomial(imps, p)
    clicks = rng.binomial(shown, quality)
    return shown, clicks, p

shares, ctrs = [], []
for w in range(weeks):
    shown, clicks, p = week(pop)
    s = np.sort(shown)[::-1][:top].sum() / imps
    shares.append(s); ctrs.append(clicks.sum() / imps)
    # explore slice only: propensity is 1/N for everyone
    pop = clicks + 1.0                               # retrain: "popularity" = last week's clicks
print("top-1% impression share by week:", [round(float(x) * 100) for x in shares])
print("page CTR by week (%):", [round(float(x) * 100, 2) for x in ctrs])
assert shares[-1] > shares[0] + 0.10                 # concentration rises by >10 points
assert max(ctrs) - min(ctrs) < 0.004                 # page CTR roughly flat (under 0.4 points)

# Proof with the data: naive CTR (clicks/impressions) of top items vs their CTR in the random slice
shown, clicks, p = week(pop)
ids = np.argsort(-shown)[:top]
naive = clicks[ids].sum() / shown[ids].sum()
exp_n = int(imps * EXPLORE)
ex_shown = rng.multinomial(exp_n, np.full(N, 1 / N))     # re-draw the random slice for these items
ex_clicks = rng.binomial(ex_shown, quality)
explore_ctr_top = ex_clicks[ids].sum() / ex_shown[ids].sum()
explore_ctr_all = ex_clicks.sum() / ex_shown.sum()
true_top = quality[ids].mean()
print("top items: naive CTR", round(float(naive) * 100, 2), "% | random-slice CTR", round(float(explore_ctr_top) * 100, 2), "% | all items random-slice", round(float(explore_ctr_all) * 100, 2), "% | true mean quality of those items", round(float(true_top) * 100, 2), "%")
assert abs(explore_ctr_all - quality.mean()) < 0.003   # random slice is an unbiased view of the catalogue
# Exposure per item in the final week: top items vs the rest
print("avg impressions per top item:", int(shown[ids].mean()), "| per other item:", int(np.delete(shown, ids).mean()))
assert shown[ids].mean() > 10 * np.delete(shown, ids).mean()
# Metric to track: top-1% exposure share + Gini of exposure
x = np.sort(shown); g = (2 * np.arange(1, N + 1) - N - 1) @ x / (N * x.sum())
print("final-week exposure Gini:", round(float(g), 2))
assert 0 < g < 1
