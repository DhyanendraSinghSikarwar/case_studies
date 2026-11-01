# Q22: is Tue-Thu enough for a food-delivery test? (simulation, illustrative numbers)
import numpy as np
from scipy.stats import ttest_ind

rng = np.random.default_rng(22)
n = 60_000
days = ["Mon", "Tue", "Wed", "Thu", "Fri", "Sat", "Sun"]
share = np.array([0.12, 0.12, 0.12, 0.12, 0.12, 0.20, 0.20])   # Sat + Sun = 40% of weekly orders
assert abs(share.sum() - 1) < 1e-12 and abs(share[5:].sum() - 0.40) < 1e-12
effect = np.array([0.05] * 5 + [-0.03] * 2)                   # weekday customers like it (+5%), weekend customers do not (-3%)

weekly_mean = 3.0                                              # orders per user per week (invented)
taste = rng.gamma(2.0, 0.5, size=(2 * n,))                      # user-level heterogeneity, mean 1
arm = np.r_[np.zeros(n, int), np.ones(n, int)]
lam = weekly_mean * taste[:, None] * share[None, :] * (1 + effect[None, :] * arm[:, None])
orders = rng.poisson(lam)                                      # users x 7 days, one week

def lift(cols, label):
    y = orders[:, cols].sum(axis=1)
    t, c = y[arm == 1], y[arm == 0]
    r = ttest_ind(t, c, equal_var=False)
    print(f"{label:22} lift {t.mean() / c.mean() - 1:+.2%}  p = {r.pvalue:.4f}  (orders/user/week-part: {c.mean():.3f} -> {t.mean():.3f})")
    return t.mean() / c.mean() - 1

l_tt = lift([1, 2, 3], "Tue-Thu only")
l_wk = lift(list(range(7)), "full week")
l_we = lift([5, 6], "weekend only")
true_week = (share * effect).sum()
print(f"true full-week effect = 0.12*5*0.05 + 0.40*(-0.03) = {true_week:+.2%}")
assert abs(true_week - 0.018) < 1e-12
assert l_tt > 0.03 and abs(l_wk - 0.018) < 0.01 and l_we < 0

# Tue-Thu covers only 36% of weekly orders
print(f"Tue-Thu share of weekly orders = {share[1:4].sum():.0%}")
assert abs(share[1:4].sum() - 0.36) < 1e-12

# Precision of the full-week readout: relative MDE for orders per user with 60,000 users per arm
y = orders.sum(axis=1)
cv_week = y[arm == 0].std() / y[arm == 0].mean()
mde_week = 2.8 * cv_week * np.sqrt(2 / n)
se_week = cv_week * np.sqrt(2 / n)
print(f"CV of weekly orders per user = {cv_week:.2f}; SE of the relative lift = {se_week:.2%}; MDE = {mde_week:.2%}")
n_need = 2 * (2.8 * cv_week / true_week) ** 2
print(f"the true weekly effect (+1.80%) is {true_week / mde_week:.1f}x the MDE; users per arm for 80% power at +1.8%: about {n_need:,.0f}")
assert 35_000 < n_need < 45_000
assert 0.01 < mde_week < 0.02 and true_week > 0
print("all asserts passed")
