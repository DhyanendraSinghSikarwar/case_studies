# Q3: how each north-star candidate behaves in two invented worlds (seeded)
import numpy as np

W = 4                      # weeks in window; week index 3 is "this week"
AOV = 300

def make_base():
    rng = np.random.default_rng(3)
    users = 200
    m = np.zeros((users, W), dtype=int)
    m[:60, :] = 2                                  # 60 loyal users: 2 orders every week
    casual = rng.random((140, W)) < 0.25           # 140 casual users: 25% chance per week
    m[60:, :] = casual.astype(int)
    return m

def metrics(m):
    last = m[:, 3]
    orders = int(last.sum())
    gmv = orders * AOV
    waou = int((last > 0).sum())
    active_last = last > 0
    prior = m[:, :3].sum(axis=1) > 0
    repeat_share = (active_last & prior).sum() / active_last.sum()
    return orders, gmv, waou, repeat_share

base = make_base()

heavy = base.copy()                  # world A: push heavy users harder
heavy[:60, 3] = 3

promo = np.vstack([base, np.zeros((40, W), dtype=int)])   # world B: 40 one-time promo users
promo[200:, 3] = 1

print(f"{'world':14} {'orders':>6} {'GMV':>7} {'WAOU':>5} {'repeat share':>13}")
res = {}
for name, m in [("baseline", base), ("A heavy push", heavy), ("B promo users", promo)]:
    res[name] = metrics(m)
    o, g, w, r = res[name]
    print(f"{name:14} {o:6d} {g:7d} {w:5d} {r:13.1%}")

b, a, p = res["baseline"], res["A heavy push"], res["B promo users"]
assert a[0] > b[0] and a[1] > b[1]            # orders and GMV rise in A
assert a[2] == b[2]                            # users did not change in A
assert p[2] > b[2]                             # WAOU rises in B
assert p[3] < b[3]                             # but repeat share falls in B
print("A: orders and GMV up, users flat.  B: users up, repeat share down.")
