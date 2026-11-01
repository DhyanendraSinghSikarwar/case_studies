import numpy as np
rng = np.random.default_rng(7)
# 1) History: 120 normal days of city orders, baseline 10,000/day, rain costs about 1.2% per 10 mm
days = 120
rain = np.where(rng.random(days) < 0.25, rng.gamma(2.0, 6.0, days), 0.0)   # mm
true_slope = -0.0012                                                       # per mm, log scale
noise = rng.normal(0, 0.01, days)
orders = 10_000 * np.exp(true_slope * rain + noise)
X = np.column_stack([np.ones(days), rain])
beta = np.linalg.lstsq(X, np.log(orders), rcond=None)[0]
print(f"estimated rain effect: {beta[1] * 10:+.2%} per 10 mm (true {true_slope * 10:+.2%})")
assert abs(beta[1] - true_slope) < 0.0003
# 2) Event week: rain by day (mm), control cities flat, city down 12% vs the control-based counterfactual
week_rain = np.array([0, 0, 25, 30, 20, 10, 0.0])         # Tue is index 2
rain_loss = float(np.mean(np.exp(beta[1] * week_rain) - 1))
print(f"rain explains about {rain_loss:+.1%} of the week")
total = -0.12
left = total - rain_loss
print(f"left for competitor + strike: {left:+.1%}")
# 3) Funnel split: placed orders (demand side) vs fulfilled share of placed (supply side), illustrative
placed0, ful0 = 10_400, 10_000 / 10_400
placed1, ful1 = 9_900, 8_800 / 9_900
demand = (placed1 - placed0) * ful0                    # fewer orders placed, old fulfilment rate
supply = placed1 * (ful1 - ful0)                       # more placed orders not fulfilled
print(f"placed {placed0:,} -> {placed1:,}; fulfilled share {ful0:.1%} -> {ful1:.1%}")
print(f"demand-side loss {demand:,.0f} orders, supply-side loss {supply:,.0f} orders, total {demand + supply:,.0f}")
assert round(demand + supply) == -1_200
assert round(demand) == -481 and round(supply) == -719
print(f"demand share {demand / -1200:.0%}, supply share {supply / -1200:.0%}")
assert round(demand / -1200, 2) == 0.40
# rain is demand-side (rain effect above) so competitor ~ demand-side remainder
rain_orders = rain_loss * 10_000
print(f"rain orders {rain_orders:,.0f}; competitor (demand remainder) {demand - rain_orders:,.0f}")
assert round(rain_orders) == -137 and round(demand - rain_orders) == -344
