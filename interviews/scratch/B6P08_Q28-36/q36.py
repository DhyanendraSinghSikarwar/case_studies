# Illustrative numbers only. Detection delay for a silent monitor, retention clock for the backfill, and a monitor self-test.
import numpy as np
from scipy import stats
interval_h = 24
gap_days = 12
missed = gap_days                                         # one missed daily run per day
print('missed daily runs:', missed)
assert missed == 12
# Dead-man switch: alert if the newest successful run is older than 1.5 x interval.
threshold_h = 1.5 * interval_h
worst_detect_h = threshold_h                              # failure right after a success; first alert when age passes the threshold
print('worst-case detection delay with a dead-man switch (h):', worst_detect_h, 'vs actual', gap_days * 24)
assert worst_detect_h == 36 and gap_days * 24 == 288 and gap_days * 24 / worst_detect_h == 8.0
missed_with_switch = int(worst_detect_h // interval_h)    # runs missed before the first alert
assert missed_with_switch == 1
# Expiry warning would have fired well before the failure.
warn_days_before = 14
print('days before today that a 14-day expiry warning fires:', gap_days + warn_days_before)
assert gap_days + warn_days_before == 26
# Retention clock: can the gap still be backfilled? Prediction and input logs kept N days (illustrative).
for retention in (30, 14):
    oldest_age = gap_days                                 # age in days of the first uncovered day
    left = retention - oldest_age
    print(f'retention {retention} d: first uncovered day expires in {left} days')
assert 30 - gap_days == 18 and 14 - gap_days == 2
# Self-test of the monitor: inject a known shift, require the alert; run on every deploy and nightly.
def monitor(ref, cur, thr=0.10):
    d = stats.ks_2samp(ref, cur).statistic
    return d >= thr, d
rng = np.random.default_rng(36)
ref = rng.standard_normal(50_000)
fires, d_inj = monitor(ref, rng.standard_normal(50_000) + 0.5)          # synthetic shift of 0.5 sd
quiet, d_null = monitor(ref, rng.standard_normal(50_000))
print('injected shift D', round(d_inj, 3), 'fires', bool(fires), '| no shift D', round(d_null, 4), 'fires', bool(quiet))
assert fires and not quiet
# Backfill: re-run the job per day partition (idempotent), find when drift actually began inside the gap.
days = np.arange(1, gap_days + 1)
shift = np.where(days >= 6, 0.1 * (days - 5), 0.0)                       # drift began on gap day 6 and grew (invented)
Ds = [stats.ks_2samp(ref[:20_000], rng.standard_normal(20_000) + s).statistic for s in shift]
first = int(days[[d >= 0.10 for d in Ds].index(True)])
print('daily D over the gap:', [round(float(d), 2) for d in Ds])
print('first day over the 0.10 threshold:', first, '-> days of unwatched drift:', gap_days - first + 1)
assert first == 8 and gap_days - first + 1 == 5
# Dashboard: show 'as of' and turn red when stale.
def banner(age_h): return 'STALE' if age_h > threshold_h else 'ok'
assert banner(12) == 'ok' and banner(48) == 'STALE' and banner(288) == 'STALE'
