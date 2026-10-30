# Illustrative numbers.
in_days, out_days = 5, 2
sales_in, sales_out = 1400, 1000
weekly_sales = in_days * sales_in + out_days * sales_out
print("weekly sales", weekly_sales)
assert weekly_sales == 9000
demand = 7 * sales_in
lost = demand - weekly_sales
print(f"weekly demand {demand:,}; lost units {lost}; lost margin at 4/unit {lost*4:,}")
assert (demand, lost, lost * 4) == (9800, 800, 3200)
avg_sales = weekly_sales / 7; avg_dem = demand / 7
print(f"daily sales average {avg_sales:.1f} vs daily demand {avg_dem:.1f}: understated by {1-avg_sales/avg_dem:.1%}")
assert round(avg_sales, 1) == 1285.7 and round(1 - avg_sales / avg_dem, 3) == 0.082
# Lost-sales margin is an upper bound: if 30% of shoppers substitute or come back, the true loss is smaller
for recapture in (0.0, 0.3):
    print(f"recapture {recapture:.0%}: lost margin {lost*(1-recapture)*4:,.0f}")
assert lost * 0.7 * 4 == 2240
# Censoring in a simulation: stock of 1,000 on out days caps what we see; demand varies day to day.
import numpy as np
rng = np.random.default_rng(3)
d = rng.normal(1400, 150, 100_000)
stock = np.where(rng.random(100_000) < 2 / 7, 1000, 1700)   # stock-outs on about 2 days in 7
seen = np.minimum(d, stock)
print(f"simulated: true mean demand {d.mean():.0f}, mean sales {seen.mean():.0f}, mean sales on in-stock-only days {seen[stock==1700].mean():.0f}")
assert d.mean() > seen.mean() + 100
assert seen[stock == 1700].mean() > seen.mean()
# Even the in-stock-day average is biased if some of those days sold out late: ones with high demand got cut
print("in-stock days that still hit the 1,700 cap:", f"{(d[stock==1700] > 1700).mean():.1%}")
assert (d[stock == 1700] > 1700).mean() > 0.01
