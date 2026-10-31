hourly, tps, api = 20.0, 2000, 15.0
tok_hr = tps*3600
print(f"tokens per hour at 100% = {tok_hr:,}")
assert tok_hr == 7_200_000
def cost_per_m(u): return hourly/(tok_hr*u/1e6)
for u in (1.0, 0.3):
    print(f"utilisation {u:.0%}: cost per million output tokens = {cost_per_m(u):.3f}")
assert abs(cost_per_m(1.0) - 2.7778) < 1e-3 and abs(cost_per_m(0.3) - 9.2593) < 1e-3
be = hourly/(tok_hr/1e6*api)
print(f"break-even utilisation = {be:.4f} ({be:.1%})")
assert abs(be - 0.185185) < 1e-5
assert abs(cost_per_m(be) - api) < 1e-9
print(f"saving vs API at 30%: {(1-cost_per_m(0.3)/api):.1%}; at 100%: {(1-cost_per_m(1.0)/api):.1%}")
assert round(1-cost_per_m(0.3)/api, 3) == 0.383
# add illustrative staff and redundancy overhead: node cost doubles for 2 nodes + 5 per hour of staff time
total_hr = 2*hourly + 5
be2 = total_hr/(2*tok_hr/1e6*api)
print(f"with 2 nodes and 5/hour staff: break-even utilisation (of both nodes) = {be2:.4f}")
assert abs(be2 - 45/(2*7.2*15)) < 1e-12
print(f"two nodes plus staff, each at 30% utilisation: cost per million = {total_hr/(2*tok_hr/1e6*0.3):.3f}")
# diurnal traffic: peak-provisioned, 100% at peak for 6h, 20% for 18h
avg_u = (6*1.0 + 18*0.2)/24
print(f"example average utilisation across a day = {avg_u:.3f}")
assert abs(avg_u - 0.4) < 1e-12
assert round(1-cost_per_m(1.0)/api, 3) == 0.815 and round(total_hr/(2*tok_hr/1e6*0.3), 3) == 10.417
print(f"at 40%: {cost_per_m(0.4):.2f}; at 15%: {cost_per_m(0.15):.2f}; break-even if API price halves: {hourly/(tok_hr/1e6*api/2):.3f}")
assert round(cost_per_m(0.4), 2) == 6.94 and round(cost_per_m(0.15), 2) == 18.52 and round(hourly/(tok_hr/1e6*api/2), 3) == 0.370
