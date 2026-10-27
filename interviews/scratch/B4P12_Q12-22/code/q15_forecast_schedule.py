"""Q15: nightly batch window simulation: full retrain nightly vs weekly retrain + nightly rescore (abstract units, seeded)."""
import random, heapq
random.seed(15)
SERIES = 12_000_000          # from Q14: 10 percent of 120M cells (invented)
TRAIN_S, SCORE_S = 0.02, 0.001   # invented seconds of one core per series
SHARDS = 2400
WINDOW_H = 4.0
FIXED_S = 20                 # per-shard startup: load data, model, write output (invented)
# shard sizes vary (big stores / SKU groups): seeded lognormal, rescaled to total
raw = [random.lognormvariate(0, 0.5) for _ in range(SHARDS)]
sizes = [int(SERIES * r / sum(raw)) for r in raw]

def makespan(per_series_s, workers):
    """Longest-processing-time-first onto `workers` identical cores. Returns hours."""
    jobs = sorted((FIXED_S + s * per_series_s for s in sizes), reverse=True)
    heap = [0.0] * workers
    for j in jobs:
        t = heapq.heappop(heap); heapq.heappush(heap, t + j)
    return max(heap) / 3600
def core_hours(per_series_s): return sum(FIXED_S + s * per_series_s for s in sizes) / 3600

pre = 0.30   # invented: freshness check + feature build + backtest + publish take 0.30 h of the window
print("shards:", SHARDS, " largest/smallest shard ratio:", round(max(sizes) / min(sizes), 1))
for name, per in (("full retrain + score nightly", TRAIN_S + SCORE_S), ("rescore only (weekly retrain)", SCORE_S)):
    ch = core_hours(per)
    need = None
    for w in range(1, 5000):
        if makespan(per, w) + pre <= WINDOW_H: need = w; break
    print(f"{name:32s} core-hours={ch:8.1f}  min workers for {WINDOW_H}h window (incl {pre}h fixed steps)={need}  makespan={makespan(per, need) + pre:.2f}h")
    if per == TRAIN_S + SCORE_S: full_ch = ch
    else: resc_ch = ch
week_full = 7 * full_ch
week_mix = 1 * (full_ch) + 6 * resc_ch
print(f"\nweekly core-hours: nightly full={week_full:.1f}  weekly retrain + nightly rescore={week_mix:.1f}  relative={week_mix/week_full:.2f}")
assert week_mix < week_full
