"""Generate fake request logs: ts_seconds,status,latency_ms,replica. Usage: q45_gen_logs.py OUTDIR"""
import csv, random, sys, pathlib
def gen(path, n, seed, p50, tail_p, tail_mult, err_rate, bad_replica=None, bad_err=0.0):
    r = random.Random(seed); rows = []
    for i in range(n):
        rep = f"pod-{r.randrange(4)}"
        lat = r.lognormvariate(0, 0.25) * p50
        if r.random() < tail_p: lat *= tail_mult
        e = bad_err if rep == bad_replica else err_rate
        status = 503 if r.random() < e else 200
        if status == 503: lat = min(lat, 30.0)                  # failures return fast (readiness/OOM restarts)
        rows.append((round(i * 0.05, 2), status, round(lat, 2), rep))
    with open(path, "w", newline="") as f: w = csv.writer(f); w.writerow(["ts", "status", "latency_ms", "replica"]); w.writerows(rows)
if __name__ == "__main__":
    out = pathlib.Path(sys.argv[1]); out.mkdir(parents=True, exist_ok=True)
    gen(out / "before.csv", 6000, 1, p50=20, tail_p=0.01, tail_mult=3, err_rate=0.001)
    gen(out / "after_bad.csv", 6000, 2, p50=24, tail_p=0.03, tail_mult=3.3, err_rate=0.004, bad_replica="pod-2", bad_err=0.07)
    gen(out / "after_ok.csv", 6000, 3, p50=20.5, tail_p=0.01, tail_mult=3, err_rate=0.001)
    print("wrote", sorted(p.name for p in out.iterdir()))
