rows, hours_now, hours_limit = 2_000_000, 5.0, 2.0
now_rate = rows / hours_now
need_rate = rows / hours_limit
speedup = need_rate / now_rate
print(f"now {now_rate:,.0f} rows/h, need {need_rate:,.0f} rows/h, speedup needed {speedup:.2f}x")
assert now_rate == 400_000 and need_rate == 1_000_000 and abs(speedup - 2.5) < 1e-12
# Amdahl: a share f of the 5 hours is optimisable by factor s (illustrative profile)
def runtime(f, s):
    return hours_now * ((1 - f) + f / s)
print("share f  speedup s  runtime(h)  meets 2h?  meets 1.6h (20% margin)?")
for f, s in [(0.5, 10), (0.7, 10), (0.7, 3), (0.9, 4), (0.9, 100)]:
    t = runtime(f, s)
    print(f"{f:7.0%}  {s:8d}  {t:10.2f}  {str(t <= 2.0):9}  {t <= 1.6}")
assert abs(runtime(0.7, 10) - 1.85) < 1e-9 and runtime(0.7, 10) <= 2.0
assert runtime(0.5, 10) > 2.0          # half the time is untouchable: ceiling is 2.5 h
assert abs(runtime(0.5, 1e9) - 2.5) < 1e-6
# smallest share that must be optimised (10x) to reach 1.6 h
f_need = (1 - 1.6 / hours_now) / (1 - 1 / 10)
print(f"with a 10x fix, at least {f_need:.1%} of runtime must be in the part you fix to hit 1.6 h")
assert abs(f_need - 0.7556) < 1e-3
# parity gate: a rewrite is accepted only if scores match the notebook
import numpy as np
rng = np.random.default_rng(7)
old = rng.random(100_000)
new = old + rng.normal(0, 1e-9, old.shape)      # a faithful rewrite
bad = old.copy(); bad[:500] += 0.2              # a rewrite with a bug in 0.5% of rows
tol = 1e-6
print("faithful rewrite max diff", f"{np.abs(old-new).max():.1e}", "| buggy rewrite rows off:", int((np.abs(old-bad) > tol).sum()))
assert np.abs(old - new).max() < tol and int((np.abs(old - bad) > tol).sum()) == 500
