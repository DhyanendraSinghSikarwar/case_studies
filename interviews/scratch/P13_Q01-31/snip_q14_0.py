import numpy as np
from scipy import stats
obs = np.array([[90, 110], [60, 140]])      # [clicked, not] x [A, B]
chi2, p, dof, exp = stats.chi2_contingency(obs, correction=False)
print(round(chi2, 3), round(p, 4), dof)     # 9.6 0.0019 1
print(exp)                                   # [[75 125], [75 125]]
print(stats.chisquare([18, 22, 20, 25, 15], f_exp=[20]*5))   # fair die? stat 2.9, p 0.575
