# Q7: alias 'champion' moved 17 -> 18 but 4 of 10 pods cached 17. Illustrative; seeded.
import math
from collections import Counter
import numpy as np

pods = ["v18"] * 6 + ["v17"] * 4
stale = pods.count("v17") / len(pods)
assert stale == 0.4

# Interpretation: the 0.08 is the mean ABSOLUTE per-request score difference between versions.
# The fleet-wide expected deviation from the intended model is then 0.4 x 0.08.
fleet_dev = stale * 0.08
print("expected mean |score deviation| over all traffic =", round(fleet_dev, 3))
assert round(fleet_dev, 3) == 0.032

rng = np.random.default_rng(7)
N = 200_000
s18 = rng.beta(2, 5, N)
sd = 0.08 * math.sqrt(math.pi / 2)                       # normal noise with mean absolute value 0.08
s17 = np.clip(s18 + rng.normal(0, sd, N), 0, 1)           # (clipping makes the mean slightly smaller)
pod_idx = rng.integers(0, 10, N)                          # random load balancing
served_v17 = np.array([pods[i] == "v17" for i in pod_idx])
served = np.where(served_v17, s17, s18)
dev = np.abs(served - s18).mean()
print(f"simulated share on v17 = {served_v17.mean():.3f}; mean |deviation| from intended = {dev:.4f}")
assert abs(served_v17.mean() - 0.4) < 0.005 and 0.028 < dev < 0.034

# a user making 5 requests sees both versions with probability:
p_mixed = 1 - 0.6**5 - 0.4**5
print("P(a user sees both versions in 5 requests) =", round(p_mixed, 4))
assert round(p_mixed, 4) == 0.912

# detection TODAY: every response carries model_version (header) and a metric labelled by version.
logs = Counter(pods[i] for i in pod_idx[:5000])
print("version counts in 5,000 logged responses:", dict(logs))
def check_versions(counter, expected, minutes_since_promotion, grace=10):
    extra = [v for v in counter if v != expected]
    if minutes_since_promotion >= grace and extra:
        return f"ALERT: serving {sorted(counter)} but expected {expected}"
    return "ok"
msg = check_versions(logs, "v18", 15); print(msg)
assert msg.startswith("ALERT") and check_versions(Counter({"v18": 10}), "v18", 15) == "ok"
assert check_versions(logs, "v18", 3) == "ok"            # inside the grace period, no alert

# fix: rolling restart one pod at a time; illustrative 90 s to load and pass readiness
stale_pods, per_pod_s, max_unavailable = 4, 90, 1
restart_min = stale_pods * per_pod_s / max_unavailable / 60
print("rolling restart time (minutes):", restart_min)
assert restart_min == 6.0

# design: deployments pin a numeric version; the alias is only read by the promotion job
def resolve_at_deploy(alias_table, alias): return alias_table[alias]    # returns 18, written into the manifest
manifest = {"model": "fraud", "version": resolve_at_deploy({"champion": 18}, "champion")}
assert manifest["version"] == 18
print("manifest pins:", manifest)

# detection delay example: alias moved 10:00, alert rule with 10 min grace + 5 min metric window -> 10:15
detect = 10 + 5
print("detected by 10:%02d" % detect); assert detect == 15
