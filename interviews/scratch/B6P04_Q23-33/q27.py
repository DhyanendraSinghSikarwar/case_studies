# Q27: cluster randomization, design effect and the cluster-size trade-off (illustrative, seeded)
import numpy as np

rng = np.random.default_rng(27)
m, rho = 50, 0.02
de = 1 + (m - 1) * rho
print("design effect:", de, "; users per arm needed:", 100_000 * de, "; clusters per arm:", 100_000 * de / m)
assert abs(de - 1.98) < 1e-9 and abs(100_000 * de - 198_000) < 1e-6

# check by simulation: variance of a mean over clusters with ICC 0.02 versus independent users
n_clusters, reps = 400, 4000
sd_between, sd_within = np.sqrt(rho), np.sqrt(1 - rho)
means = np.empty(reps)
for r in range(reps):
    cl = rng.normal(0, sd_between, (n_clusters, 1)) + rng.normal(0, sd_within, (n_clusters, m))
    means[r] = cl.mean()
var_cluster = means.var()
var_iid = 1 / (n_clusters * m)
print(f"simulated variance ratio (clustered / independent) = {var_cluster/var_iid:.2f}")
assert abs(var_cluster / var_iid - de) < 0.15
print("MDE grows by sqrt(DE) =", round(np.sqrt(de), 3))

# trade-off: ring-lattice 'friend graph' (each user linked to 10 neighbours on each side), contiguous clusters
k = 10
print("cluster size | edges cut (share) | design effect")
cuts = {}
for size in (10, 25, 50, 100, 200, 400):
    cut = 0; tot = 0
    for d in range(1, k + 1):                    # edge from i to i+d crosses a boundary if i%size + d >= size
        i = np.arange(size)
        cut += (i + d >= size).sum() / size; tot += 1
    cuts[size] = cut / tot
    print(f"{size:12d} | {cuts[size]:.3f}             | {1 + (size - 1) * rho:.2f}")
assert cuts[400] < cuts[50] < cuts[10] and 1 + 399 * rho > 1 + 49 * rho
