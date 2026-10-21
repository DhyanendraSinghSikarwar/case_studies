import numpy as np
from statsmodels.stats.multitest import multipletests
p=np.array([0.001,0.008,0.012,0.04,0.2,0.35,0.5,0.6,0.7,0.9])
for m in ["bonferroni","fdr_bh"]:
    r=multipletests(p,alpha=0.05,method=m)
    print(m, r[0].sum(), np.round(r[1][:4],3))
print("P(>=1 false positive in 20 metrics):", round(1-0.95**20,2))
