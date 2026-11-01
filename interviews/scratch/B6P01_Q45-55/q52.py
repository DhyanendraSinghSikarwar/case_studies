# Q52: push CTR +25% from urgent wording. Does it help? (illustrative numbers, seeded)
import numpy as np
rng = np.random.default_rng(52)

# 1) CTR is a ratio on pushes SENT, not value. 3 arms, 100k users each, 4 weeks.
N = 100_000
ctr_old, ctr_new = 0.040, 0.050
assert round(ctr_new / ctr_old - 1, 2) == 0.25

# incremental sessions per user per week: holdout (no push) vs old wording vs urgent wording
base_rate = 3.0                                 # sessions/user/week with no push
sess_h = rng.poisson(base_rate, N)
sess_a = rng.poisson(base_rate + 0.30, N)       # old wording adds 0.30 sessions
sess_b = rng.poisson(base_rate + 0.32, N)       # urgent wording: CTR up 25% but only +0.02 more incremental sessions
def diff_ci(x, y):
    d = x.mean() - y.mean()
    se = np.sqrt(x.var(ddof=1)/len(x) + y.var(ddof=1)/len(y))
    return d, 1.96 * se
for name, a, b in (("old vs holdout", sess_a, sess_h), ("urgent vs holdout", sess_b, sess_h), ("urgent vs old", sess_b, sess_a)):
    d, h = diff_ci(a, b)
    print(f"{name}: {d:+.3f} sessions/user/week, 95% CI +/- {h:.3f}")
d_ba, h_ba = diff_ci(sess_b, sess_a)
assert abs(d_ba) < 0.1 and diff_ci(sess_a, sess_h)[0] > 0.25          # pushes add sessions; urgency adds little beyond that

# 2) what the CTR hides: opt-outs shrink reach over time
sends_per_week = 5
d_old, d_new = 0.003, 0.010                      # weekly share of users who turn pushes off
value_per_click_old, value_per_click_new = 1.00, 0.85   # urgent-click sessions are shallower (assumption)
def cum_value(ctr, drop, vpc, weeks):
    reach = (1 - drop) ** np.arange(weeks)
    return float(np.sum(sends_per_week * ctr * vpc * reach))
for w in (4, 12, 52, 104):
    a = cum_value(ctr_old, d_old, value_per_click_old, w)
    b = cum_value(ctr_new, d_new, value_per_click_new, w)
    print(f"{w:>3} weeks: value per starting user old {a:6.2f}, urgent {b:6.2f}, urgent/old {b/a:.2f}")
cross = next(w for w in range(1, 600) if cum_value(ctr_new, d_new, value_per_click_new, w) < cum_value(ctr_old, d_old, value_per_click_old, w))
print("urgent wording falls behind cumulatively after week", cross)
assert cum_value(ctr_new, d_new, value_per_click_new, 4) > cum_value(ctr_old, d_old, value_per_click_old, 4)
assert cum_value(ctr_new, d_new, value_per_click_new, 104) < cum_value(ctr_old, d_old, value_per_click_old, 104)
