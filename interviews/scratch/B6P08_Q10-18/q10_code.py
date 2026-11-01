import numpy as np

rng = np.random.default_rng(10)
days, bad_days, per_day = 90, 2, 1000          # illustrative: 1,000 orders a day
share_days = bad_days / days
assert round(share_days * 100, 1) == 2.2

# Training table: lognormal order values around 850 rupees; last 2 days are in paise
day = np.repeat(np.arange(days), per_day)
val = rng.lognormal(mean=np.log(850), sigma=0.4, size=day.size)
raw = val.copy()
bad = day >= days - bad_days
raw[bad] *= 100
share_rows = bad.mean()
assert abs(share_rows - share_days) < 1e-12     # equal volume per day: row share = day share
print("bad share of days/rows:", round(share_days * 100, 2), "%")
print("median clean/raw:", round(float(np.median(val))), round(float(np.median(raw))))
print("mean   clean/raw:", round(float(val.mean())), round(float(raw.mean())))
assert raw.mean() / val.mean() > 3             # 2.2% of rows moves the mean 3x
assert abs(np.median(raw) / np.median(val) - 1) < 0.02   # the median barely moves

# Repair: divide the affected partitions by 100, only because the window is known exactly
fixed = raw.copy()
fixed[bad] /= 100
assert np.allclose(fixed, val)
print("repair restores the table:", bool(np.allclose(fixed, val)))

# Contract check at ingestion: compare each day's median with the trailing 14-day median
def first_alarm(values_by_day, ratio=5.0, k=14):
    meds = [np.median(values_by_day[day == d]) for d in range(days)]
    for d in range(k, days):
        base = np.median(meds[d - k:d])
        if meds[d] > ratio * base or meds[d] < base / ratio:
            return d
    return None
a = first_alarm(raw)
assert a == days - bad_days                    # alarm on the first bad day
delay_hours_daily = 24          # daily batch check: at most one day
delay_hours_caught = bad_days * 24
print("first alarm day index:", a, "| detection delay with the check <= 24 h vs", delay_hours_caught, "h without")
assert delay_hours_caught == 48

# Served predictions: a linear-in-log model sees log(85000)-log(850) = ln(100) extra
ln100 = np.log(100)
print("extra log-value fed to the model:", round(float(ln100), 2))
assert round(float(ln100), 2) == 4.61
# Suppose the model's log-odds weight on log(order_value) is 0.3 (illustrative):
shift = 0.3 * ln100
print("log-odds shift for a typical order:", round(float(shift), 2))
assert round(float(shift), 2) == 1.38
