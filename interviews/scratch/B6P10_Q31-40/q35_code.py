import math
listings, tok, rate, hours = 3_000_000, 1000, 20_000, 24
total = listings * tok
secs = total / rate
cluster_hours = secs / 3600
clusters = math.ceil(cluster_hours / hours)
print("tokens", total, "seconds", secs, "cluster-hours", round(cluster_hours, 2), "clusters", clusters)
assert total == 3_000_000_000 and secs == 150_000 and round(cluster_hours, 2) == 41.67 and clusters == 2
# utilisation of 2 clusters and headroom for reruns
cap_h = clusters * hours
print("capacity hours", cap_h, "utilisation", round(cluster_hours / cap_h, 3))
assert round(cluster_hours / cap_h, 3) == 0.868
# if 10% fail quality checks and are redone, and 5% are retried for format errors
for redo in (0.10, 0.15, 0.20):
    h = cluster_hours * (1 + redo)
    print("redo", redo, "hours", round(h, 2), "clusters", math.ceil(h / 24), "util at 2:", round(h / 48, 3))
assert math.ceil(cluster_hours * 1.10 / 24) == 2 and math.ceil(cluster_hours * 1.20 / 24) == 3
assert round(cluster_hours * 1.15 / 48, 3) == 0.998
# audit sample: 400 random listings per language batch gives margin ~ +-5 points at worst case
n = 385
moe = 1.96 * math.sqrt(0.25 / n)
print("n", n, "worst-case 95% margin", round(moe, 3))
assert round(moe, 3) == 0.05
# 1,000 tokens assumed to be all generated at the quoted rate (conservative: prefill is usually faster)
