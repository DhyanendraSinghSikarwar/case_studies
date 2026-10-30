# Q42 GMV +30% with a coupon cluster: detect abuse, restate month (illustrative simulation)
import numpy as np, pandas as pd
rng = np.random.default_rng(42)
# 20,000 genuine accounts, 600 ring accounts on 40 shared devices
g = pd.DataFrame({"acct": np.arange(20_000), "age_days": rng.integers(0, 720, 20_000),
                  "device": rng.integers(0, 18_000, 20_000), "ring": False})
r = pd.DataFrame({"acct": np.arange(20_000, 20_600), "age_days": rng.integers(0, 6, 600),
                  "device": 100_000 + rng.integers(0, 40, 600), "ring": True})
# fuzz the ring: 20% older accounts, 20% with a unique device
old = rng.random(600) < 0.20; r.loc[old, "age_days"] = rng.integers(8, 25, old.sum())
uni = rng.random(600) < 0.20; r.loc[uni, "device"] = 200_000 + np.arange(uni.sum())
# genuine look-alikes: 300 new accounts in a hostel sharing 10 devices, many use the welcome coupon
h = pd.DataFrame({"acct": np.arange(20_600, 20_900), "age_days": rng.integers(0, 6, 300),
                  "device": 300_000 + rng.integers(0, 10, 300), "ring": False})
acc = pd.concat([g, r, h], ignore_index=True)
orders = []
hostel = set(range(20_600, 20_900))
for row in acc.itertuples():
    if row.acct in hostel:
        for _ in range(rng.poisson(1.2)):
            orders.append((row.acct, rng.lognormal(np.log(400), 0.4), rng.random() < 0.7, rng.random() < 0.04))
    elif row.ring:
        k = rng.integers(4, 9)
        for _ in range(k):
            orders.append((row.acct, rng.normal(900, 80), rng.random() < 0.92, rng.random() < 0.55))   # coupon_used, later cancelled/returned
    else:
        k = rng.poisson(0.9)
        for _ in range(k):
            orders.append((row.acct, rng.lognormal(np.log(500), 0.5), rng.random() < 0.06, rng.random() < 0.04))
o = pd.DataFrame(orders, columns=["acct", "gmv", "coupon", "returned"]).merge(acc, on="acct")
# rule: new account (<7d) + coupon + device shared by >=5 accounts
dev_n = acc.groupby("device").acct.transform("count")
acc["shared_device"] = dev_n >= 5
o = o.merge(acc[["acct", "shared_device"]], on="acct")
o["flag"] = (o.age_days < 7) & o.coupon & o.shared_device
tot = o.gmv.sum()
print(f"total GMV {tot/1e6:.2f}M; flagged GMV {o[o.flag].gmv.sum()/1e6:.2f}M ({o.flag.mean():.1%} of orders)")
tp = (o.flag & o.ring).sum(); fp = (o.flag & ~o.ring).sum(); fn = (~o.flag & o.ring).sum()
print(f"rule on orders: precision {tp/(tp+fp):.3f} recall {tp/(tp+fn):.3f}")
# cohort contrast
print(o.groupby(pd.cut(o.age_days, [-1, 6, 30, 720])).coupon.mean().round(3).to_string())
# restate: drop flagged orders and returned orders
clean = o[~o.flag & ~o.returned].gmv.sum()
print(f"restated GMV (no flagged, no returned) {clean/1e6:.2f}M vs reported {tot/1e6:.2f}M: change {clean/tot-1:+.1%}")
prev_month = 10.5e6      # last month's gross GMV, invented
gross_clean = o[~o.flag].gmv.sum()
print(f"reported growth {tot/prev_month-1:+.1%}; growth excluding flagged orders {gross_clean/prev_month-1:+.1%}")
true_clean = o[~o.ring].gmv.sum()
print(f"growth excluding true ring orders (known only in this simulation): {true_clean/prev_month-1:+.1%}")
assert 0.29 < tot/prev_month-1 < 0.31
assert gross_clean < tot
