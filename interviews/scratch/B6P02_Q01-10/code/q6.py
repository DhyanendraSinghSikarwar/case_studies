# Q6 delivery-time model: prove or disprove training-serving skew on account_age (illustrative numbers)
import numpy as np
rng = np.random.default_rng(6)

n = 50_000
age_days = np.round(rng.lognormal(mean=3.6, sigma=1.0, size=n)).clip(0, 1500)   # offline: days
dist_km = rng.gamma(4, 1.0, size=n)

def model(age, dist):                          # the trained model: log-shaped in age
    return 13.1 + 4.1 * np.log1p(age)

pred_offline = model(age_days, dist_km)
print(f"mean prediction with offline feature (days): {pred_offline.mean():.1f} min")

# Hypothesis: the service computes account_age in HOURS
age_service = age_days * 24
pred_service = model(age_service, dist_km)
print(f"mean prediction with service feature (hours): {pred_service.mean():.1f} min")
assert 27.5 < pred_offline.mean() < 28.5 and 40.5 < pred_service.mean() < 41.5

# Parity test: join the logged service value with the offline value for the SAME rows
ratio = age_service / np.where(age_days == 0, np.nan, age_days)
r = ratio[~np.isnan(ratio)]
print(f"ratio service/offline on {len(r):,} rows: min {r.min():.2f} median {np.median(r):.2f} max {r.max():.2f}")
assert r.min() == r.max() == 24.0              # a constant ratio proves a unit bug

# If the cause were random noise instead, the ratio would not be constant:
noisy = age_days * rng.uniform(0.8, 1.2, n)
r2 = noisy[age_days > 0] / age_days[age_days > 0]
print(f"noise-case ratio spread: {r2.min():.2f} to {r2.max():.2f}")
assert r2.max() - r2.min() > 0.3

# Fix: change the service function to days (shared code), no retrain. Then re-run parity.
age_fixed = age_service / 24
pred_fixed = model(age_fixed, dist_km)
print(f"after fix: mean prediction {pred_fixed.mean():.1f} min, max abs diff vs offline {np.abs(pred_fixed - pred_offline).max():.1e}")
assert np.allclose(pred_fixed, pred_offline)

# Size of the shift explained by the unit: 4.1 * ln(24) minutes on every row with age > 0
shift = 4.1 * np.log(24)
print(f"expected mean shift from the unit alone: about {shift:.1f} min; observed {pred_service.mean() - pred_offline.mean():.1f} min")
assert abs((pred_service.mean() - pred_offline.mean()) - shift) < 1.0
