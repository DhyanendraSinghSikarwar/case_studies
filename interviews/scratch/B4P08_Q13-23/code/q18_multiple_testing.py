import numpy as np
from scipy.stats import ks_2samp
rng = np.random.default_rng(18)
F, RUNS, N = 100, 200, 500
ALPHA = 0.05
def run_pvals(drifted):
    ref = rng.normal(0, 1, (N, F)); cur = rng.normal(0, 1, (N, F))
    cur[:, :drifted] += 0.3        # first features shift by 0.3 sigma
    return np.array([ks_2samp(ref[:, j], cur[:, j]) for j in range(F)])  # rows: (D, p)
def bh(p, q=ALPHA):
    m = len(p); o = np.argsort(p); thr = q * (np.arange(1, m + 1) / m)
    ok = np.where(p[o] <= thr)[0]; rej = np.zeros(m, bool)
    if len(ok): rej[o[:ok.max() + 1]] = True
    return rej
def rules(res):
    D, p = res[:, 0], res[:, 1]
    return {"raw p<0.05": p < ALPHA,
            "Bonferroni": p < ALPHA / F,
            "Benjamini-Hochberg": bh(p),
            "share rule (>=10% drifted)": np.full(F, (p < ALPHA).mean() >= 0.10),
            "effect floor (p<0.05 and D>=0.15)": (p < ALPHA) & (D >= 0.15)}
for drifted in (0, 5):
    any_alert = {}; caught = {}; fa_feat = {}
    for _ in range(RUNS):
        for k, flags in rules(run_pvals(drifted)).items():
            any_alert[k] = any_alert.get(k, 0) + bool(flags.any())
            if drifted:
                caught[k] = caught.get(k, 0) + flags[:drifted].mean()
    print(f"\n{'NO drift' if drifted == 0 else '5 of 100 features truly drifted by 0.3 sigma'}: {RUNS} runs, n={N} per window")
    for k in any_alert:
        extra = f" | avg share of the 5 true drifts caught {caught[k]/RUNS:.2f}" if drifted else ""
        print(f"  {k:36s} runs with an alert: {any_alert[k]:3d}/{RUNS}{extra}")
print("\nexpected false alarms per run at 5% x 100 features:", 0.05 * 100)
