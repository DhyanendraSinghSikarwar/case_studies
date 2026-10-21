import numpy as np
from statsmodels.stats.proportion import proportions_ztest
from scipy.stats import ttest_ind
z,p=proportions_ztest([1000,1100],[10000,10000]); print(round(z,2),round(p,3))
rng=np.random.default_rng(1)
a=rng.lognormal(3,1,5000); b=rng.lognormal(3.03,1,5000)
print(ttest_ind(b,a,equal_var=False))
