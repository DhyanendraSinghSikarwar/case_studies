import numpy as np
from scipy.stats import rankdata

rng = np.random.default_rng(31)
N, D, T = 4000, 160, 100          # customers, days of history, prediction day
H = 15                            # label horizon: churn within the next 15 days

def auc(y, s):
    r = rankdata(s); n1 = int(y.sum()); n0 = len(y) - n1
    return (r[y == 1].sum() - n1 * (n1 + 1) / 2) / (n1 * n0)

# daily spend panel: customers order on a day with prob p; churners stop on their churn day
churn = rng.random(N) < 0.15
c_day = np.where(churn, T + rng.integers(1, H + 1, N), 10**6)
p = rng.beta(3, 3, N) * np.where(churn, 0.55, 1.0)       # churners are slightly less active before
active = np.arange(D)[None, :] < c_day[:, None]
spend = rng.random((N, D)) < p[:, None]
spend = spend * rng.gamma(2.0, 250.0, (N, D)) * active
y = churn.astype(int)                                      # label: churned in (T, T+30]

# 1) the leaky feature: window [T-14, T+15] (centred on T); honest feature: window [T-29, T]
leaky = spend[:, T - 14:T + 16].sum(1)
honest = spend[:, T - 29:T + 1].sum(1)
print("spend_30d offline AUC (leaky window)     :", round(auc(y, -leaky), 3))
print("spend_30d point-in-time AUC (trailing)   :", round(auc(y, -honest), 3))

# 2) replay test: recompute the feature from data truncated at the prediction date and compare
def spend_30d_replay(data, t, window_fn):
    visible = data[:, :t + 1]                  # nothing after t exists in the snapshot
    return window_fn(visible, t)
def leaky_window(vis, t):                      # what the team computed; asks for days that do not exist yet
    return vis[:, max(0, t - 14):t + 16].sum(1)
def trailing_window(vis, t):
    return vis[:, t - 29:t + 1].sum(1)
rep_leaky = spend_30d_replay(spend, T, leaky_window)
rep_ok = spend_30d_replay(spend, T, trailing_window)
diff_leaky = np.mean(~np.isclose(rep_leaky, leaky))
diff_ok = np.mean(~np.isclose(rep_ok, honest))
print("share of rows where replay != stored, leaky:", round(diff_leaky, 3), " trailing:", diff_ok)
# rows that changed are exactly those with spend in days T+1..T+15
future_used = spend[:, T + 1:T + 16].sum(1) > 0
assert np.array_equal(~np.isclose(rep_leaky, leaky), future_used)
assert diff_ok == 0.0

# 3) shift test: push the window back by 15 days; a leak vanishes, real signal stays
shifted = spend[:, T - 29 - 15:T + 1 - 15].sum(1)
print("AUC after shifting the window 15 days back:", round(auc(y, -shifted), 3))

# 4) audit the rest of the feature set with the same replay and a suspicious-AUC screen
orders_7d = (spend[:, T - 6:T + 1] > 0).sum(1)                    # trailing, fine
last_order_gap_full = np.array([T - np.max(np.nonzero(r[:T + 1 + 15])[0], initial=0) for r in spend])  # looks 15 days ahead
last_order_gap_ok = np.array([T - np.max(np.nonzero(r[:T + 1])[0], initial=0) for r in spend])
rows = [("spend_30d", leaky, rep_leaky), ("orders_7d", orders_7d, orders_7d),
        ("days_since_last_order", last_order_gap_full, last_order_gap_ok)]
for name, stored, replay in rows:
    flag = np.mean(~np.isclose(stored, replay))
    a = max(auc(y, stored), 1 - auc(y, stored))
    print(f"{name:24s} rows changed by replay: {flag:5.3f}   single-feature AUC as stored: {a:.3f}")

assert 0.82 < auc(y, -leaky) < 0.92 and 0.72 < auc(y, -honest) < 0.82
assert auc(y, -leaky) - auc(y, -honest) > 0.06
assert abs(auc(y, -shifted) - auc(y, -honest)) < 0.03
assert diff_leaky > 0.3
