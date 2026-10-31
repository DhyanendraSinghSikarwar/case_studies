# Q19: static "20% below" volume alert versus a calendar-aware alert. Synthetic, seeded, illustrative.
import numpy as np
rng = np.random.default_rng(19)
WEEKS, H = 9, 168
shape = 1000 * (0.55 + 0.45 * np.sin(np.pi * (np.arange(24) - 4) / 20).clip(0))   # day curve
HOLIDAYS = {37, 45}       # two weekday holidays (day index) inside the eval window
def is_off(d): return d % 7 in (5, 6) or d in HOLIDAYS
vol = np.zeros(WEEKS * H)
for d in range(WEEKS * 7):
    f = 0.6 if is_off(d) else 1.0
    vol[d*24:(d+1)*24] = shape * f * rng.normal(1, 0.03, 24)
OUT1 = (38*24 + 11, 38*24 + 14)      # day 38 is a Friday, 11:00-14:00 (3 hours)
OUT2 = (57*24 + 18, 57*24 + 21)      # day 57 is a Tuesday 18:00-21:00 (3 hours)
for a, b in (OUT1, OUT2): vol[a:b] *= 0.35
START = 5 * H                        # evaluate the last 4 weeks (28 days, 672 hours)
def episodes(fire):
    eps, i = [], START
    while i < len(fire):
        if fire[i]:
            j = i
            while j + 1 < len(fire) and fire[j + 1]: j += 1
            eps.append((i, j)); i = j + 1
        else: i += 1
    return eps
# OLD rule: below 80% of the mean of the same hour over the previous 7 days (all day types mixed)
old = np.zeros(len(vol), bool)
for t in range(START, len(vol)):
    base = np.mean([vol[t - 24*k] for k in range(1, 8)])
    old[t] = vol[t] < 0.8 * base
# NEW rule: baseline = median of same hour, same day type, previous 28 days (needs >=4 samples)
new = np.zeros(len(vol), bool); ratio = np.full(len(vol), np.nan)
for t in range(START, len(vol)):
    d, h = divmod(t, 24)
    same = [vol[(k*24)+h] for k in range(d - 28, d) if k >= 0 and is_off(k) == is_off(d)]
    if len(same) < 4: continue
    ratio[t] = vol[t] / np.median(same)
for t in range(START, len(vol)):
    if np.isnan(ratio[t]): continue
    deep = ratio[t] < 0.5                                   # tier 1: page at once
    mild = ratio[t] < 0.75 and t > 0 and ratio[t-1] < 0.75  # tier 2: two hours in a row
    new[t] = deep or mild
real = [OUT1, OUT2]
def report(name, fire):
    eps = episodes(fire)
    caught = sum(any(s <= a < e + 1 or (a <= s < b) for s, e in eps) for a, b in real)
    new_pages = [e for e in eps if any(a <= e[0] < b for a, b in real)]
    delays = [e[0] - a for e in eps for a, b in real if a <= e[0] < b]
    print(f"{name}: pages={len(eps)} real_caught={len(new_pages)}/2 precision={len(new_pages)/len(eps):.0%} delays_h={delays}")
    return len(eps), len(new_pages), delays
n_old, c_old, d_old = report("OLD static", old)
n_new, c_new, d_new = report("NEW calendar", new)
assert c_old == 2 and c_new == 2          # both rules still page on both outages
assert n_new == 2 and d_new == [0, 0]     # new rule: only the 2 real pages, caught in the first outage hour
assert n_old == 10 and n_old == 5 * n_new   # old rule: 10 pages, 8 of them weekend or holiday noise
# the prompt's own arithmetic
assert round(2 / 11, 3) == 0.182 and 9 + 2 == 11
# weekend outage test for the new rule: inject a 3-hour drop on a Saturday (day 47)
v2 = vol.copy(); v2[47*24+18:47*24+21] *= 0.35
r2 = np.full(len(v2), np.nan)
for t in range(46*24, 48*24):
    d, h = divmod(t, 24)
    same = [v2[k*24+h] for k in range(d - 28, d) if is_off(k) == is_off(d)]
    r2[t] = v2[t] / np.median(same)
assert (r2[47*24+18:47*24+21] < 0.5).all() and (r2[46*24:47*24+18][~np.isnan(r2[46*24:47*24+18])] > 0.75).all()
print("weekend outage ratio:", np.round(r2[47*24+18:47*24+21], 2), "-> pages under NEW rule")
# per-page budget: 4 weeks, tolerate at most 2 noise pages
print("old pages per 28 days:", n_old, "| new pages per 28 days:", n_new)
