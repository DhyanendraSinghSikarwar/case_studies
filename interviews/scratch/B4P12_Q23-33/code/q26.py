# Q26: serving cost levers. Abstract units: replicas, not money. All inputs invented.
import math
PEAK, REPEAT, HEAD = 300, 0.40, 0.70           # peak RPS, repeat share, target utilisation
BASE_RPS = 30                                    # one replica, one request at a time (invented)
def need(load, per_rep): return math.ceil(load / (per_rep * HEAD))
base = need(PEAK, BASE_RPS)
HIT = 0.40 * 0.9                                 # repeats only count if still cached: assume 90% of repeats hit
levers = {   # name: (load factor, per-replica factor, effort 1-5 (my estimate), risk)
 "response cache":       (1 - HIT, 1.0, 2, "stale answers; privacy of cached keys"),
 "dynamic batching":     (1.0, 3.0, 2, "adds wait for the batch to fill (p99)"),
 "quantisation":         (1.0, 1.5, 3, "small accuracy loss, needs re-validation"),
 "right-size replica":   (1.0, 1.2, 1, "less headroom for bursts"),
 "move to batch":        (0.25, 1.0, 5, "answers no longer real-time; 25% of traffic assumed movable"),
}
print(f"baseline: {PEAK} RPS / ({BASE_RPS} x {HEAD}) -> {base} replicas")
rows = []
for k, (lf, pf, eff, risk) in levers.items():
    n = need(PEAK * lf, BASE_RPS * pf); red = base - n
    rows.append((red / eff, k, n, red, eff, risk))
print(f"{'lever':<20}{'replicas':>9}{'saved':>6}{'effort':>7}{'saved/effort':>13}  risk")
for r in sorted(rows, reverse=True): print(f"{r[1]:<20}{r[2]:>9}{r[3]:>6}{r[4]:>7}{r[0]:>13.2f}  {r[5]}")
both = need(PEAK * (1 - HIT), BASE_RPS * 3.0)
print(f"cache + batching together: {both} replicas (saved {base-both})")
print("availability floor: never below 2 replicas, so the plan is", max(2, both))
