# Illustrative numbers only. Wave sizes, exposure, and a hidden hour/segment bug that global metrics cannot see.
shares = {'R1': 40, 'R2': 25, 'R3': 15, 'R4': 10, 'R5': 6, 'R6': 4}   # percent of all requests
assert sum(shares.values()) == 100
# Smallest region first; the 40% region is split so the last step is never a 40% jump.
waves = [('W1 R6', 4), ('W2 +R5', 6), ('W3 +R4', 10), ('W4 +R3', 15), ('W5 +R2', 25), ('W6 +half R1', 20), ('W7 rest of R1', 20)]
cum, tot = [], 0
for name, s in waves:
    tot += s; cum.append(tot)
print('cumulative exposure %:', cum)
assert cum == [4, 10, 20, 35, 60, 80, 100]
steps = [b / a for a, b in zip(cum, cum[1:])]
print('growth factor per wave:', [round(x, 2) for x in steps])
assert max(steps) == 2.5 and cum[0] == shares['R6']
dwell_h = 24
print('days to complete with a 24 h dwell per wave:', len(waves) * dwell_h / 24)
assert len(waves) * dwell_h / 24 == 7
# Hidden bug: only customer type X, only in one hour of the day (e.g. 18:00 local).
daily = 10_000_000                                  # requests per day (illustrative)
x_share = {'R1': 0.04, 'R2': 0.03, 'R3': 0.03, 'R4': 0.02, 'R5': 0.01, 'R6': 0.005}   # share of X inside each region
def affected(regions):                               # requests per day hit by the bug if those regions are live
    return sum(daily * shares[r] / 100 * x_share[r] / 24 for r in regions)
full = affected(shares)
w1 = affected(['R6'])
print('bad requests per day, full rollout:', round(full), 'in wave 1:', round(w1))
assert round(w1) == 83 and 11_000 < full < 14_000
# Global view: bad rate is tiny and cannot be seen against noise.
bad_rate_global = full / daily
print('global bad-request rate at full rollout', round(bad_rate_global * 100, 3), '%')
assert bad_rate_global < 0.0015
alert_global = 0.005                                # 0.5% global error alert (illustrative)
assert bad_rate_global < alert_global               # never fires
# Segment view: inside (type X, hour 18) every request is bad, so the segment rate is 100%.
seg_n_day_w1 = daily * 0.04 * 0.005 / 24            # requests per day in the segment during wave 1
min_n = 200                                         # minimum requests before a segment is judged
days_needed = min_n / seg_n_day_w1
print('segment requests per day in wave 1', round(seg_n_day_w1), 'days to reach', min_n, ':', round(days_needed, 1))
assert round(seg_n_day_w1) == 83 and 2.3 < days_needed < 2.5
# Wave 2 adds R5 and the sample grows.
seg_w2 = seg_n_day_w1 + daily * 0.06 * 0.01 / 24
print('wave 2 segment requests per day', round(seg_w2), 'days to reach', min_n, ':', round(min_n / seg_w2, 2))
assert min_n / seg_w2 < 1
# Rule: advance only when (a) one full 24 h cycle has passed and (b) every watched segment has >= min_n requests.
def can_advance(hours, seg_counts):
    return hours >= 24 and all(c >= min_n for c in seg_counts.values())
assert not can_advance(24, {'X@18': 83}) and can_advance(72, {'X@18': 250}) and not can_advance(10, {'X@18': 900})
# Halt rules (illustrative): per segment, decision changed vs the old threshold above 5% with n >= 200, or global error +0.2 pt.
halt = lambda seg_rate, n: n >= min_n and seg_rate > 0.05
assert halt(1.0, 250) and not halt(1.0, 83)
# Blast radius = exposure share x hours to detect x severity. Compare detecting at wave 1 versus after full rollout.
hours_to_detect = 72
print('requests exposed at wave 1 over 72 h:', round(w1 * hours_to_detect / 24), 'vs full rollout:', round(full * hours_to_detect / 24))
assert round(w1 * 3) == 250 and round(full * 3) > 30_000
