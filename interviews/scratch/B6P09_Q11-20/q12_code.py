import numpy as np

clicks, invalid = 2_000_000, 200_000
cvr_valid, cvr_invalid = 0.02, 0.0
share_invalid = invalid / clicks
blended = (1 - share_invalid) * cvr_valid + share_invalid * cvr_invalid
assert share_invalid == 0.10
assert abs(blended - 0.018) < 1e-12
print("blended CVR:", round(blended, 4))

# Bids per click if value per conversion is 50 (illustrative)
value = 50
bid_raw, bid_valid = blended * value, cvr_valid * value
assert abs(bid_raw - 0.90) < 1e-9 and abs(bid_valid - 1.00) < 1e-9
print("bid raw vs valid-only:", round(bid_raw, 2), round(bid_valid, 2), "underbid", round(1 - bid_raw / bid_valid, 3))
assert abs((1 - bid_raw / bid_valid) - 0.10) < 1e-9

# Heterogeneity: two publishers, same valid CVR, different invalid share
for name, inv in [("pub A", 0.02), ("pub B", 0.30)]:
    b = (1 - inv) * cvr_valid
    print(name, "invalid", inv, "raw CVR", round(b, 4))
assert abs((1 - 0.30) * 0.02 - 0.014) < 1e-12

# Delay: classification arrives 3 days after the click. Naive training on the last days
# treats unclassified invalid clicks as valid (or drops them), so labels differ by age.
rng = np.random.default_rng(12)
days, per_day, delay = 10, 20_000, 3
day = np.repeat(np.arange(days), per_day)
is_invalid = rng.random(day.size) < share_invalid
conv = (~is_invalid) & (rng.random(day.size) < cvr_valid)
age = days - 1 - day                                   # 0 = today
known_invalid = is_invalid & (age >= delay)            # invalid label only known after 3 days
recent = age < delay
cvr_recent_naive = conv[recent].mean()                 # all recent clicks, invalid not yet flagged
cvr_recent_true_valid = conv[recent & ~is_invalid].mean()
cvr_old_valid = conv[~recent & ~known_invalid].mean()  # matured: invalid removed
print("recent days, invalid still unflagged:", round(float(cvr_recent_naive), 4))
print("recent days, true valid only:", round(float(cvr_recent_true_valid), 4))
print("matured days, invalid removed:", round(float(cvr_old_valid), 4))
assert abs(cvr_recent_naive - 0.018) < 0.002
assert abs(cvr_old_valid - 0.02) < 0.002
assert cvr_recent_naive < cvr_old_valid               # same traffic, different apparent CVR by label age

# Fix 1: train on matured clicks only (age >= delay). Fix 2: model P(invalid) and weight.
p_valid = 1 - share_invalid
corrected = cvr_recent_naive / p_valid
print("recent naive / P(valid):", round(float(corrected), 4))
assert abs(corrected - 0.02) < 0.003
