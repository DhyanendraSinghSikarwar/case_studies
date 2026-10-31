from fractions import Fraction as F

good_profit, bad_loss = 1000, 6000
cuts = {"A": (40_000, F(2, 100)), "B": (55_000, F(35, 1000)), "C": (70_000, F(6, 100))}
be = F(good_profit, good_profit + bad_loss)
print("break-even bad rate:", float(be))
assert abs(float(be) - 0.142857) < 1e-5

def profit(n, r):
    bad = n * r
    return (n - bad) * good_profit - bad * bad_loss
P, BAD = {}, {}
for k, (n, r) in cuts.items():
    BAD[k] = n * r
    P[k] = profit(n, r)
    print(k, "approved", n, "bad", int(BAD[k]), "profit", int(P[k]))
assert (int(BAD["A"]), int(BAD["B"]), int(BAD["C"])) == (800, 1925, 4200)
assert (int(P["A"]), int(P["B"]), int(P["C"])) == (34_400_000, 41_525_000, 40_600_000)

# Marginal bands
for a, b in (("A", "B"), ("B", "C")):
    extra = cuts[b][0] - cuts[a][0]
    xbad = BAD[b] - BAD[a]
    xr = xbad / extra
    delta = P[b] - P[a]
    print(a, "->", b, "extra", extra, "extra bad", int(xbad), "marginal bad rate", round(float(xr), 4), "profit change", int(delta))
    assert delta == (extra - xbad) * good_profit - xbad * bad_loss
    assert (xr < be) == (delta > 0)
assert round(float((BAD["B"] - BAD["A"]) / 15_000), 3) == 0.075
assert round(float((BAD["C"] - BAD["B"]) / 15_000), 4) == 0.1517

# Sensitivity: multiply every bad rate by a factor
best = {}
for f in (F(1), F(12, 10), F(15, 10), F(2)):
    pr = {k: profit(n, r * f) for k, (n, r) in cuts.items()}
    best[float(f)] = max(pr, key=pr.get)
    print("bad rates x", float(f), "best cutoff", best[float(f)], {k: int(v) for k, v in pr.items()})
assert best[1.0] == "B" and best[2.0] == "A"
# How far can the A->B band bad rate rise before B is worse than A?
print("A->B band can rise from 7.5% to", round(float(be), 4), "before the extra applicants lose money")
