# Q33: paid-search ROAS from a marketing-mix fit (illustrative)
s0, s1, r0, r1, gm = 100_000, 200_000, 500_000, 650_000, 0.40
roas0, roas1 = r0 / s0, r1 / s1
mroas = (r1 - r0) / (s1 - s0)
mprofit = mroas * gm - 1
print(f"average ROAS (total revenue / spend): {roas0:.2f} at 100k, {roas1:.2f} at 200k")
print(f"marginal ROAS {mroas:.2f}; marginal gross margin per 1 of spend {mroas*gm:.2f}; marginal profit per 1 of spend {mprofit:+.2f}")
print(f"extra revenue {r1-r0:,}; extra margin {(r1-r0)*gm:,.0f}; extra spend {s1-s0:,}; net {(r1-r0)*gm-(s1-s0):+,.0f} a month")
assert (roas0, roas1) == (5.0, 3.25) and abs(mroas - 1.5) < 1e-12 and abs(mprofit + 0.4) < 1e-12
assert (r1 - r0) * gm - (s1 - s0) == -40_000

# break-even marginal ROAS and the revenue the extra 100k would need
be = 1 / gm
need = (s1 - s0) * be
print(f"break-even marginal ROAS {be:.2f}; extra revenue needed for the extra 100k to pay for itself {need:,.0f} (fitted: {r1-r0:,})")
assert abs(be - 2.5) < 1e-12 and need == 250_000

# average ROAS includes baseline (non-search) revenue: if the baseline were 350k at zero spend,
# search-attributable revenue is 150k at 100k and 300k at 200k
for base in (0, 350_000):
    print(f"  baseline {base:,}: attributable ROAS {(r0-base)/s0:.2f} at 100k, {(r1-base)/s1:.2f} at 200k")
assert (500_000 - 350_000) / 100_000 == 1.5 and (650_000 - 350_000) / 200_000 == 1.5

# the 1.5 is an average over the 100k to 200k stretch; a diminishing-returns curve through the same two points
# (R = a + b*sqrt(S)) has a higher marginal ROAS at 100k and a lower one at 200k
import numpy as np
b = (r1 - r0) / (np.sqrt(s1) - np.sqrt(s0))
for s_ in (100_000, 150_000, 200_000):
    m = b / (2 * np.sqrt(s_))
    print(f"  sqrt curve, marginal ROAS at {s_:,}: {m:.2f} -> marginal profit per 1 spent {m*gm-1:+.2f}")
assert b / (2 * np.sqrt(100_000)) > 1.5 > b / (2 * np.sqrt(200_000))
assert b / (2 * np.sqrt(100_000)) * gm - 1 < 0          # even the best point on that curve is below break-even 2.5
