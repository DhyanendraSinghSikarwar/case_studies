# Q46: week-over-week DAU by platform that does not lie (illustrative toy data)
import pandas as pd

days = pd.date_range("2026-01-05", "2026-01-18")            # Mon 5 Jan .. Sun 18 Jan
base = {"android": [100]*5 + [70, 60], "ios": [50, 52, 54, 56, 58, 40, 40]}  # Mon..Sun, each platform flat week over week
rows = []
for p, pat in base.items():
    for d in days:
        if p == "ios" and d == pd.Timestamp("2026-01-08"):    # tracking outage: no rows at all
            continue
        for i in range(pat[d.dayofweek]):
            rows.append((f"{p[0]}{d:%m%d}_{i}", p, d + pd.Timedelta(hours=12)))
ev = pd.DataFrame(rows, columns=["user_id", "platform", "ts"])
ev = ev[ev.ts < pd.Timestamp("2026-01-15")]                 # data cut: this week only through Wed 14 Jan

# 1) DAU = distinct users per platform per day, then a date spine so empty days are visible
dau = ev.assign(day=ev.ts.dt.normalize()).groupby(["platform", "day"]).user_id.nunique()
spine = pd.MultiIndex.from_product([["android", "ios"], pd.date_range("2026-01-05", "2026-01-14")], names=["platform", "day"])
dau_s = dau.reindex(spine, fill_value=0)
print("rows without spine:", len(dau), "| rows with spine:", len(dau_s))
assert len(dau) == 19 and len(dau_s) == 20
assert dau_s[("ios", pd.Timestamp("2026-01-08"))] == 0

# 2) week-over-week: lag by 7 DAYS (join on date - 7), not by 7 ROWS
s = dau_s.rename("dau").reset_index()
selfjoin = s.merge(s.assign(day=s.day + pd.Timedelta(days=7)), on=["platform", "day"], how="left", suffixes=("", "_prev"))
window = s.assign(dau_prev=s.groupby("platform").dau.shift(7))   # valid only because the spine makes rows = days
assert (selfjoin.dau_prev.fillna(-1).values == window.dau_prev.fillna(-1).values).all()
# without the spine, shift(7) rows picks the wrong day after the gap
nos = dau.rename("dau").reset_index()
nos["dau_prev_rows"] = nos.groupby("platform").dau.shift(7)
wrong = nos[(nos.platform == "ios") & (nos.day == "2026-01-13")].dau_prev_rows.iloc[0]
right = s[(s.platform == "ios") & (s.day == "2026-01-13")].merge(selfjoin, on=["platform", "day"]).dau_prev.iloc[0]
print("ios Tue 13 Jan, last week's value: shift(7 rows) =", wrong, "| join on date-7 =", right)
assert wrong == 50.0 and right == 52.0

# 3) the partial-week trap: this week has Mon-Wed only
w1 = dau_s.loc["android"].loc["2026-01-05":"2026-01-11"].mean()
w2_partial = dau_s.loc["android"].loc["2026-01-12":"2026-01-14"].mean()
naive = w2_partial / w1 - 1
w1_same = dau_s.loc["android"].loc["2026-01-05":"2026-01-07"].mean()
fair = w2_partial / w1_same - 1
print(f"android avg DAU: last full week {w1:.1f}, this week Mon-Wed {w2_partial:.1f}, naive WoW {naive:+.1%}")
print(f"like-for-like (Mon-Wed vs Mon-Wed): {fair:+.1%}")
assert round(w1, 1) == 90.0 and w2_partial == 100.0 and round(naive, 3) == 0.111 and fair == 0

# 4) gap visible on iOS: average with spine vs without
i_spine = dau_s.loc["ios"].loc["2026-01-05":"2026-01-11"].mean()
i_obs = dau.loc["ios"].loc["2026-01-05":"2026-01-11"].mean()
print(f"ios week-1 avg DAU: with spine {i_spine:.1f}, over observed rows only {i_obs:.1f}")
assert round(i_spine, 1) == 42.0 and round(i_obs, 1) == 49.0

# 5) timezone: same events, different day boundaries
tz = pd.DataFrame({"user_id": ["u"]*2, "ts": pd.to_datetime(["2026-01-05 20:00", "2026-01-06 02:00"])})
utc_days = tz.ts.dt.normalize().nunique()
ist_days = tz.ts.dt.tz_localize("UTC").dt.tz_convert("Asia/Kolkata").dt.normalize().nunique()
print("one user, two events: active days in UTC =", utc_days, "| in IST =", ist_days)
assert utc_days == 2 and ist_days == 1
