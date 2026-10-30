# Q7 v2 live 5 days, metric -4% versus prior week, campaign shifted the mix (illustrative numbers)
import numpy as np
from scipy.stats import norm

# Segments: organic vs campaign-acquired users. Conversion rates per segment and model.
share_prev = {"organic": 0.80, "campaign": 0.20}
share_now = {"organic": 0.70, "campaign": 0.30}
conv_v1 = {"organic": 0.100, "campaign": 0.050}          # what v1 would achieve (known from past)
conv_v2 = {"organic": 0.1015, "campaign": 0.0510}        # v2 is slightly better inside each segment

def overall(share, conv): return sum(share[k] * conv[k] for k in share)
prev = overall(share_prev, conv_v1)
now = overall(share_now, conv_v2)
print(f"last week (v1, old mix): {prev:.4f}; this week (v2, new mix): {now:.4f}; change {now/prev-1:+.1%}")
assert abs(now / prev - 1 + 0.04) < 0.005   # about -4%

# Decompose into mix effect and model effect
mix_only = overall(share_now, conv_v1)                    # v1 on the new mix
print(f"v1 on the new mix would give {mix_only:.4f} ({mix_only/prev-1:+.1%})")
print(f"model effect of v2 on the new mix: {now/mix_only-1:+.1%}")
assert mix_only / prev - 1 < -0.05 and now / mix_only - 1 > 0.01

# Evidence in 24 hours: switch back test. How many sessions per arm to see a 3% relative drop?
p = now
d = 0.03 * p
n_arm = 2 * (1.96 + 0.8416) ** 2 * p * (1 - p) / d ** 2
print(f"sessions per arm to detect a 3% relative drop at p={p:.4f}: {int(np.ceil(n_arm)):,}")
daily = 400_000
for split in (0.05, 0.50):
    days = n_arm / (daily * split)
    print(f"  with {split:.0%} of {daily:,}/day on v1: {days:.1f} days")
assert (n_arm / (daily * 0.05)) > 5 and (n_arm / (daily * 0.5)) < 1.0
