import numpy as np
rng = np.random.default_rng(28)
TRUE_P = 0.05                                    # true 7-day conversion probability (model predicts 5%)
# Share of eventual conversions that have happened by day d after the click (illustrative delay curve)
cdf = np.array([0.30, 0.50, 0.65, 0.78, 0.88, 0.95, 1.00])    # day 1 ... day 7
N = 200_000
print("cohort age (days) | matured share | expected observed | observed (sim) | pred/obs")
rows = []
for age in range(1, 8):
    # each user converts w.p. TRUE_P within 7 days; conversion day drawn from the delay curve
    conv = rng.random(N) < TRUE_P
    u = rng.random(N)
    day = np.searchsorted(cdf, u) + 1             # day of conversion, 1..7
    seen = conv & (day <= age)
    obs = seen.mean()
    rows.append((age, cdf[age - 1], TRUE_P * cdf[age - 1], obs))
    print(f"{age:17d} | {cdf[age-1]:13.2f} | {TRUE_P*cdf[age-1]:17.4f} | {obs:14.4f} | {TRUE_P/obs:.2f}")
assert abs(rows[0][3] - 0.015) < 0.0015            # yesterday's cohort: about 1.5%
assert abs(rows[-1][3] - 0.05) < 0.0015           # fully matured: about 5%
# Prompt arithmetic: predicted 5% vs observed 1.5% would be a miscalibration of 3.33x if read naively
assert abs(0.05 / 0.015 - 3.333) < 0.001
# Maturity-adjusted calibration of age-1 cohort: observed / (pred * share matured)
adj = rows[0][3] / (0.05 * cdf[0])
print(f"maturity-adjusted ratio for yesterday's cohort: {adj:.2f} (1.00 means well calibrated)")
assert 0.9 < adj < 1.1
# Alert rule: only evaluate cohorts at least 7 days old; threshold uses sampling noise at that size
se = np.sqrt(TRUE_P * (1 - TRUE_P) / 20000)
print(f"for a 20,000-user cohort the standard error of a 5% rate is {se:.4f}; alert band about +/-{1.96*se:.4f}")
assert abs(se - 0.00154) < 0.00005
print("asserts passed")
