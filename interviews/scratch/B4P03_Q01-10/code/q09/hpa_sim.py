"""HPA formula with tolerance, min/max clamp and a scale-down stabilisation window."""
import math

def desired(current, metric, target, tol=0.10, lo=2, hi=10):
    ratio = metric / target
    if abs(ratio - 1.0) <= tol:                 # inside the dead band: do nothing
        d = current
    else:
        d = math.ceil(current * ratio)
    return max(lo, min(hi, d))

print("hand example: 4 pods, 90% vs 60% ->", desired(4, 90, 60))          # ceil(4*1.5)=6
print("tolerance   : 4 pods, 63% vs 60% ->", desired(4, 63, 60), "(ratio 1.05, no change)")
print("clamp high  : 8 pods, 150% vs 60% ->", desired(8, 150, 60), "(raw 20, capped at max 10)")
print("clamp low   : 4 pods, 10% vs 60% ->", desired(4, 10, 60), "(raw 1, floor at min 2)")

def run(cpu_per_pod_total, window=5, steps=14):
    """cpu_per_pod_total[t] = total CPU demand in 'cores' at step t; each pod requests 1 core; target 60%."""
    cur, recs, log = 4, [], []
    for t, demand in enumerate(cpu_per_pod_total[:steps]):
        util = 100 * demand / cur                  # average utilisation vs request
        rec = desired(cur, util, 60)
        recs.append(rec)
        # scale-up uses the newest recommendation; scale-down uses the MAX over the window
        new = rec if rec > cur else min(cur, max(recs[-window:]))
        log.append((t, round(util), rec, new))
        cur = new
    return log

demand = [3.6]*3 + [6.0]*3 + [1.2]*8          # spike, then quiet
print("t  util%  rec  replicas_after")
for t, u, r, n in run(demand):
    print(f"{t:<2d} {u:<5d}  {r:<3d}  {n}")
