# Q39: three changes in one week, conversion metric -5% (illustrative numbers, hand-checkable)
import numpy as np

# Segment table: (share, conversion %) before and after
before = {"existing iOS": (0.50, 4.40), "existing Android": (0.50, 3.60)}
after = {"existing iOS": (0.35, 4.40), "existing Android": (0.35, 3.50), "new campaign users": (0.30, 3.45)}
tot = lambda d: sum(s * r for s, r in d.values())
b, a = tot(before), tot(after)
print(f"overall conversion {b:.2f}% -> {a:.2f}%  ({a / b - 1:+.1%})")
assert round(b, 2) == 4.00 and round(a, 2) == 3.80 and round(a / b - 1, 3) == -0.05

# Decomposition: existing-user rate change + new-user mix effect
ex_b = (0.50 * 4.40 + 0.50 * 3.60) / 1.0
ex_a = (0.35 * 4.40 + 0.35 * 3.50) / 0.70
new = 3.45; s_new = 0.30
rate_effect = ex_a - ex_b                       # existing users, same people-type, before vs after
mix_effect = s_new * (new - ex_a)               # replacing 30% of traffic by users who convert lower
print(f"existing-user rate effect {rate_effect:+.3f} pp, new-user mix effect {mix_effect:+.3f} pp, sum {rate_effect + mix_effect:+.3f} pp")
assert abs(rate_effect + mix_effect - (a - b)) < 1e-9
assert abs(rate_effect - (-0.05)) < 1e-9 and abs(mix_effect - (-0.15)) < 1e-9
print(f"share of the drop: mix {mix_effect / (a - b):.0%}, existing-user rate {rate_effect / (a - b):.0%}")

# Where is the existing-user rate effect? By platform: iOS flat, Android -0.10 pp
android_drop = 3.50 - 3.60
print(f"existing Android change {android_drop:+.2f} pp; existing iOS change {4.40 - 4.40:+.2f} pp")
assert abs(0.5 * android_drop - rate_effect) < 1e-9     # all of it sits in Android

# Schema suspect: a feature became null for part of Android. Conversion with feature vs null rows
null_share, rate_null, rate_ok = 0.20, 3.00, 3.625
android_after = (1 - null_share) * rate_ok + null_share * rate_null
print(f"Android after = {android_after:.3f}% = 80% x {rate_ok}% + 20% null rows x {rate_null}%")
assert abs(android_after - 3.50) < 1e-9
print(f"Android rows WITH the feature: {rate_ok}% vs {3.60}% before (flat within noise); the drop sits in null rows")

# Model release: a 10% holdback of existing users stayed on the old model during the same week
rng = np.random.default_rng(39)
n_old, n_new, p = 100_000, 900_000, 0.0395             # true rate identical in both arms
c_old = rng.binomial(n_old, p) / n_old; c_new = rng.binomial(n_new, p) / n_new
se = np.sqrt(c_old * (1 - c_old) / n_old + c_new * (1 - c_new) / n_new)
d = c_new - c_old
print(f"holdback test: new model minus old model {d * 100:+.3f} pp, 95% CI [{(d - 1.96 * se) * 100:+.3f}, {(d + 1.96 * se) * 100:+.3f}] pp")
assert abs(d) < 0.001 and (d - 1.96 * se) < 0 < (d + 1.96 * se)

# Cost of being wrong: rolling back the model would have recovered about 0.00 pp of the -0.20 pp
print("rollback of the model would recover about", round(d * 100, 2), "pp of the 0.20 pp drop (within noise)")
