# Q39: 95% on-time objective over 28 daily runs (invented numbers)
import math

N, TARGET = 28, 0.95
allowed = math.floor(N * (1 - TARGET) + 1e-9)       # whole misses allowed
exact = N * (1 - TARGET)
print("budget (fractional misses):", round(exact, 2), "-> whole misses allowed:", allowed)
assert round(exact, 2) == 1.4 and allowed == 1
print("1 miss ->", round(27 / 28, 4), "| 2 misses ->", round(26 / 28, 4), "(below 0.95)")
assert 27 / 28 >= TARGET and 26 / 28 < TARGET

misses = 3
on_time = N - misses
print("actual on-time", on_time, "/", N, "=", round(on_time / N, 4))
assert on_time == 25 and round(on_time / N, 3) == 0.893
print("budget used", round(misses / exact, 2), "of the budget (", round(misses / exact * 100), "%)")
assert round(misses / exact, 2) == 2.14
print("overspend: ", misses - allowed, "whole misses over the allowed 1")
assert misses - allowed == 2

# When does the budget come back? Rolling 28-day window; invented miss days.
miss_days = [3, 10, 20]
for today in (28, 31, 38, 48):
    in_win = [d for d in miss_days if today - 27 <= d <= today]
    ok = len(in_win) <= allowed
    print(f"day {today}: misses in window {len(in_win)} -> within objective: {ok}")
assert [len([d for d in miss_days if t - 27 <= d <= t]) for t in (28, 31, 38, 48)] == [3, 2, 1, 0]

# A lateness SLO says nothing about wrongness. Same 28 runs, all on time, one silently bad.
runs = [{"on_time": True, "null_rate": 0.01} for _ in range(N)]
runs[17] = {"on_time": True, "null_rate": 0.31}     # an upstream column went mostly null
lateness_ok = sum(r["on_time"] for r in runs) / N
quality_ok = sum(r["null_rate"] <= 0.05 for r in runs) / N      # a data-quality objective
print("lateness objective:", lateness_ok, "| data-quality objective:", round(quality_ok, 3))
assert lateness_ok == 1.0 and round(quality_ok, 3) == 0.964
assert quality_ok >= 0.95 and (N - 2) / N < 0.95
