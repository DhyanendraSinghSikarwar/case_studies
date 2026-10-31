import numpy as np
from scipy.stats import ks_2samp
from sklearn.linear_model import LogisticRegression
from sklearn.metrics import roc_auc_score

rng = np.random.default_rng(9)
PER_DAY, DAYS, LAG, T0 = 200, 100, 30, 50
N = PER_DAY * DAYS
X = rng.normal(0, 1, (N, 2))                       # inputs never change
day = np.arange(N) // PER_DAY
def labels(w1, w2):
    z = X[:, 0] * w1 + X[:, 1] * w2
    return z + rng.normal(0, 0.7, N)
base = labels(2.0, 1.0)
sudden = np.where(day >= T0, labels(-1.0, 1.0), base)             # rule flips at day 50
alpha = np.clip((day - T0) / 30, 0, 1)                            # gradual: blend over 30 days
gradual = np.where(rng.random(N) < alpha, labels(-1.0, 1.0), base)
pre = day < T0
model = LogisticRegression().fit(X[pre], (base[pre] > 0).astype(int))
score = model.decision_function(X)

def page_hinkley(err, base, delta=0.02, lam=20.0):
    cum, ph_min = 0.0, 0.0
    for i, e in enumerate(err):
        cum += e - base - delta          # error above the baseline error rate, minus a small allowance
        ph_min = min(ph_min, cum)
        if cum - ph_min > lam: return i
    return None

for name, y in (("sudden", (sudden > 0).astype(int)), ("gradual", (gradual > 0).astype(int))):
    print(f"== {name} concept change starting day {T0}")
    ks_pre = ks_2samp(X[pre][:, 0], X[~pre][:, 0]); ks_pre2 = ks_2samp(X[pre][:, 1], X[~pre][:, 1])
    print(f"  feature KS before vs after: x0 D={ks_pre.statistic:.3f} p={ks_pre.pvalue:.2f} | x1 D={ks_pre2.statistic:.3f} p={ks_pre2.pvalue:.2f}  (quiet)")
    for a, b in ((10, 20), (40, 50), (60, 70), (80, 90)):
        s = (day >= a) & (day < b)
        print(f"  AUC days {a:>2}-{b:<2}: {roc_auc_score(y[s], score[s]):.3f}", end="")
    print()
    err = (model.predict(X) != y).astype(float)
    # detector sees errors only in the order labels arrive (day + LAG); order is the same as prediction order
    warm = 10 * PER_DAY                              # first 10 days set the baseline error rate
    i = warm + page_hinkley(err[warm:], err[:warm].mean())
    d = i // PER_DAY
    print(f"  Page-Hinkley fires at sample {i} = prediction day {d} -> detection delay {d - T0} days of data; with {LAG}-day label lag you learn on day {d + LAG}")
