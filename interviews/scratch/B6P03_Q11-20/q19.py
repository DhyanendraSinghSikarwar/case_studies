# Q19: dropping the 2% of rows with a missing key feature (exact counts from the prompt)
import numpy as np
from scipy.stats import chi2_contingency, rankdata
rows, pos = 200_000, 1_000
mis_n, mis_pos = 4_000, 600
obs_n, obs_pos = rows - mis_n, pos - mis_pos
print("observed rows", obs_n, "observed positives", obs_pos); assert obs_n == 196_000 and obs_pos == 400
r_mis, r_obs = mis_pos / mis_n, obs_pos / obs_n
print(f"positive rate: missing {r_mis:.2%}  present {r_obs:.3%}  ratio {r_mis / r_obs:.1f}x")
assert r_mis == 0.15 and round(r_obs, 5) == 0.00204 and round(r_mis / r_obs, 1) == 73.5
print(f"rows dropped {mis_n / rows:.1%}; positives dropped {mis_pos / pos:.0%}")
assert mis_n / rows == 0.02 and mis_pos / pos == 0.6
tab = np.array([[mis_pos, mis_n - mis_pos], [obs_pos, obs_n - obs_pos]])
chi2, p, _, _ = chi2_contingency(tab, correction=False)
print(f"chi-square {chi2:,.0f}, p-value {p:.1e}")
assert p < 1e-100
# missing flag as a single feature
y = np.r_[np.ones(mis_pos), np.zeros(mis_n - mis_pos), np.ones(obs_pos), np.zeros(obs_n - obs_pos)]
flag = np.r_[np.ones(mis_n), np.zeros(obs_n)]
r = rankdata(flag); n1 = y.sum(); n0 = len(y) - n1
auc = (r[y == 1].sum() - n1 * (n1 + 1) / 2) / (n1 * n0)
tpr, fpr = mis_pos / pos, (mis_n - mis_pos) / (rows - pos)
print(f"AUC of the missing flag alone {auc:.3f}  (TPR {tpr:.2f}, FPR {fpr:.4f}, (1+TPR-FPR)/2 = {(1 + tpr - fpr) / 2:.3f})")
assert abs(auc - (1 + tpr - fpr) / 2) < 1e-9 and auc > 0.78
# what drop does to training and what happens live: share of live positives in missing rows
print(f"after dropping, training positives {obs_pos} of {pos}; but in live traffic 4,000 per 200,000 rows still arrive with the feature missing")
# If we mean-impute and skip the flag, the model cannot tell those rows apart:
print(f"if scored like normal rows, expected positives in the missing group at the normal rate: {mis_n * r_obs:.1f} versus {mis_pos} real")
assert round(mis_n * r_obs, 1) == 8.2
