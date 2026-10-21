import numpy as np
from statsmodels.stats.multitest import multipletests
rng = np.random.default_rng(1)
pv = np.concatenate([rng.uniform(0, 0.0005, 10), rng.uniform(0, 1, 990)])  # first 10 are real
print((pv < 0.05).sum())                       # uncorrected: many false hits
for m in ('bonferroni', 'holm', 'fdr_bh'):
    rej = multipletests(pv, alpha=0.05, method=m)[0]
    print(m, rej.sum(), 'true found:', rej[:10].sum(), 'false:', rej[10:].sum())
print(1 - 0.95**20)                            # 0.64
