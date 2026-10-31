import math
# Q6 ETA: illustrative numbers from the prompt (peak orders assumed to be only the 20% peak arrivals)
orders_day, peak_share, peak_hours = 400_000, 0.20, 2
dwell_s, refresh_s = 35 * 60, 30
peak_orders = orders_day * peak_share
lam = peak_orders / (peak_hours * 3600)          # orders per second during peak
L = lam * dwell_s                                 # Little's law: L = lambda * W
refresh_rps = L / refresh_s
total_rps = refresh_rps + lam
print(f"peak arrivals {peak_orders:,.0f} over {peak_hours} h = {lam:.2f} orders/s")
print(f"in flight at peak L = {lam:.2f} x {dwell_s} s = {L:,.0f}")
print(f"refresh {refresh_rps:,.1f} rps + checkout {lam:.2f} rps = {total_rps:,.1f} rps; refresh share {refresh_rps/total_rps:.1%}")
print(f"average in flight over the day {orders_day/86_400*dwell_s:,.0f} ({L/(orders_day/86_400*dwell_s):.1f}x)")
print(f"60 s refresh: {L/60:,.1f} + {lam:.2f} = {L/60+lam:,.1f} rps")
# caveat: the other 80% of orders (320,000) over the other 22 hours also overlap lunch
bg = orders_day * 0.80 / (22 * 3600)
print(f"if background orders continue at {bg:.2f}/s: in flight {(lam+bg)*dwell_s:,.0f}, total rps {(lam+bg)*dwell_s/refresh_s + lam + bg:,.1f}")
# instances at an assumed 150 rps each and 60% utilisation
inst = math.ceil(total_rps / (150 * 0.6))
print(f"instances at 150 rps x 60%: {total_rps/(150*0.6):.2f} -> {inst}")
# steady state is reached once the peak lasts longer than the dwell time
print(f"peak lasts {peak_hours*60} min vs dwell 35 min -> steady state reached")
assert peak_orders == 80_000 and round(lam, 2) == 11.11
assert round(L) == 23_333 and round(refresh_rps, 1) == 777.8 and round(total_rps, 1) == 788.9
assert round(refresh_rps / total_rps, 3) == 0.986
assert round(orders_day / 86_400 * dwell_s) == 9_722
assert round(L / 60 + lam, 1) == 400.0
assert round(bg, 2) == 4.04 and round((lam + bg) * dwell_s) == 31_818
assert inst == 9 and peak_hours * 60 > 35
