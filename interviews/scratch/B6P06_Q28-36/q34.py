# Illustrative: model forecast 10.5M, target 12M, assumed forecast error sd 0.8M (from a backtest, invented).
from statistics import NormalDist
model, target, sd = 10.5, 12.0, 0.8
uplift = target - model
print(f"gap {uplift:.1f}M = {uplift/model:.1%} of the model figure, {uplift/target:.1%} of target")
assert uplift == 1.5 and round(uplift / model, 3) == 0.143 and round(uplift / target, 3) == 0.125
N = NormalDist(model, sd)
p_hit = 1 - N.cdf(target)
p10, p90 = N.inv_cdf(0.10), N.inv_cdf(0.90)
print(f"P10 {p10:.2f}  P50 {model:.2f}  P90 {p90:.2f}  P(actual >= 12) = {p_hit:.1%}")
assert round(p10, 2) == 9.47 and round(p90, 2) == 11.53 and 0.02 < p_hit < 0.04
# z-score of the target
print("target is", round(uplift / sd, 2), "standard deviations above the model")
assert round(uplift / sd, 2) == 1.88
# What would make 12 a P50? Needed pipeline uplift on the base: 14.3% across the board.
# Illustrative commit/stretch view: commit at P20, stretch = target.
p20 = N.inv_cdf(0.20)
print(f"commit (P20) {p20:.2f}, model {model}, target {target}, risk gap to target {target-model:.1f}")
assert round(p20, 2) == 9.83
# If sales really lift by 5% of the model (an upside scenario), P(hit)
up = model * 1.05
print(f"model +5% -> {up:.2f}; P(>=12) = {1-NormalDist(up, sd).cdf(target):.1%}")
assert round(up, 2) == 11.03
