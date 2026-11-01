import numpy as np
sprint, per_change, changes = 20, 3, 3
lost = per_change * changes
print(f"total: {changes} relabel-and-retrain cycles x {per_change} days = {lost} days = {lost/sprint:.0%} of {sprint}")
assert lost == 9 and lost/sprint == 0.45
# three definitions; if the first build was planned work anyway, only two cycles are avoidable
avoidable = per_change * 2
print(f"if the first definition was planned work, avoidable loss = {avoidable} days = {avoidable/sprint:.0%}")
assert avoidable == 6 and avoidable/sprint == 0.30
# build once, label many: one pass over a gap table gives all three labels (illustrative simulation)
rng = np.random.default_rng(26)
gap = rng.lognormal(mean=3.2, sigma=1.0, size=100_000)   # days of inactivity at snapshot, illustrative
rates = {d: float((gap >= d).mean()) for d in (30, 60, 90)}
print({d: f"{r:.1%}" for d, r in rates.items()})
assert rates[30] > rates[60] > rates[90]
# change control: each extra definition requested after the sprint plan costs 3 days; a parametrised label costs 0.5 day
param_cost = 0.5
print(f"three definitions with a parametrised label: {3*param_cost} days instead of {lost}")
assert 3*param_cost == 1.5
