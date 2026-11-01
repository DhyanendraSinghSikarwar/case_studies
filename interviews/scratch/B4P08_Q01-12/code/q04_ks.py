import numpy as np
from scipy.stats import ks_2samp

rng = np.random.default_rng(3)
print(f"{'shift (sd)':<11}{'n':>8}{'D':>8}{'p':>10}   naive(p<.05) rule(p<.001 and D>=0.1)")
for shift in (0.02, 0.30):
    for n in (200, 2000, 200000):
        a = rng.normal(0, 1, n); b = rng.normal(shift, 1, n)
        r = ks_2samp(a, b)
        naive = r.pvalue < 0.05
        rule = r.pvalue < 0.001 and r.statistic >= 0.1
        print(f"{shift:<11}{n:>8}{r.statistic:8.3f}{r.pvalue:10.4f}   {str(naive):<12} {rule}")

print("\nFalse alarms with no shift: 500 daily checks at p<0.05, n=2000 each")
fa = sum(ks_2samp(rng.normal(0, 1, 2000), rng.normal(0, 1, 2000)).pvalue < 0.05 for _ in range(500))
print("  naive alarms:", fa, "of 500 (about 5 percent is expected by construction)")
