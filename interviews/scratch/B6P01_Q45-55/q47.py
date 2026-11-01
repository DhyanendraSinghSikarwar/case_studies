# Q47: late-arriving events make the newest hours look like a dip (illustrative simulation)
import numpy as np
rng = np.random.default_rng(47)

HOURS = 24 * 8                       # 8 days of hourly data
PER_HOUR = 1000                      # true events per hour (flat on purpose: any dip is fake)
n = rng.poisson(PER_HOUR, HOURS)
event_h = np.repeat(np.arange(HOURS), n) + rng.random(n.sum())          # event time in hours
offline = rng.random(n.sum()) < 0.30                                    # 30% sit on the phone first
lag_h = np.where(offline, rng.exponential(2.0, n.sum()), rng.exponential(0.05, n.sum()))
ingest_h = event_h + lag_h                                              # when the warehouse sees it
print("lag percentiles in hours p50/p90/p99:", np.round(np.percentile(lag_h, [50, 90, 99]), 2))

def visible_per_hour(now_h):
    """what the dashboard shows at time now_h: events ingested by then, bucketed by EVENT hour"""
    m = ingest_h <= now_h
    return np.bincount(event_h[m].astype(int), minlength=HOURS)[:HOURS]

# dashboard viewed at 23:30 on the last full day (day index 6): look at its last hours
now = 24 * 7 - 0.5
shown = visible_per_hour(now)
final = visible_per_hour(1e9)
last = range(24 * 7 - 6, 24 * 7 - 1)       # completed hours 18..22; hour 23 is still in progress at 23:30
print("hour 23 is still running at 23:30, so only half of it can exist:", shown[24*7-1], "of", final[24*7-1])
print("hour-of-day | shown at 23:30 | final next morning | shown/final")
for h in last:
    print(f"{h % 24:>11} | {shown[h]:>14} | {final[h]:>18} | {shown[h] / final[h]:.2f}")
ratio = np.array([shown[h] / final[h] for h in last])
assert ratio[-1] < 0.85 and ratio[0] > 0.9 and ratio[-1] == ratio.min()   # newest completed hour is the thinnest
assert abs(final[24*7 - 2] / PER_HOUR - 1) < 0.1                               # truth is flat: ~1000

# confirm the cause: completeness by age, learned from earlier days
ages = np.array([0.5, 1, 2, 4, 6, 12])
comp = np.array([np.mean(lag_h <= a) for a in ages])
print("share of events visible by age (h):", dict(zip(ages.tolist(), np.round(comp, 3).tolist())))
assert comp[0] < 0.9 and comp[-1] > 0.99

# fix 1: only report hours older than the p99 lag (the watermark)
p99 = np.percentile(lag_h, 99)
print("watermark age (h) to report at p99 completeness:", round(float(p99), 1))
# fix 2: nowcast = shown / completeness(age), with an interval flag, for alerting
def comp_at(age): return np.mean(lag_h <= age)
est = [shown[h] / comp_at(now - (h + 0.5)) for h in last]
err = [abs(e / final[h] - 1) for e, h in zip(est, last)]
print("nowcast error vs final by hour:", np.round(err, 3).tolist())
assert max(err) < 0.1
