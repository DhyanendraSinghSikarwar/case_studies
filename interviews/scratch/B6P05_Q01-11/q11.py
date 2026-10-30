import numpy as np
spend, attributed, incr, gm = 100_000.0, 400_000.0, 120_000.0, 0.30
roas, iroas = attributed / spend, incr / spend
print(f"ROAS {roas:.1f}; incremental ROAS {iroas:.1f}")
assert roas == 4.0 and abs(iroas - 1.2) < 1e-12
profit_inc = incr * gm - spend
profit_attr = attributed * gm - spend
print(f"profit on spend: incremental {profit_inc:+,.0f}; if platform number were true {profit_attr:+,.0f}")
assert abs(profit_inc + 64000) < 1e-9 and abs(profit_attr - 20000) < 1e-9
be_iroas = 1 / gm
print(f"break-even iROAS = 1/{gm} = {be_iroas:.2f}; incremental revenue needed {spend*be_iroas:,.0f}; break-even margin at iROAS 1.2 = {1/iroas:.0%}")
assert abs(be_iroas - 3.3333) < 1e-3 and abs(1 / iroas - 0.8333) < 1e-3
print(f"share of attributed revenue that was incremental: {incr/attributed:.0%}")
assert incr / attributed == 0.30
# illustrative measurement noise: the geo estimate has SE 40,000 (assumed); simulate
rng = np.random.default_rng(11)
se = 40_000.0
draws = rng.normal(incr, se, 100_000)
print(f"with SE {se:,.0f}: 95% interval for incremental revenue {incr-1.96*se:,.0f} to {incr+1.96*se:,.0f}")
p_profit = (draws * gm > spend).mean()
print(f"share of draws with a profit (incremental revenue above {spend*be_iroas:,.0f}): {p_profit:.4f}")
assert (incr + 1.96 * se) * gm < spend and p_profit < 0.001
# how large would the SE have to be before the call is open?
se_open = (spend * be_iroas - incr) / 1.96
print(f"upper 95% bound reaches break-even only if SE >= {se_open:,.0f}")
assert abs(se_open - 108843) < 1
# if ads also have a 3-month carry-over worth +50% of in-period incremental revenue
print(f"even with +50% carry-over, iROAS {iroas*1.5:.2f} and profit {incr*1.5*gm-spend:+,.0f}")
assert incr * 1.5 * gm - spend < 0
