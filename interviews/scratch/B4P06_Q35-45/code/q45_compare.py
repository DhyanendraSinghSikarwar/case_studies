"""Compare before/after request logs and recommend keep or rollback. Usage: q45_compare.py BEFORE.csv AFTER.csv"""
import csv, sys, math
from collections import defaultdict
P99_RATIO_LIMIT, ERR_DELTA_LIMIT, ERR_ABS_LIMIT = 1.5, 0.005, 0.01     # team thresholds: invented; agree yours with the SLO

def percentile(sorted_vals, q):                    # nearest-rank percentile, easy to hand-check
    return sorted_vals[max(0, math.ceil(q / 100 * len(sorted_vals)) - 1)]

def load(path):
    with open(path) as f: return [(float(r["ts"]), int(r["status"]), float(r["latency_ms"]), r["replica"]) for r in csv.DictReader(f)]

def summarise(rows):
    ok = sorted(l for _, s, l, _ in rows if s < 500); errs = [r for r in rows if r[1] >= 500]
    by = defaultdict(lambda: [0, 0])
    for _, s, _, rep in rows: by[rep][0] += 1; by[rep][1] += s >= 500
    return {"n": len(rows), "err_rate": len(errs) / len(rows), "p50": percentile(ok, 50), "p95": percentile(ok, 95), "p99": percentile(ok, 99),
            "replica_err": {k: v[1] / v[0] for k, v in sorted(by.items())}}

def recommend(b, a):
    reasons = []
    if a["p99"] / b["p99"] >= P99_RATIO_LIMIT: reasons.append(f"p99 x{a['p99']/b['p99']:.2f} (limit x{P99_RATIO_LIMIT})")
    if a["err_rate"] - b["err_rate"] >= ERR_DELTA_LIMIT: reasons.append(f"error rate +{(a['err_rate']-b['err_rate'])*100:.2f} pp (limit {ERR_DELTA_LIMIT*100:.1f} pp)")
    if a["err_rate"] >= ERR_ABS_LIMIT: reasons.append(f"error rate {a['err_rate']*100:.2f}% over {ERR_ABS_LIMIT*100:.0f}% absolute limit")
    return ("ROLLBACK", reasons) if reasons else ("KEEP", ["all deltas inside thresholds"])

def report(bp, ap):
    b, a = summarise(load(bp)), summarise(load(ap))
    print(f"{'metric':10s}{'before':>10s}{'after':>10s}{'delta':>10s}")
    for k in ("p50", "p95", "p99"): print(f"{k + ' ms':10s}{b[k]:10.1f}{a[k]:10.1f}{a[k]-b[k]:+10.1f}  (x{a[k]/b[k]:.2f})")
    print(f"{'5xx rate':10s}{b['err_rate']*100:9.2f}%{a['err_rate']*100:9.2f}%{(a['err_rate']-b['err_rate'])*100:+9.2f}pp")
    worst = max(a["replica_err"].items(), key=lambda kv: kv[1])
    print("5xx rate by replica after:", {k: f"{v*100:.1f}%" for k, v in a["replica_err"].items()})
    if worst[1] > 0.01 and worst[1] > 3 * a["err_rate"]: print(f"note: errors concentrated on {worst[0]}: check OOM kills, restarts and readiness on that pod")
    verdict, why = recommend(b, a); print("RECOMMENDATION:", verdict, "|", "; ".join(why)); return verdict

if __name__ == "__main__": report(sys.argv[1], sys.argv[2])
