# Q4: 40 features x hourly test at 5% -> false alert arithmetic. Illustrative.
import numpy as np
from scipy import stats

F, alpha, hours = 40, 0.05, 24
checks = F * hours
exp_alerts = checks * alpha
p_any_hour = 1 - (1 - alpha) ** F
hours_with_alert = hours * p_any_hour
print(f"checks/day={checks}, expected false feature alerts/day={exp_alerts}")
print(f"P(at least one alert in an hour)={p_any_hour:.4f}; expected hours per day with a page={hours_with_alert:.1f}")
assert checks == 960 and exp_alerts == 48 and 0.871 < p_any_hour < 0.872 and 20.8 < hours_with_alert < 21.0

# verify by simulation (seeded): p-values are uniform when nothing changed
rng = np.random.default_rng(4)
sim = rng.random((100_000, F)) < alpha
print("simulated P(any in hour)=", round(sim.any(axis=1).mean(), 3), "| mean alerts per hour =", round(sim.sum(axis=1).mean(), 3))
assert abs(sim.any(axis=1).mean() - p_any_hour) < 0.005 and abs(sim.sum(axis=1).mean() - 2.0) < 0.02

# fixes, each priced by the same false-alarm arithmetic
bonf = alpha / F
p_bonf = 1 - (1 - bonf) ** F
print(f"Bonferroni per-feature level={bonf}: P(any/hour)={p_bonf:.4f}, hours/day={hours*p_bonf:.2f}")
assert abs(p_bonf - 0.0488) < 0.0005

p_k5 = stats.binom.sf(4, F, alpha)           # P(at least 5 of 40 features alert in one hour)
print(f"page only if >=5 of 40 alert: P(false page/hour)={p_k5:.4f}")
assert 0.047 < p_k5 < 0.049

p_persist3 = p_bonf ** 3                      # Bonferroni AND three consecutive hours (hours independent under no change)
print(f"Bonferroni + 3 consecutive hours: P(false page/hour)={p_persist3:.6f}; per day={hours*p_persist3:.5f}")
assert hours * p_persist3 < 0.003
p_plain3 = p_any_hour ** 3
print(f"plain 5% + 3 consecutive hours: P(false page/hour)={p_plain3:.3f}  (still ~{hours*p_plain3:.0f} a day)")
assert hours * p_plain3 > 15

# the cost of strictness: power on a real shift of 0.1 SD at n=2000 per window, per-feature z test
n, shift = 2000, 0.1
def power(a):
    zc = stats.norm.isf(a / 2); mu = shift * np.sqrt(n / 2)
    return stats.norm.sf(zc - mu) + stats.norm.cdf(-zc - mu)
print(f"per-feature power at 5%: {power(0.05):.3f}; at Bonferroni level {bonf}: {power(bonf):.3f}")
assert power(0.05) > 0.8 and 0.3 < power(bonf) < 0.6   # strictness costs power on small real shifts

# but huge samples flag trivial shifts: with n=2,000,000 a 0.003 SD shift is "significant" at 5%
n2, tiny = 2_000_000, 0.003
mu2 = tiny * np.sqrt(n2 / 2)
print(f"power to flag a 0.003 SD shift at n={n2}: {stats.norm.sf(1.96 - mu2):.2f} -> use an effect-size floor, not p alone")
assert stats.norm.sf(1.96 - mu2) > 0.5

# correlated features: does the independence assumption overstate false pages?
cov = 0.7 * np.ones((F, F)) + 0.3 * np.eye(F)
z = rng.multivariate_normal(np.zeros(F), cov, size=20_000)
pc = (np.abs(z) > 1.96).any(axis=1).mean()
print(f"with feature correlation 0.7: P(any/hour)={pc:.3f} (independence gave {p_any_hour:.3f})")
assert pc < p_any_hour
