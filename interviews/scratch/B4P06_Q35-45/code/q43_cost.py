"""Serving cost calculator. EVERY number below is INVENTED for the demo (units: 'cu' = made-up currency units)."""
import math
from dataclasses import dataclass

@dataclass(frozen=True)
class Realtime:
    price_per_hour: float      # cost of one replica for one hour
    rps_per_replica: float     # sustainable requests/s at 100% busy (measured by you in real life)
    target_util: float         # keep below 1.0 so p99 does not blow up (queueing)
    min_replicas: int = 1

@dataclass(frozen=True)
class Batch:
    price_per_hour: float
    preds_per_sec: float       # batch throughput of one worker (big batches, so higher than online)
    spot_factor: float = 1.0   # 0.4 means spot costs 40% of on-demand (invented); batch only
    overhead_hours: float = 0.25   # startup + load + write results, billed

def replicas_needed(rps, rt):
    return max(rt.min_replicas, math.ceil(rps / (rt.rps_per_replica * rt.target_util)))

def realtime_static_cost_per_day(avg_rps, peak_to_avg, rt):
    """Provision for the peak all day (no autoscaling)."""
    n = replicas_needed(avg_rps * peak_to_avg, rt)
    return n * rt.price_per_hour * 24, n

def realtime_autoscaled_cost_per_day(avg_rps, rt, scale_headroom=1.3):
    """Replicas follow the average load plus headroom for scale-up lag; floor at min_replicas."""
    n = max(rt.min_replicas, math.ceil(avg_rps * scale_headroom / (rt.rps_per_replica * rt.target_util)))
    return n * rt.price_per_hour * 24, n

def batch_cost_per_day(preds_per_day, b, workers=1):
    hours = preds_per_day / (b.preds_per_sec * 3600 * workers) + b.overhead_hours
    return hours * workers * b.price_per_hour * b.spot_factor

def per_1000(cost_per_day, preds_per_day):
    return 1000 * cost_per_day / preds_per_day

def utilisation(avg_rps, replicas, rt):
    return avg_rps / (replicas * rt.rps_per_replica)

def breakeven_runs_per_day(always_on_cost_per_day, preds_per_run, b, workers=1):
    """How many batch runs per day (each scoring preds_per_run rows) cost the same as keeping the real-time service on.
    Fewer runs than this: batch is cheaper. More runs (fresher scores): always-on is cheaper."""
    one_run = batch_cost_per_day(preds_per_run, b, workers)      # cost of one run, overhead included
    return always_on_cost_per_day / one_run

if __name__ == "__main__":
    cpu = Realtime(price_per_hour=1.0, rps_per_replica=50, target_util=0.6)
    gpu = Realtime(price_per_hour=6.0, rps_per_replica=600, target_util=0.6)
    bcpu = Batch(price_per_hour=1.0, preds_per_sec=400, spot_factor=0.4)
    avg_rps, ratio = 20, 4                                          # average 20 req/s, peak 80 req/s
    day = avg_rps * 86400
    print(f"traffic: avg {avg_rps} rps, peak/avg {ratio}, {day:,} predictions/day (all numbers invented)")
    print(f"{'option':34s}{'replicas':>9s}{'cost/day':>10s}{'cu per 1000':>13s}{'avg util':>10s}")
    for name, cost, n, rt in [("CPU real-time, sized for peak", *realtime_static_cost_per_day(avg_rps, ratio, cpu), cpu),
                              ("CPU real-time, autoscaled", *realtime_autoscaled_cost_per_day(avg_rps, cpu), cpu),
                              ("GPU real-time, sized for peak", *realtime_static_cost_per_day(avg_rps, ratio, gpu), gpu)]:
        print(f"{name:34s}{n:9d}{cost:10.1f}{per_1000(cost, day):13.4f}{utilisation(avg_rps, n, rt):10.1%}")
    bc = batch_cost_per_day(day, bcpu); print(f"{'CPU nightly batch on spot':34s}{'1 job':>9s}{bc:10.1f}{per_1000(bc, day):13.4f}{'n/a':>10s}")
    one_always_on = cpu.price_per_hour * 24
    for rows in (1_728_000, 50_000_000):
        r = breakeven_runs_per_day(one_always_on, rows, bcpu, workers=math.ceil(rows / (bcpu.preds_per_sec * 3600 * 6)))
        print(f"scoring {rows:>10,} rows per run (workers sized to finish in ~6h): batch = always-on CPU replica ({one_always_on:.0f} cu/day) at {r:.1f} runs/day")
    print("  nightly = 1 run/day, hourly = 24 runs/day. Real-time is the only choice when a user waits for the answer.")
