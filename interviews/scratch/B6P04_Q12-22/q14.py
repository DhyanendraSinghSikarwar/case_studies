# Q14: -4% add-to-cart events but equal orders: a logging bug on Android? (illustrative simulation)
import numpy as np
import pandas as pd
from scipy.stats import chi2_contingency

rng = np.random.default_rng(14)
n_per_arm = 2_000_000
android_share = 0.45
atc_per_user = 0.60          # add-to-cart events per user per week (same on all platforms)
order_rate = 0.30            # orders per user per week (from the backend, same in both arms)
lost_android_atc = 0.04 / android_share   # share of Android ATC events that stop being logged in treatment

print(f"implied Android ATC loss if iOS/web are clean: 0.04 / 0.45 = {lost_android_atc:.1%}")
assert abs(lost_android_atc - 0.0889) < 0.0005

rows = []
for arm in ("control", "treatment"):
    plat = rng.random(n_per_arm) < android_share
    atc_true = rng.poisson(atc_per_user, n_per_arm)
    orders = rng.poisson(order_rate, n_per_arm)
    logged = atc_true.copy()
    if arm == "treatment":      # renamed event is not picked up for part of Android events
        logged = np.where(plat, rng.binomial(atc_true, 1 - lost_android_atc), atc_true)
    rows.append(pd.DataFrame({"arm": arm, "android": plat, "atc": logged, "orders": orders}))
df = pd.concat(rows, ignore_index=True)

# 1) top line
g = df.groupby("arm")[["atc", "orders"]].sum()
print("top line ATC change :", f"{g.loc['treatment','atc'] / g.loc['control','atc'] - 1:+.2%}")
print("top line order change:", f"{g.loc['treatment','orders'] / g.loc['control','orders'] - 1:+.2%}")

# 2) cut by platform
p = df.groupby(["android", "arm"])[["atc", "orders"]].sum().unstack()
for plat, name in ((False, "iOS/web"), (True, "Android")):
    a = p.loc[plat, ("atc", "treatment")] / p.loc[plat, ("atc", "control")] - 1
    o = p.loc[plat, ("orders", "treatment")] / p.loc[plat, ("orders", "control")] - 1
    print(f"{name:8} ATC {a:+.2%}   orders {o:+.2%}")

# 3) funnel ratio orders per ATC event: jumps only where logging broke
ratio = (df.groupby(["android", "arm"])["orders"].sum() / df.groupby(["android", "arm"])["atc"].sum()).unstack()
print("orders per ATC event\n", ratio.round(3))

# 4) user split by platform and arm is fine (no SRM on platform mix)
ct = pd.crosstab(df["arm"], df["android"])
print("platform mix p-value:", round(chi2_contingency(ct)[1], 3))

# checks on the numbers quoted in the text
top = g.loc['treatment','atc'] / g.loc['control','atc'] - 1
assert -0.045 < top < -0.035
ord_chg = g.loc['treatment','orders'] / g.loc['control','orders'] - 1
assert abs(ord_chg) < 0.005
ios_chg = p.loc[False, ("atc","treatment")] / p.loc[False, ("atc","control")] - 1
and_chg = p.loc[True, ("atc","treatment")] / p.loc[True, ("atc","control")] - 1
assert abs(ios_chg) < 0.005 and -0.11 < and_chg < -0.07
assert ratio.loc[True, "treatment"] > 1.07 * ratio.loc[True, "control"]
print("all asserts passed")
