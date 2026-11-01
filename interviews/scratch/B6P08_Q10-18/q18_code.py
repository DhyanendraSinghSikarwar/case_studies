import math
from scipy import stats

daily, share = 2_000_000, 0.15
degraded = round(daily * share)
assert degraded == 300_000
err = 0.001
print("HTTP errors/day:", round(daily * err), "| degraded (200 OK, score 0.5):", degraded, "| ratio:", round(degraded / (daily * err)))
assert round(daily * err) == 2000 and round(degraded / (daily * err)) == 150
good = 1 - err - share
print("useful responses:", round(good * 100, 1), "% (an SLI that counts only HTTP success says 99.9%)")
assert round(good * 100, 1) == 84.9
# Alert design: degraded share per 5-minute window
per5 = daily / (24 * 12)
print("requests per 5 min:", round(per5))
assert round(per5) == 6944
base_rate = 0.001                                   # normal timeout rate 0.1% (illustrative)
mu = per5 * base_rate
thr_share = 0.01
thr_count = math.ceil(per5 * thr_share)
p_fa = stats.poisson.sf(thr_count - 1, mu)
print(f"normal mean {mu:.1f} per window; alert at >= {thr_count}; false-alarm prob per window {p_fa:.1e}")
assert thr_count == 70 and p_fa < 1e-12
# Time to detect at the incident rate: 15% over the 5-minute window
exp_inc = per5 * share
print("expected degraded in a 5-minute window during the incident:", round(exp_inc), "-> alert fires in the first window")
assert round(exp_inc) == 1042 and exp_inc > thr_count
# Detection delay: unknown (days) vs 5-10 minutes with the alert
print("detection delay with the alert: about 5-10 minutes")
# Cost of delay: degraded requests per hour at the incident rate
per_hour = daily / 24 * share
print("degraded requests per hour:", round(per_hour))
assert round(per_hour) == 12500
# Counting after the fact: log rows with fallback flag; score==0.5 alone over-counts if 0.5 can be legitimate
legit_rate = 0.0002
print("rows with score exactly 0.5 that are legitimate (illustrative 0.02%):", round(daily * legit_rate))
assert round(daily * legit_rate) == 400
