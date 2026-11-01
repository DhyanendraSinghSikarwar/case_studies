import numpy as np
cost, save, value = 4.0, 0.20, 120.0
g1 = dict(n=10_000, churn=0.25)
g2 = dict(n=10_000, churn=0.10)
def net(g, save=save, cost=cost, value=value):
    churners = g["n"] * g["churn"]
    saved = churners * save
    return churners, saved, saved * value - g["n"] * cost
for name, g in (("top 10,000", g1), ("next 10,000", g2)):
    c, s, v = net(g)
    print(f"{name}: churners {c:,.0f}, saved {s:,.0f}, value {s*value:,.0f}, cost {g['n']*cost:,.0f}, net {v:+,.0f}")
v1, v2 = net(g1)[2], net(g2)[2]
assert (v1, v2) == (20000.0, -16000.0)
print(f"contact both: {v1+v2:+,.0f}  (second group adds {v2:+,.0f})")
assert v1 + v2 == 4000.0
be = cost / (save * value)
print(f"break-even churn rate for this offer = {cost}/({save}*{value}) = {be:.2%}")
assert abs(be - 1/6) < 1e-12 and g2["churn"] < be < g1["churn"]
# the plan assumes a 20% save rate that is the same in both groups; test lower save rate in the top group
for s in (0.10, 0.133, 0.20):
    print(f"  save rate {s:.1%} in top group: net {net(g1, save=s)[2]:+,.0f}")
assert abs(net(g1, save=0.10)[2] - (-10000)) < 1e-9
be_s = cost / (g1["churn"] * value)
print(f"break-even save rate in top group {be_s:.1%}")
assert abs(be_s - 0.1333) < 1e-3
# sleeping dogs: the offer pushes a small share of would-be stayers to leave (assumed harm)
stayers = g1["n"] * (1 - g1["churn"])
for h in (0.0, 0.01, 0.02):
    print(f"  harm rate {h:.0%} of stayers: top-group net {v1 - h*stayers*value:+,.0f}")
h_be = v1 / (stayers * value)
print(f"net reaches zero if {h_be:.2%} of would-be stayers are pushed to leave")
assert abs(v1 - 0.01 * stayers * value - 11000) < 1e-9 and abs(h_be - 0.02222) < 1e-4
