# Q8: feature table 210 minutes late; the scoring job silently used yesterday's partition. Illustrative; seeded.
from datetime import date, datetime, timedelta
import numpy as np

# prompt arithmetic
due, landed, scored = datetime(2026, 10, 31, 6, 0), datetime(2026, 10, 31, 9, 30), datetime(2026, 10, 31, 7, 0)
late_min = (landed - due) / timedelta(minutes=1)
assert late_min == 210
print("late by", int(late_min), "min; scoring ran", int((due + timedelta(hours=1) - due) / timedelta(minutes=1)), "min after the due time but", int((landed - scored) / timedelta(minutes=1)), "min before the data existed")
assert (landed - scored) / timedelta(minutes=1) == 150

# illustrative recovery timeline: rescoring takes 25 min for 1,000,000 customers; start 5 min after landing
rescore_start = landed + timedelta(minutes=5); rescore_end = rescore_start + timedelta(minutes=25)
exposure_min = (rescore_end - scored) / timedelta(minutes=1)
print("stale scores existed from 07:00 to", rescore_end.strftime("%H:%M"), "=", int(exposure_min), "min")
assert rescore_end.strftime("%H:%M") == "10:00" and exposure_min == 180

# how different are one-day-old features? Simulate scores with day-to-day correlation rho (an ASSUMPTION; measure it for real)
rng = np.random.default_rng(8)
N = 1_000_000
for rho in (0.99, 0.95, 0.80):
    s_old = rng.normal(size=N)
    s_new = rho * s_old + np.sqrt(1 - rho**2) * rng.normal(size=N)
    top_old = s_old >= np.quantile(s_old, 0.90); top_new = s_new >= np.quantile(s_new, 0.90)
    wrong = int((top_old != top_new).sum())          # customers wrongly in or out of the top 10% target list
    print(f"rho={rho}: customers whose top-10% membership differs = {wrong:,} ({wrong/N:.1%})")
    if rho == 0.95: w95 = wrong
assert 20_000 < w95 < 70_000        # a 'small' 1-day lag still misplaces tens of thousands of customers at rho 0.95

# what makes it fail loudly: freshness assertion on the INPUT, and lineage on the OUTPUT
def pick_partition(available, run_date):
    if run_date not in available:
        raise RuntimeError(f"feature partition {run_date} missing (latest is {max(available)}); refusing to score")
    return run_date
today, yday = date(2026, 10, 31), date(2026, 10, 30)
try:
    pick_partition({yday}, today); raise SystemExit("must fail")
except RuntimeError as e:
    print("job now fails:", e)
assert pick_partition({yday, today}, today) == today

def check_output(rows, expected_date, expected_n, tol=0.01):
    bad = [r for r in rows if r["feature_date"] != expected_date]
    assert not bad, f"{len(bad)} rows carry stale feature_date"
    assert abs(len(rows) - expected_n) / expected_n <= tol, "row count off"
    return "ok"
good = [{"customer": i, "feature_date": today} for i in range(1000)]
stale = [{"customer": i, "feature_date": yday} for i in range(1000)]
assert check_output(good, today, 1000) == "ok"
try: check_output(stale, today, 1000); raise SystemExit("must fail")
except AssertionError as e: print("output check:", e)

# sensor alert: table not landed by 06:30 (30 min grace) pages the data owner; shows detection at 06:30 instead of 09:30+
alert_at = due + timedelta(minutes=30)
print("alert time:", alert_at.strftime("%H:%M"), "-> alert fires", int((landed - alert_at) / timedelta(minutes=1)), "min before the table lands")
assert alert_at.strftime("%H:%M") == "06:30"
