import numpy as np
from scipy import stats

web_c, mob_c = 8_000, 2_000
web_t, mob_t = 2_000, 8_000
rc_web, rc_mob = 0.10, 0.04
rt_web, rt_mob = 0.11, 0.05
conv_c = (web_c * rc_web + mob_c * rc_mob) / (web_c + mob_c)
conv_t = (web_t * rt_web + mob_t * rt_mob) / (web_t + mob_t)
print(f"overall conversion: control {conv_c:.3%}, treatment {conv_t:.3%}")
assert round(conv_c * 100, 1) == 8.8 and round(conv_t * 100, 1) == 6.2
assert rt_web > rc_web and rt_mob > rc_mob       # treatment wins in each segment

# Randomization check: platform mix by arm (should be the same under random assignment)
table = np.array([[web_c, mob_c], [web_t, mob_t]])
chi2, p, dof, _ = stats.chi2_contingency(table, correction=False)
print(f"platform-by-arm chi2 = {chi2:.0f}, p = {p:.1e}")
assert p < 1e-100

# Standardised comparison: apply the pooled platform mix (50/50) to both arms
mix_web = (web_c + web_t) / 20_000
std_c = mix_web * rc_web + (1 - mix_web) * rc_mob
std_t = mix_web * rt_web + (1 - mix_web) * rt_mob
print(f"standardised (50/50 mix): control {std_c:.2%}, treatment {std_t:.2%}, lift {(std_t-std_c)*100:.1f} pts")
assert round((std_t - std_c) * 100, 1) == 1.0

# Under proper randomization, how often would the mix differ even a little? (web share 80% vs 20% is impossible)
rng = np.random.default_rng(10)
shares = rng.binomial(10_000, 0.5, 100_000) / 10_000
print("max |web share - 50%| in 100,000 fair randomizations:", round(np.abs(shares - 0.5).max(), 4))
assert np.abs(shares - 0.5).max() < 0.03
print("observed web share: control 80%, treatment 20%")
