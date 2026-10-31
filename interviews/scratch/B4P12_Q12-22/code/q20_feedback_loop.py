"""Q20: popularity feedback loop. A daily retrain on clicks the model itself caused locks onto old winners; a 5% unpersonalised
holdout (random items) gives a clean estimate. Sandbox simulation, invented numbers, seeded."""
import numpy as np
rng = np.random.default_rng(20)
N, K, DAYS, IMPR, HOLD, CHURN = 2000, 10, 40, 100_000, 0.10, 0.04
appeal = rng.beta(1.2, 18, N)                      # true click probability per item (hidden from the model)
age = np.zeros(N)
clicks = np.zeros(N); shows = np.zeros(N); hc_ = np.zeros(N); hs_ = np.zeros(N)
for _ in range(20_000):                            # day-0 seed: random exposure
    i = rng.integers(N); shows[i] += 1; clicks[i] += rng.random() < appeal[i]
POS = 1 / np.log2(np.arange(2, K + 2)); POS /= POS.sum()
print(f"{'day':>3s} {'main CTR':>9s} {'holdout CTR of model slate':>27s} {'best well-measured holdout items':>33s} {'ratio':>6s} {'fresh share main/holdout':>26s}")
rows = []
for day in range(DAYS + 1):
    if day:
        new = rng.choice(N, int(N * CHURN), replace=False)       # catalogue churn: new items arrive with fresh appeal
        appeal[new] = rng.beta(1.2, 18, len(new)); age[new] = 0
        for a in (clicks, shows, hc_, hs_): a[new] = 0
        age[np.setdiff1d(np.arange(N), new)] += 1
    top = np.argsort(-clicks)[:K]                                # naive model: rank by total clicks (rich get richer)
    n_h = int(IMPR * HOLD); n_m = IMPR - n_h
    it = top[rng.choice(K, size=n_m, p=POS)]
    c = rng.random(n_m) < np.minimum(appeal[it] * 2, 1)
    np.add.at(shows, it, 1); np.add.at(clicks, it, c)
    hi = rng.integers(N, size=n_h); hc = rng.random(n_h) < appeal[hi]
    np.add.at(hs_, hi, 1); np.add.at(hc_, hi, hc); np.add.at(shows, hi, 1); np.add.at(clicks, hi, hc)
    ok = hs_ >= 30
    hctr = np.where(hs_ > 0, hc_ / np.maximum(hs_, 1), 0)
    slate_est = hctr[top][ok[top]].mean() if ok[top].any() else float("nan")
    best = np.sort(hctr[ok])[-K:].mean() if ok.sum() >= K else float("nan")
    ratio = slate_est / best
    fresh_main = (age[it] < 7).mean(); fresh_hold = (age[hi] < 7).mean()
    rows.append((day, c.mean(), slate_est, best, ratio, fresh_main, fresh_hold))
    if day in (5, 10, 15, 20, 30, 40):
        print(f"{day:3d} {c.mean():9.3f} {slate_est:27.3f} {best:33.3f} {ratio:6.2f} {fresh_main:12.1%} /{fresh_hold:7.1%}")
late = [r for r in rows if r[0] >= 15]
print("\nmain-traffic CTR over days 15-40: min %.3f max %.3f (the in-loop metric looks fine)" % (min(r[1] for r in late), max(r[1] for r in late)))
print("holdout ratio over days 15-40: mean %.2f  -> ALERT rule: ratio < 0.8 for 5 days" % np.mean([r[4] for r in late]))
assert np.mean([r[4] for r in late]) < 0.8 and np.mean([r[5] for r in late]) < 0.1
