import numpy as np
from scipy import stats
rng = np.random.default_rng(2)
ref = rng.normal(0, 1, 5000); live = rng.normal(0.3, 1, 5000)
print(stats.kstest(ref, 'norm'))        # one-sample: fits N(0,1)
print(stats.ks_2samp(ref, live))        # two-sample: drift detected
