# Q22 experimentation platform sizing (illustrative)
import hashlib, math
users, layers, exps_total, per_layer = 12_000_000, 10, 120, 12
assert per_layer * layers == exps_total and exps_total // 40 == 3
users_per_exp = users // per_layer
need = 800_000
assert users_per_exp == 1_000_000 and users_per_exp >= need
headroom = users_per_exp - need
assert headroom == 200_000 and headroom / need == 0.25
print(f"users per experiment per day={users_per_exp:,}, need={need:,}, headroom={headroom:,} ({headroom/need:.0%} of need)")

# If only 30% of users are eligible (invented), each experiment sees fewer
elig = round(users_per_exp * 0.30)
assert elig == 300_000 and elig < need
print(f"with 30% eligibility: {elig:,} < {need:,}")

# What 800,000 (400,000 per arm) can detect: baseline 5%, alpha 0.05 two-sided, power 80%
z = 1.96 + 0.8416
p, n_arm = 0.05, 400_000
mde = z * math.sqrt(2 * p * (1 - p) / n_arm)
assert abs(mde - 0.001366) < 2e-5
print(f"minimum detectable absolute lift ~ {mde*100:.3f} points ({mde/p:.1%} relative)")

# Assignment load: Little's law on the lookup service (upper bound uses the 5 ms p99 for every call)
rps, lat = 20_000, 0.005
inflight = rps * lat
assert inflight == 100
print(f"requests in flight at most ~ {inflight:.0f}; each request resolves {layers} layers")

# Deterministic hash bucketing: each layer has its own salt, so layers are independent
def bucket(uid, layer, k):
    h = hashlib.sha256(f"layer{layer}:{uid}".encode()).digest()
    return int.from_bytes(h[:8], 'big') % k
N = 120_000
counts = [0] * per_layer
cross = [[0] * per_layer for _ in range(per_layer)]
for u in range(N):
    a, b = bucket(u, 0, per_layer), bucket(u, 1, per_layer)
    counts[a] += 1
    cross[a][b] += 1
expected = N / per_layer
assert all(abs(c - expected) / expected < 0.05 for c in counts)
# users in experiment 0 of layer 0 spread evenly over layer 1 buckets (independence)
row = cross[0]
assert all(abs(c - sum(row) / per_layer) / (sum(row) / per_layer) < 0.15 for c in row)
print("bucket counts layer0:", counts)
print("layer-0 experiment 0 across layer-1 buckets:", row)
