import numpy as np

before, after, consent, orders = 10_000, 7_000, 0.60, 25_000
drop = 1 - after / before
naive = after / consent
assert abs(drop - 0.30) < 1e-12 and round(naive) == 11_667
print("drop", drop, "naive scale-up", round(naive), "vs before", round(naive / before - 1, 3))
assert round(naive / before - 1, 3) == 0.167

# What the numbers say: first-party orders are flat, so true conversions did not rise 16.7%.
cov_before, cov_after = before / orders, after / orders
print("attributed share of orders before/after:", cov_before, cov_after)
assert cov_before == 0.40 and cov_after == 0.28
# Proportional loss would give 6,000 (60% of 10,000); we see 7,000, so reporting kept 70% of volume.
implied_factor = (after / before) / consent
print("observed retention / consent share =", round(implied_factor, 3))
assert round(implied_factor, 3) == 1.167       # consenters appear to convert 16.7% more often (or modelled credit fills the gap)

# Calibration scalar for the bid model: attributed conversions per order dropped 40% -> 28%.
# If the bid model predicts P(conversion) learned on old labels, its predictions are now ~30% too high
# relative to the new reported labels, but NOT too high relative to true conversions.
true_per_day = orders * cov_before            # assumption: old attribution was ~complete (test with a holdout!)
print("if old reporting was complete, true attributed-eligible conversions/day ~", true_per_day)
assert true_per_day == 10_000

# Simulation: consenters differ from non-consenters
rng = np.random.default_rng(16)
n = 200_000
consent_flag = rng.random(n) < consent
rate = np.where(consent_flag, 0.0467, 0.0333)    # consenters convert 1.4x more (illustrative)
conv = rng.random(n) < rate
true_total = conv.sum(); seen = conv[consent_flag].sum()
scaled = seen / consent
print("sim: true", true_total, "seen", seen, "naive scaled", round(scaled), "ratio", round(scaled / true_total, 3))
assert scaled > 1.1 * true_total               # naive scale-up overstates when consenters are better converters
# Fix with a stratified ratio: calibrate on a segment where outcomes are known for everyone (first-party logged-in users)
logged = rng.random(n) < 0.3
ratio = conv[logged & consent_flag].sum() / conv[logged].sum()   # share of true conversions visible among logged-in
est = seen / ratio
print("sim: estimate scaled by visible share in logged-in segment", round(est), "true", true_total)
assert abs(est / true_total - 1) < 0.05
