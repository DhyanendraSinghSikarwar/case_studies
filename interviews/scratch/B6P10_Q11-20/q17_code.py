import math

# Prompt arithmetic
zones, interval_s, base, cap_step = 100, 60, 100.0, 0.20
decisions = zones * (24 * 3600 // interval_s)
assert decisions == 144_000
print("price decisions a day:", decisions)
price5 = base * (1 + cap_step) ** 5
assert abs(price5 - 248.832) < 1e-9
print("fare after 5 consecutive +20% steps:", round(price5, 3), "| multiple of base:", round(price5 / base, 3))
# The per-update cap limits speed, not level: how long to reach 2x or 3x base?
for mult in (2, 3):
    steps = math.ceil(math.log(mult) / math.log(1 + cap_step))
    print(f"steps to reach at least {mult}x base: {steps} (= {steps} minutes at a 60 s interval); price after: {base * 1.2 ** steps:.2f}")
assert math.ceil(math.log(2) / math.log(1.2)) == 4 and abs(100 * 1.2 ** 4 - 207.36) < 1e-9
assert math.ceil(math.log(3) / math.log(1.2)) == 7
# Step down is not the mirror: -20% three times from 207.36
down = 207.36 * 0.8 ** 3
print("207.36 after three -20% steps:", round(down, 2))
assert abs(down - 106.16832) < 1e-6

# Guardrail check on a noisy raw price proposal: smoothing plus clip to +-20% and absolute cap
import numpy as np
rng = np.random.default_rng(17)
raw = base * np.exp(np.cumsum(rng.normal(0.08, 0.15, 30)))        # volatile model proposals (illustrative)
cap_abs = 2.0 * base                                                # illustrative absolute cap (business decision)
p, path = base, []
for r in raw:
    step = min(max(r, p * (1 - cap_step)), p * (1 + cap_step))
    p = min(step, cap_abs)
    path.append(p)
path = np.array(path)
ratios = path[1:] / path[:-1]
assert ratios.max() <= 1.2 + 1e-9 and ratios.min() >= 0.8 - 1e-9 and path.max() <= cap_abs + 1e-9
print("max one-step change:", round(float(ratios.max()), 3), "| max price:", round(float(path.max()), 2), "| minutes at cap:", int((path >= cap_abs - 1e-9).sum()))
