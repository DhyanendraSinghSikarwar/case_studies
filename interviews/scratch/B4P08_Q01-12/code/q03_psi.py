import numpy as np

def psi(ref, cur, bins=10, eps=1e-4):
    edges = np.quantile(ref, np.linspace(0, 1, bins + 1))
    edges[0], edges[-1] = -np.inf, np.inf          # catch values outside the reference range
    r = np.histogram(ref, edges)[0] / len(ref)
    c = np.histogram(cur, edges)[0] / len(cur)
    r, c = np.clip(r, eps, None), np.clip(c, eps, None)   # epsilon for empty bins
    return float(np.sum((c - r) * np.log(c / r)))

def psi_cat(ref, cur, eps=1e-4):
    cats = sorted(set(ref) | set(cur))
    r = np.array([np.mean(np.asarray(ref) == k) for k in cats]).clip(eps)
    c = np.array([np.mean(np.asarray(cur) == k) for k in cats]).clip(eps)
    return float(np.sum((c - r) * np.log(c / r)))

rng = np.random.default_rng(7)
ref = rng.normal(0, 1, 20000)
cases = {
    "no shift":      rng.normal(0, 1, 20000),
    "mean +0.5":     rng.normal(0.5, 1, 20000),
    "variance x1.5": rng.normal(0, 1.5, 20000),
    "tail only":     np.where(rng.random(20000) < 0.03, rng.normal(5, 0.5, 20000), rng.normal(0, 1, 20000)),
}
print("PSI by scenario (10 quantile bins)")
for k, v in cases.items():
    print(f"  {k:<14}", round(psi(ref, v), 4))
print("\nPSI vs number of bins")
print("  bins        " + "".join(f"{b:>8}" for b in (5, 10, 20)))
for k, v in cases.items():
    print(f"  {k:<12}" + "".join(f"{psi(ref, v, b):8.4f}" for b in (5, 10, 20)))

print("\nNo true shift, mean PSI over 200 repeats (10 bins, reference n=5000)")
refs = rng.normal(0, 1, 5000)
for n in (100, 500, 5000, 50000):
    vals = [psi(refs, rng.normal(0, 1, n)) for _ in range(200)]
    print(f"  current n={n:<6} mean={np.mean(vals):.4f}  max={np.max(vals):.4f}")

print("\nCategorical PSI (A/B/C share 50/30/20 -> 40/30/30), with a new category D")
a = ["A"] * 50 + ["B"] * 30 + ["C"] * 20
b = ["A"] * 40 + ["B"] * 30 + ["C"] * 30
d = ["A"] * 40 + ["B"] * 30 + ["C"] * 25 + ["D"] * 5
print("  shares move :", round(psi_cat(a, b), 4))
print("  new category:", round(psi_cat(a, d), 4))
# hand check of the first number
print("  hand check  :", round((0.4-0.5)*np.log(0.4/0.5) + 0 + (0.3-0.2)*np.log(0.3/0.2), 4))
