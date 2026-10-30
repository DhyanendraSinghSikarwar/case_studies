# Q11: seasonal/event error versus real drift (all numbers illustrative, seeded)
import numpy as np
rng = np.random.default_rng(11)

# Hand-check table: MAPE = |actual - forecast| / actual
for name, a, f, want in [("normal week", 1000, 880, 12.0), ("sale week", 1000, 780, 22.0), ("week after", 1000, 870, 13.0)]:
    m = 100 * abs(a - f) / a
    assert abs(m - want) < 1e-9
    print(f"{name:12} actual={a} forecast={f} MAPE={m:.1f}%  signed error={100*(f-a)/a:+.1f}%")

weeks = np.arange(156)                       # 3 years
event = np.isin(weeks % 52, [42, 43])        # two sale weeks a year
baseline = 1000 * (1 + 0.1 * np.sin(2 * np.pi * weeks / 52))   # known trend+season
S = 40                                       # 40 SKUs per week, error pooled across SKUs
noise = rng.lognormal(0, 0.15, size=(weeks.size, S))
uplift = np.where(event, 1.25, 1.0)          # sale lifts demand 25%
actual = (baseline * uplift)[:, None] * noise
fc_old = np.repeat(baseline[:, None], S, axis=1)                            # model without an event feature

def mape(a, f): return 100 * np.mean(np.abs(a - f) / a)
def bias(a, f): return 100 * np.mean((f - a) / a)

for y in range(3):
    s = slice(52 * y, 52 * (y + 1))
    ev, nev = event[s], ~event[s]
    print(f"year {y+1}: MAPE normal weeks {mape(actual[s][nev], fc_old[s][nev]):.1f}%, "
          f"sale weeks {mape(actual[s][ev], fc_old[s][ev]):.1f}%, bias in sale weeks {bias(actual[s][ev], fc_old[s][ev]):+.1f}%")

# Event-aware fix: learn the uplift from PAST sale weeks only (years 1-2), test on year 3
past = (weeks < 104) & event
learned = np.mean(actual[past] / baseline[past][:, None])
fc_new = (baseline * np.where(event, learned, 1.0))[:, None] * np.ones((1, S))
y3 = slice(104, 156)
ev3 = event[y3]
mo, mn = mape(actual[y3][ev3], fc_old[y3][ev3]), mape(actual[y3][ev3], fc_new[y3][ev3])
print(f"learned sale uplift = {learned:.2f}x; year-3 sale-week MAPE old {mo:.1f}% -> new {mn:.1f}%")
assert 1.15 < learned < 1.35 and mn < mo - 5

# Contrast: real drift = permanent +15% demand level shift from week 130 (not tied to an event)
actual_d = actual.copy()
actual_d[130:] *= 1.15
def rolling_bias(a, f, k=4):
    e = 100 * ((f - a) / a).mean(axis=1)
    return np.array([e[max(0, i - k + 1):i + 1].mean() for i in range(len(e))])
rb = rolling_bias(actual_d, fc_new)
post_event_weeks = [i for i in range(104, 130) if (i - 1) % 52 not in (42, 43) and i % 52 not in (42, 43, 44, 45)]
print(f"rolling 4-wk bias, quiet weeks before shift: mean {np.mean(rb[post_event_weeks]):+.1f}%")
print(f"rolling 4-wk bias, weeks 140-155 after shift: mean {np.mean(rb[140:156]):+.1f}%")
assert abs(np.mean(rb[post_event_weeks])) < 3 and np.mean(rb[140:156]) < -8
# Decision rule: sale-week error compared with same sale weeks last year, normal-week error compared with normal weeks
last_year = mape(actual[52:104][event[52:104]], fc_old[52:104][event[52:104]])
this_year = mape(actual[104:156][event[104:156]], fc_old[104:156][event[104:156]])
print(f"same-event comparison, old model: last year {last_year:.1f}% vs this year {this_year:.1f}% -> "
      f"{'no drift signal' if abs(this_year-last_year) < 6 else 'investigate'}")
assert abs(this_year - last_year) < 6
