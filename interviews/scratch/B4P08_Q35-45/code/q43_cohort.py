import numpy as np
# Matured-cohort recall: labels arrive 30-90 days after the event, so today's cohort is unlabelled.
rng = np.random.default_rng(43)
days, per = 200, 20000
rec = []
for d in range(days):
    fraud = rng.random(per) < 0.01
    caught = fraud & (rng.random(per) < (0.80 if d < 120 else 0.60))   # real recall drops from day 120
    delay = rng.integers(30, 91, per)
    rec += [(d, f, c, dl) for f, c, dl in zip(fraud, caught, delay)]
d_, f_, c_, dl_ = map(np.array, zip(*rec))
today = 199
def recall_cohort(day):  # what we know today about the cohort of that day
    m = (d_ == day) & f_ & (day + dl_ <= today)
    return (c_[m].sum() / max(m.sum(), 1)), int(m.sum())
for day in (60, 110, 130, 150):
    r, n = recall_cohort(day)
    known = ((d_ == day) & f_ & (day + dl_ <= today)).sum() / max(((d_ == day) & f_).sum(), 1)
    print(f"cohort day {day}: share of its fraud labelled by day {today}: {known:.2f}  recall on labelled part: {("%.2f" % r) if n else "n/a"} (n={n})")
