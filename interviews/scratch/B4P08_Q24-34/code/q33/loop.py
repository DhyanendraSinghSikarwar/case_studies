import numpy as np
from sklearn.linear_model import LogisticRegression
from sklearn.ensemble import GradientBoostingClassifier
from sklearn.metrics import roc_auc_score

rng = np.random.default_rng(33)
def applicants(n):
    x1 = rng.normal(0, 1, n)                 # bureau-like score (higher is safer)
    x2 = rng.normal(0, 1, n)                 # other signal
    # truth: for normal applicants x1 and x2 both matter; for thin-file (x1 low) x2 matters in the OPPOSITE way
    logit = -0.5 - 1.2 * x1 + np.where(x1 > -0.5, 0.9 * x2, -1.5 * x2)
    y = (rng.random(n) < 1 / (1 + np.exp(-logit))).astype(int)      # 1 = defaults
    return np.c_[x1, x2], y

X, y = applicants(60_000)
X_new, y_new = applicants(60_000)             # fresh applicants, ALL labelled: this is the truth we can only see in a simulation

# old policy: reject x1 < -0.5; labels exist only for approved
approved = X[:, 0] >= -0.5
print(f"approved {approved.mean():.0%} of applicants; labels observed for {approved.sum()} of {len(y)}")

def fit(Xt, yt, w=None):
    return GradientBoostingClassifier(n_estimators=100, max_depth=3, random_state=0).fit(Xt, yt, sample_weight=w)

m = fit(X[approved], y[approved])
ap_new = X_new[:, 0] >= -0.5
print("--- retrain on approved-only labels")
print(f"measured AUC (approved applicants only) {roc_auc_score(y_new[ap_new], m.predict_proba(X_new[ap_new])[:, 1]):.3f}")
print(f"true AUC (all applicants)               {roc_auc_score(y_new, m.predict_proba(X_new)[:, 1]):.3f}")
print(f"true AUC inside rejected region         {roc_auc_score(y_new[~ap_new], m.predict_proba(X_new[~ap_new])[:, 1]):.3f}")

# mitigation: approve a random 5 % of the would-be rejected (exploration holdout), weight them 1/0.05
EPS = 0.05
explore = (~approved) & (rng.random(len(y)) < EPS)
use = approved | explore
w = np.where(explore, 1 / EPS, 1.0)
m2 = fit(X[use], y[use], w[use])
print(f"--- retrain with {explore.sum()} exploration labels (cost: we knowingly approve some risky cases)")
print(f"true AUC (all applicants)               {roc_auc_score(y_new, m2.predict_proba(X_new)[:, 1]):.3f}")
print(f"true AUC inside rejected region         {roc_auc_score(y_new[~ap_new], m2.predict_proba(X_new[~ap_new])[:, 1]):.3f}")
print(f"measured AUC (approved applicants only) {roc_auc_score(y_new[ap_new], m2.predict_proba(X_new[ap_new])[:, 1]):.3f}")
