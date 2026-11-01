# Q24: page-view randomization vs user randomization (illustrative simulation, seeded)
import numpy as np

rng = np.random.default_rng(24)
print("relative lift quoted:", round(5.2 / 5.0 - 1, 3))
assert abs(5.2 / 5.0 - 1 - 0.04) < 1e-9

U = 400000
views = rng.integers(1, 9, U)                  # 1..8 page views per user
uid = np.repeat(np.arange(U), views)
pos = np.arange(len(uid)) - np.repeat(np.cumsum(views) - views, views)   # 0-based view index inside the user
base, delta = 0.05, 0.01                       # true effect of 'having seen new': +1 point

def lift(arm):
    # carryover: a user who has seen the new design at or before this view keeps the benefit, whichever design this view shows
    first_new = np.minimum.reduceat(np.where(arm == 1, pos, 99), np.cumsum(views) - views)
    seen = pos >= first_new[uid]
    y = rng.random(len(uid)) < base + delta * seen
    return y[arm == 1].mean() - y[arm == 0].mean()

est_view = lift(rng.integers(0, 2, len(uid)))
est_user = lift(rng.integers(0, 2, U)[uid])
print(f"estimated lift in points: page-view randomization {est_view*100:.2f}; user randomization {est_user*100:.2f}; truth 1.00")
assert abs(est_user - 0.01) < 0.002 and est_view < 0.7 * est_user

# SE problem: if the metric is 'user converted in the session' copied onto every view row, the rows are clones.
conv = rng.random(U) < 0.05
y_row = conv[uid].astype(float)
se_naive = np.sqrt(y_row.var() / len(y_row))
se_user = np.sqrt(conv.var() / U)
print(f"rows={len(y_row)}, users={U}: naive SE {se_naive*100:.3f} pts vs user-level SE {se_user*100:.3f} pts; true SE is {se_user/se_naive:.2f}x bigger")
assert se_user / se_naive > 1.5
