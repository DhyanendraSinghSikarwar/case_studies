"""Q36: idle GPU-hours from an hourly utilisation log (one row = one GPU for one hour), plus the always-on vs scale-to-zero example.
All numbers are made up. Cost unit is 'GPU-hour' so no prices are needed."""
import csv, pathlib, collections

IDLE_BELOW = 10          # percent; a policy choice, state it out loud
rows = list(csv.DictReader(open(pathlib.Path(__file__).resolve().parent / "q36_util_log.csv")))
per = collections.defaultdict(lambda: [0, 0])
for r in rows:
    p = per[r["pod"]]; p[0] += 1; p[1] += int(r["gpu_util_pct"]) < IDLE_BELOW
tot = idle = 0
print(f"{'pod':9}{'gpu-hours':>10}{'idle':>6}{'idle %':>8}")
for pod, (n, i) in sorted(per.items()):
    print(f"{pod:9}{n:>10}{i:>6}{100*i/n:>8.0f}"); tot += n; idle += i
print(f"{'TOTAL':9}{tot:>10}{idle:>6}{100*idle/tot:>8.0f}   (idle = util < {IDLE_BELOW}%)")

print("\nAlways-on vs scale-to-zero (made-up: 2 GPU replicas, traffic 6 h/day, cold start 3 min)")
gpus, busy_h, cold_min = 2, 6, 3
always = gpus * 24
s2z = gpus * busy_h + gpus * (cold_min / 60) * 2     # assume 2 cold starts/day, GPU billed while loading
print(f"always-on    : {always} GPU-h/day")
print(f"scale-to-zero: {s2z:.1f} GPU-h/day  (saves {always - s2z:.1f}, {100*(always-s2z)/always:.0f}%)")
print(f"price of it  : first request after idle waits about {cold_min} min unless one replica is kept warm")
