import math
# Q7 forecasting batch: illustrative numbers from the prompt
stores, per_store, window_h, worker_rate = 300, 4_000, 3, 10
series = stores * per_store
window_s = window_h * 3600
need = series / window_s
workers_exact = need / worker_rate
workers = math.ceil(workers_exact)
util = series / (workers * worker_rate * window_s)
print(f"series {series:,}; window {window_s:,} s; need {need:.2f} series/s; workers {workers_exact:.2f} -> {workers}")
print(f"with {workers} workers batch uses {util:.1%} of the window; spare {workers*worker_rate*window_s - series:,} series-slots")
w30 = math.ceil(workers_exact * 1.3)
print(f"with 30% headroom for retries and slow nodes: {w30} workers")
intermittent = int(series * 0.40)
print(f"intermittent series {intermittent:,}; regular {series-intermittent:,}; output rows {series*14:,}")
# if intermittent series take twice as long per series (illustrative), blended rate falls
blend_time = 0.6 * 1 + 0.4 * 2          # relative time per series
print(f"if intermittent cost 2x, blended rate {worker_rate/blend_time:.2f}/s -> workers {math.ceil(need/(worker_rate/blend_time))}")
assert series == 1_200_000 and window_s == 10_800 and round(need, 2) == 111.11
assert round(workers_exact, 2) == 11.11 and workers == 12 and round(util, 3) == 0.926
assert w30 == 15 and intermittent == 480_000 and series * 14 == 16_800_000
assert math.ceil(need / (worker_rate / blend_time)) == 16 and round(worker_rate / blend_time, 2) == 7.14
