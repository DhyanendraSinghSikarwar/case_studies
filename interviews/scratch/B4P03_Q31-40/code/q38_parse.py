"""Q38: parse Prometheus text exposition, compute p95 from histogram buckets (same linear interpolation idea as histogram_quantile)
and an error ratio. One scrape, so these are totals since start; PromQL would use rate() over a window."""
import math, pathlib, re

LINE = re.compile(r'^([a-zA-Z_:][a-zA-Z0-9_:]*)(\{[^}]*\})?\s+(\S+)$')
def parse(text):
    out = []
    for ln in text.splitlines():
        if not ln.strip() or ln.startswith("#"): continue
        m = LINE.match(ln.strip())
        if not m: raise ValueError(f"bad line: {ln!r}")
        labels = dict(re.findall(r'(\w+)="([^"]*)"', m.group(2) or ""))
        out.append((m.group(1), labels, float(m.group(3))))
    return out

def quantile(q, buckets):                       # buckets: [(upper_bound, cumulative_count)] sorted
    total = buckets[-1][1]; rank = q * total; prev_b, prev_c = 0.0, 0.0
    for b, c in buckets:
        if c >= rank:
            if math.isinf(b): return prev_b     # in the +Inf bucket: Prometheus returns the highest finite bound
            return prev_b + (b - prev_b) * (rank - prev_c) / (c - prev_c)
        prev_b, prev_c = b, c

s = parse((pathlib.Path(__file__).resolve().parent / "q38_metrics.txt").read_text())
bk = sorted((float("inf") if l["le"] == "+Inf" else float(l["le"]), v) for n, l, v in s if n.endswith("_bucket"))
print(f"samples parsed: {len(s)}")
print(f"p95 latency  : {quantile(0.95, bk):.4f} s")
print(f"p50 latency  : {quantile(0.50, bk):.4f} s")
req = {l["code"]: v for n, l, v in s if n == "http_requests_total"}
print(f"error ratio  : {req['500'] / sum(req.values()):.3f}")
try: parse("this is not a metric line")
except ValueError as e: print("bad input   :", e)
