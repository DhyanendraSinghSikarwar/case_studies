import numpy as np
from scipy.stats import skew
rng = np.random.default_rng(0)
inc = rng.lognormal(mean=11, sigma=1, size=10000)
print("mean %.0f median %.0f std %.0f skew %.2f" % (inc.mean(), np.median(inc), inc.std(), skew(inc)))
print("p25/p75/p90/p99:", np.percentile(inc,[25,75,90,99]).round(0))
print("skew after log:", round(skew(np.log(inc)),2))
