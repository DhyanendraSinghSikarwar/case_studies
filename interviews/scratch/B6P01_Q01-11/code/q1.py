# Q1: is the DAU drop real, and where is it? (illustrative numbers)
import numpy as np

two_weeks_ago, last_week, this_week = 1.00, 0.98, 0.90   # million DAU
wow = this_week / last_week - 1
vs2w = this_week / two_weeks_ago - 1
print(f"WoW change: {wow:.1%}   vs two weeks ago: {vs2w:.1%}")
assert round(wow, 3) == -0.082 and round(vs2w, 3) == -0.100

# Noise check: 8 earlier weeks of weekly DAU with ~1% natural wobble (seeded, illustrative)
rng = np.random.default_rng(7)
hist = 1.00 * (1 + rng.normal(0, 0.01, 8))
wow_hist = hist[1:] / hist[:-1] - 1
sd = wow_hist.std(ddof=1)
z = wow / sd
print(f"history WoW sd: {sd:.2%}   this week's z: {z:.1f}")
assert abs(z) > 3

# Decomposition by platform (million DAU)
seg = {"Android": (0.45, 0.44, 0.37), "iOS": (0.40, 0.40, 0.40), "Web": (0.15, 0.14, 0.13)}
tot_change = this_week - last_week
print(f"{'segment':8} {'last':>5} {'this':>5} {'delta':>6} {'share of drop':>14}")
for k, (a, b, c) in seg.items():
    d = c - b
    print(f"{k:8} {b:5.2f} {c:5.2f} {d:6.2f} {d / tot_change * 100 + 0.0:13.1f}%")
assert abs(sum(v[0] for v in seg.values()) - 1.00) < 1e-9
assert abs(sum(v[1] for v in seg.values()) - 0.98) < 1e-9
assert abs(sum(v[2] for v in seg.values()) - 0.90) < 1e-9
assert round((0.37 - 0.44) / tot_change, 3) == 0.875
