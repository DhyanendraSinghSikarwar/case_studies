# Illustrative numbers only. Replay duplicates, window self-healing, flips across a threshold, and a dedupe fix.
import random, collections
rate, replay_min, window_min = 50_000, 20, 60
dupes = rate * replay_min
normal_window = rate * window_min
assert dupes == 1_000_000 and normal_window == 3_000_000
print('peak inflation of the hourly total', round(dupes / normal_window, 4))
assert round(dupes / normal_window, 4) == 0.3333

# 1. Event-time sliding window: when do the duplicates age out? Minute-level sketch at full scale.
# Duplicates carry event times in [T0-20, T0). The window at time t holds event times in (t-60, t].
T0 = 0
def dup_in_window(t):
    lo, hi = max(t - window_min, T0 - replay_min), min(t, T0)
    return max(0, hi - lo) * rate
last_bad = max(t for t in range(0, 200) if dup_in_window(t) > 0)
print('last minute after restart with inflated total:', last_bad)
assert last_bad == 59 and dup_in_window(60) == 0
# So a true 60-minute event-time window heals within an hour of the restart.
# Reading inflated counts 2 hours later means the duplicates sit in a non-expiring state (running counter, or TTL on processing time).

# 2. Mini simulation at 1/100 scale: counter without dedupe versus dedupe by event_id.
rnd = random.Random(7)
users = 2000
events = [(i, rnd.randrange(users)) for i in range(3000)]        # 60 minutes of normal events at 50/min
replayed = events[-1000:]                                        # last 20 minutes replayed (1/100 of 1M)
assert len(replayed) == dupes // 1000
naive = collections.Counter(u for _, u in events + replayed)
seen, dedup = set(), collections.Counter()
for eid, u in events + replayed:
    if eid in seen: continue
    seen.add(eid); dedup[u] += 1
truth = collections.Counter(u for _, u in events)
assert dedup == truth
extra = sum(naive.values()) - sum(truth.values())
assert extra == 1000 and round(extra / sum(truth.values()), 4) == 0.3333
# 3. How many scores flipped? Rule: risk flag if orders_last_hour >= 3 (illustrative threshold).
thr = 3
flips = sum(1 for u in range(users) if (naive[u] >= thr) != (truth[u] >= thr))
print('users flagged correctly', sum(truth[u] >= thr for u in range(users)), 'flagged with inflated counts', sum(naive[u] >= thr for u in range(users)), 'flips', flips)
assert flips > 0 and all(naive[u] >= truth[u] for u in range(users))   # inflation only pushes counts up
# 4. Reconciliation check that would have caught it at the first run.
stream_total, batch_total = 4_000_000, 3_000_000
gap = (stream_total - batch_total) / batch_total
alert_if = 0.05
assert gap > alert_if and round(gap, 4) == 0.3333
check_every_min = 10
print('worst-case detection delay with a', check_every_min, 'minute reconciliation:', check_every_min, 'min vs 120 min actual')
assert check_every_min < 120
# 5. Repair scope: re-aggregate from the raw log for the window that touched duplicates.
repair_from_min = -replay_min - window_min       # first window that could contain any duplicate
repair_to_min = 120                              # until the fix is live (illustrative)
print('recompute event-time range (minutes relative to restart):', repair_from_min, 'to', repair_to_min)
assert repair_to_min - repair_from_min == 200
