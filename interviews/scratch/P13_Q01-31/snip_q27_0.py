import numpy as np
from scipy import stats
t = np.array([[8, 2], [1, 5]])
print(stats.fisher_exact(t))                      # odds ratio 20, p = 0.035
chi2, p, dof, exp = stats.chi2_contingency(t, correction=False)
print(round(p, 4)); print(exp)                    # 0.0134 ; expected counts include 2.625 (<5)
