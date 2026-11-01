import numpy as np
fc, act, unit = 118_000, 100_000, 25
excess = fc - act
cost = excess * unit
print("excess units", excess, "cost", cost)
assert excess == 18_000 and cost == 450_000
print("error vs actual", excess / act, "| as share of forecast", round(excess / fc, 4))
assert excess / act == 0.18 and round(excess / fc, 4) == 0.1525
# the 450,000 is an UPPER bound: it assumes every forecast unit was bought and none recovered
for share in (1.0, 0.6, 0.3):
    print(f"if supply bought {share:.0%} of the forecast excess: cost", int(cost * share))
assert int(cost * 0.6) == 270_000
# one month is one data point: compare with invented history of monthly % errors (seeded)
rng = np.random.default_rng(6)
hist = rng.normal(2, 8, 24)                    # model's past errors in % vs actual (illustrative)
base = rng.normal(0, 12, 24)                   # old method's past errors in %
print("model mean error %.1f%%, sd %.1f%%; old method sd %.1f%%" % (hist.mean(), hist.std(ddof=1), base.std(ddof=1)))
z = (18 - hist.mean()) / hist.std(ddof=1)
print("this month's +18%% is %.1f sd from the model's own history" % z)
assert z > 1.5
# asymmetric cost check: with 25 per excess unit and (invented) 40 lost margin per short unit,
# the cost-minimising quantile of demand is 40/(40+25)
q = 40 / (40 + 25)
print("order at demand quantile", round(q, 3))
assert round(q, 3) == 0.615
