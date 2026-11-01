# Q13: difference-in-differences for a one-city price change (illustrative numbers)
import numpy as np

# 1) The arithmetic from the prompt
pre_t, post_t = 2.0, 2.3
pre_c, post_c = 2.0, 2.2
did = (post_t - pre_t) - (post_c - pre_c)
print(f"naive before/after in treated city: {(post_t - pre_t) / pre_t:+.0%}")
print(f"DiD = {did:.2f} orders per user per week = {did / pre_t:+.1%} of the baseline")
assert abs(did - 0.1) < 1e-9 and abs(did / pre_t - 0.05) < 1e-9

# 2) Simulated weekly panel: 8 pre weeks, 4 post weeks, 1 treated + 5 comparison cities
rng = np.random.default_rng(13)
weeks, pre_w = 12, 8
trend = np.linspace(0, 0.2, weeks)           # shared market trend (+0.2 over 12 weeks)

def panel(extra_slope_treated=0.0, true_effect=0.10, noise=0.03):
    cities = []
    for k in range(6):
        y = 2.0 + trend + rng.normal(0, noise, weeks)
        if k == 0:
            y = y + np.linspace(0, extra_slope_treated, weeks)
            y[pre_w:] += true_effect
        cities.append(y)
    return np.array(cities)

def did_est(Y, treated=0):
    ctrl = [i for i in range(len(Y)) if i != treated]
    t = Y[treated, pre_w:].mean() - Y[treated, :pre_w].mean()
    c = Y[ctrl, pre_w:].mean() - Y[ctrl, :pre_w].mean()
    return t - c

def pretrend_gap(Y, treated=0):
    """slope of (treated - mean control) over the pre weeks, per week"""
    ctrl = [i for i in range(len(Y)) if i != treated]
    gap = Y[treated, :pre_w] - Y[ctrl, :pre_w].mean(axis=0)
    return np.polyfit(np.arange(pre_w), gap, 1)[0]

# parallel trends hold
ests, slopes = [], []
for _ in range(2000):
    Y = panel(); ests.append(did_est(Y)); slopes.append(pretrend_gap(Y))
print(f"parallel trends: DiD mean {np.mean(ests):.3f} (truth 0.100), sd {np.std(ests):.3f}, pre-trend slope sd {np.std(slopes):.4f}")
assert abs(np.mean(ests) - 0.10) < 0.005

# treated city was already growing faster (violation)
ests2, slopes2 = [], []
for _ in range(2000):
    Y = panel(extra_slope_treated=0.12); ests2.append(did_est(Y)); slopes2.append(pretrend_gap(Y))
print(f"trend violated:   DiD mean {np.mean(ests2):.3f} (truth 0.100), pre-trend slope mean {np.mean(slopes2):.4f} per week")
assert np.mean(ests2) > 0.15 and np.mean(slopes2) > 0.005

# 3) Placebo (permutation) inference with ONE treated city: pretend each comparison city was treated
Y = panel()
real = did_est(Y, 0)
placebo = [did_est(Y, k) for k in range(1, 6)]
print(f"real DiD {real:.3f}; placebo DiDs {np.round(placebo, 3)}")
rank = 1 + sum(abs(p) >= abs(real) for p in placebo)
print(f"rank of real among 6 = {rank}; smallest possible permutation p = 1/6 = {1/6:.3f}")
assert rank == 1
print("all asserts passed")
