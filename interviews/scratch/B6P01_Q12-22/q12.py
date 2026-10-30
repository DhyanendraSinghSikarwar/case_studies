import math
# Illustrative numbers. Revenue = users x conversion x orders/buyer x AOV
last = dict(users=1_000_000, conv=0.050, opb=1.60, aov=500.0)
this = dict(users=  980_000, conv=0.046, opb=1.60, aov=510.0)
def rev(d): return d["users"] * d["conv"] * d["opb"] * d["aov"]
r0, r1 = rev(last), rev(this)
chg = r1 / r0 - 1
print(f"revenue last {r0:,.0f}  this {r1:,.0f}  change {chg:+.2%}")
assert round(chg, 3) == -0.080
# log (LMDI) split: order-independent, parts add up exactly to the rupee change
tot_log = math.log(r1 / r0)
parts = {k: (r1 - r0) * math.log(this[k] / last[k]) / tot_log for k in last}
for k, v in parts.items():
    print(f"{k:6} {v:>12,.0f}  share of change {abs(v / (r1 - r0)) * (1 if v * (r1 - r0) > 0 else -1) if abs(v) > 1 else 0:+.0%}")
assert abs(sum(parts.values()) - (r1 - r0)) < 1e-6
assert abs(parts["opb"]) < 1e-6
assert round(parts["conv"] / (r1 - r0), 2) == 1.00      # conversion explains ~all of the drop
assert round(parts["aov"] / (r1 - r0), 2) == -0.24      # AOV partly offset it
assert round(parts["users"] / (r1 - r0), 2) == 0.24
# calendar check: 31-day month versus 30-day month
print(f"days effect alone: {30/31 - 1:+.1%}; revenue per day change {(r1/30)/(r0/31) - 1:+.1%}")
assert round(30/31 - 1, 3) == -0.032 and round((r1/30)/(r0/31) - 1, 3) == -0.050
# drill the winning branch: conversion by platform (illustrative)
seg = {"android": (0.80, 0.050, 0.045), "ios": (0.15, 0.050, 0.050), "web": (0.05, 0.050, 0.050)}
# (traffic share, conv last, conv this) shares held fixed for the drill
c0 = sum(s * a for s, a, b in seg.values()); c1 = sum(s * b for s, a, b in seg.values())
print(f"blended conv {c0:.2%} -> {c1:.2%}")
for k, (s, a, b) in seg.items():
    print(f"{k:8} share-weighted drop {s * (b - a) * 100:+.2f} pts of conversion")
assert round(c0, 3) == 0.050 and round(c1, 3) == 0.046
