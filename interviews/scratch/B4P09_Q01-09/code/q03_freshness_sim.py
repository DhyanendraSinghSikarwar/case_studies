# Q3: rolling 7-day count, refreshed daily vs hourly vs per event. Pure Python, seeded.
import bisect, random, statistics
H = 3600.0; DAY = 24 * H; WIN = 7 * DAY
rng = random.Random(7)

# ~3 events per day for 30 days (exponential gaps), timestamps in seconds
events, t = [], 0.0
while t < 30 * DAY:
    t += rng.expovariate(3 / DAY); events.append(t)

def count_7d(at):                      # truth: events in (at - 7d, at]
    return bisect.bisect_right(events, at) - bisect.bisect_right(events, at - WIN)

# 300 prediction requests, days 10..30
preds = sorted(rng.uniform(10 * DAY, 30 * DAY) for _ in range(300))

def run(period):                       # batch job runs every `period` seconds, serves its last output
    stale, err = [], []
    for p in preds:
        computed_at = (p // period) * period if period else p
        served = count_7d(computed_at)
        stale.append(p - computed_at); err.append(abs(served - count_7d(p)))
    return statistics.mean(stale) / H, max(stale) / H, statistics.mean(err), max(err), sum(e > 0 for e in err) / len(err)

print(f"{len(events)} events in 30 days; {len(preds)} prediction requests")
print(f"{'route':<18}{'mean stale (h)':>15}{'max stale (h)':>15}{'mean abs err':>14}{'max abs err':>13}{'share wrong':>13}")
for name, period in [("daily batch", DAY), ("hourly batch", H), ("per event/stream", 0)]:
    ms, xs, me, xe, sw = run(period)
    print(f"{name:<18}{ms:>15.2f}{xs:>15.2f}{me:>14.2f}{xe:>13d}{sw:>13.0%}")

# on-demand features: only the request has the data
def seconds_since_login(last_login_ts, now): return now - last_login_ts
def country_match(ship, bill): return int(ship == bill)
print("\non-demand examples:", seconds_since_login(1000.0, 1042.5), country_match("IN", "IN"), country_match("IN", "AE"))
