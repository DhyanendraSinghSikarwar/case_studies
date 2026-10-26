import numpy as np
from scipy.stats import ks_2samp

rng = np.random.default_rng(38)
ref = rng.normal(0, 1, 50000)                       # history: a large, clean reference
edges = np.quantile(ref, np.linspace(0, 1, 11)); edges[0], edges[-1] = -np.inf, np.inf  # 10 reference-quantile bins
ref_p = np.full(10, 0.1)

def psi(x):
    c = np.histogram(x, edges)[0] / len(x)
    c = np.clip(c, 1e-4, None)
    return float(np.sum((c - ref_p) * np.log(c / ref_p)))

B = 1000
print("null distribution = PSI/KS between the reference and clean batches drawn from the SAME history, %d bootstrap batches" % B)
print(f"{'n':>6} {'mean PSI':>9} {'p95 PSI':>8} {'p99 PSI':>8} {'P(PSI>0.1) on clean':>20} {'p99 KS D':>9}")
for n in (200, 2000, 20000):
    ps, ds = [], []
    for _ in range(B):
        b = rng.choice(ref, n, replace=True)
        ps.append(psi(b)); ds.append(ks_2samp(ref, b).statistic)
    ps, ds = np.array(ps), np.array(ds)
    print(f"{n:6d} {ps.mean():9.4f} {np.quantile(ps,.95):8.4f} {np.quantile(ps,.99):8.4f} {np.mean(ps>0.1):20.3f} {np.quantile(ds,.99):9.4f}")

# backtest: a threshold at the 99th pct, n=2000, against a real 0.15-sigma shift and 200 clean days
n = 2000
ps = [psi(rng.choice(ref, n)) for _ in range(B)]
thr = float(np.quantile(ps, .99))
clean_fa = np.mean([psi(rng.normal(0, 1, n)) > thr for _ in range(200)])
hit = np.mean([psi(rng.normal(0.15, 1, n)) > thr for _ in range(200)])
print(f"\nn=2000 chosen PSI threshold (p99 of null) = {thr:.4f}; false alarms on 200 fresh clean batches = {clean_fa:.3f}; detection of a 0.15-sigma shift = {hit:.3f}")
# many features: per-feature alpha 0.01 across 50 independent features
print("50 features, per-feature false-alarm rate 0.01: P(at least one alarm per day) = %.3f" % (1 - 0.99**50))
print("per-feature rate for a 0.01 daily family-wise rate over 50 features = %.5f" % (1 - 0.99**(1/50)))
