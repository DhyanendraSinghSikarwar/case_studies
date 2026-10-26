import numpy as np
from scipy.stats import wasserstein_distance
from scipy.spatial.distance import jensenshannon
rng = np.random.default_rng(21)
n = 20000
age_ref = rng.normal(35, 8, n); inc_ref = rng.normal(60000, 15000, n)
cases = {
 "age +2 years (mean shift)":      ("age", age_ref, age_ref + 2 + rng.normal(0, 0, n)),
 "age sd 8 -> 12 (spread change)": ("age", age_ref, rng.normal(35, 12, n)),
 "income +2000 rupees":            ("inc", inc_ref, rng.normal(62000, 15000, n)),
 "income +10000 rupees":           ("inc", inc_ref, rng.normal(70000, 15000, n)),
}
def js_hist(a, b, bins=20):
    edges = np.histogram_bin_edges(np.concatenate([a, b]), bins=bins)
    pa = np.histogram(a, edges)[0] + 1e-9; pb = np.histogram(b, edges)[0] + 1e-9   # tiny count avoids 0 bins
    return jensenshannon(pa / pa.sum(), pb / pb.sum(), base=2)   # distance (sqrt of divergence), 0..1
print(f"{'case':34s} {'W (raw units)':>14s} {'W/ref sd':>9s} {'JS (base 2)':>12s}")
for name, (_, a, b) in cases.items():
    w = wasserstein_distance(a, b)
    print(f"{name:34s} {w:14.2f} {w / a.std():9.3f} {js_hist(a, b):12.3f}")
# zero-count behaviour: KL would be infinite, JS stays finite
p = np.array([0.5, 0.5, 0.0]); q = np.array([0.4, 0.4, 0.2])
print("JS distance with an empty bin in p:", round(float(jensenshannon(p, q, base=2)), 3), "| KL(q||p) would divide by zero")
