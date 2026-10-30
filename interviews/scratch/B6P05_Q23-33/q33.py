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

# the curve is only pinned by two points: two different curves through them give opposite advice at 150k
import numpy as np
# diminishing-returns (square-root-type) curve through the 2 points, R = a + b*sqrt(S)
b = (r1 - r0) / (np.sqrt(s1) - np.sqrt(s0)); a = r0 - b * np.sqrt(s0)
# linear through the same points
slope = mroas
rev_sqrt = a + b * np.sqrt(150_000); rev_lin = r0 + slope * 50_000
print(f"revenue at 150k: sqrt curve {rev_sqrt:,.0f}, straight line {rev_lin:,.0f}")
m_sqrt = b / (2 * np.sqrt(150_000))
print(f"marginal ROAS at 150k: sqrt curve {m_sqrt:.2f} (profit {m_sqrt*gm-1:+.2f}), straight line {slope:.2f} (profit {slope*gm-1:+.2f})")
assert abs(rev_sqrt - 580_000) < 15_000 and abs(m_sqrt - 1.5) < 0.9
# uncertainty: if the true marginal ROAS is 1.5 +/- 0.5, share of that range above the 2.5 break-even
print("a marginal ROAS of 2.5 needs the fitted +150k to be +250k, 67% higher")
assert abs(250_000 / 150_000 - 1 - 0.667) < 1e-3
