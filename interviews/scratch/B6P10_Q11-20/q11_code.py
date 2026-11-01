import math
import numpy as np

# Sizing (from the question; peak figures are the question's, 'full load' means no headroom)
rps, cands, kept, per_server = 50_000, 300, 40, 50_000
no_pre = rps * cands
with_pre = rps * kept
assert no_pre == 15_000_000 and with_pre == 2_000_000
s_no, s_pre = math.ceil(no_pre / per_server), math.ceil(with_pre / per_server)
assert (s_no, s_pre) == (300, 40)
# With 30% headroom (my assumption) the fleet is larger; the prefilter itself costs extra
s_pre_hr = math.ceil(with_pre / (per_server * 0.70))
assert s_pre_hr == 58
print("predictions/s without prefilter:", no_pre, "servers:", s_no)
print("predictions/s with prefilter   :", with_pre, "servers:", s_pre, "| with 30% headroom:", s_pre_hr)
print("reduction factor:", no_pre / with_pre)

# Calibration: negatives down-sampled at keep rate w shifts predictions up; undo with p = p'w/(1-p'+p'w)
rng = np.random.default_rng(11)
n = 2_000_000
true_p = rng.beta(1, 49, n)                      # mean CTR about 2%
click = rng.random(n) < true_p
w = 0.1
keep = click | (rng.random(n) < w)               # keep all clicks, 10% of non-clicks
p_shift = true_p / (true_p + (1 - true_p) * w)   # what a perfect model fits on the sampled data
p_fix = p_shift * w / (1 - p_shift + p_shift * w)
assert np.allclose(p_fix, true_p)
print("mean true CTR:", round(float(true_p.mean()), 4),
      "| mean pred on sampled data:", round(float(p_shift[keep].mean()), 4),
      "| after correction:", round(float(p_fix.mean()), 4))
assert p_shift.mean() > 2 * true_p.mean()

# Prefilter recall: cheap score correlated with true value; keep top 40 of 300; how many of the true top 5 survive?
trials, hit = 2000, 0
for _ in range(trials):
    v = rng.normal(size=300)
    cheap = 0.7 * v + math.sqrt(1 - 0.49) * rng.normal(size=300)
    top5 = set(np.argsort(-v)[:5]); kept40 = set(np.argsort(-cheap)[:40])
    hit += len(top5 & kept40)
recall = hit / (trials * 5)
print("share of true top-5 ads kept by a 0.7-correlation prefilter (illustrative):", round(recall, 3))
assert 0.6 < recall < 0.95
