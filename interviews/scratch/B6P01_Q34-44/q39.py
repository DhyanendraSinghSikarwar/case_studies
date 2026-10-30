# Q39 CTR +5% vs 8-week retention -0.5pt (illustrative)
import numpy as np
from scipy.stats import norm
users = 1_000_000
clicks_ctrl, clicks_trt = 20.0, 21.0            # clicks per user in 8 weeks, +5%
value_per_click = 0.02                           # invented
click_gain = (clicks_trt - clicks_ctrl) * value_per_click
ret_ctrl, ret_trt = 0.400, 0.395
future_value_per_retained = 6.0                  # invented value of a retained user over the next 6 months
retention_loss = (ret_ctrl - ret_trt) * future_value_per_retained
print(f"short-term gain per exposed user: {click_gain:.4f}")
print(f"long-term loss per exposed user : {retention_loss:.4f}")
print(f"net per user {click_gain-retention_loss:+.4f}; net for 1M users {(click_gain-retention_loss)*users:+,.0f}")
be = click_gain / (ret_ctrl - ret_trt)
print(f"break-even future value per retained user: {be:.2f}")
assert abs(click_gain - 0.02) < 1e-12 and abs(retention_loss - 0.03) < 1e-12 and abs(be - 4.0) < 1e-9

# holdout size to detect a 0.5pt retention difference at 40% base, alpha 0.05 two-sided, 80% power
p = 0.40; d = 0.005
n = 2 * (norm.ppf(0.975) + norm.ppf(0.80))**2 * p * (1 - p) / d**2
print(f"users per arm needed: {n:,.0f}")
assert 150_000 < n < 152_000

# diversity metric: entropy of item exposure share, two feeds over 1,000 items
ranks = np.arange(1, 1001)
def entropy(alpha):
    w = ranks**(-alpha); w = w/w.sum()
    return -(w*np.log2(w)).sum()
h0, h1 = entropy(0.8), entropy(1.1)
print(f"exposure entropy (bits): old feed {h0:.2f}, new feed {h1:.2f}, change {h1/h0-1:+.1%}")
assert h1 < h0
