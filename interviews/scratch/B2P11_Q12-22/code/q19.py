# TOY: head vs tail sampling on SYNTHETIC traces, retention sweep, and user deletion across stores. Seeded.
import random, hashlib, time
random.seed(7)
N = 100_000
traces = []
for i in range(N):
    err = random.random() < 0.01
    low = (not err) and random.random() < 0.02
    traces.append(dict(id=i, tenant=random.choice(["a", "b", "c"]), error=err, low_score=low))
n_err = sum(t["error"] for t in traces); n_low = sum(t["low_score"] for t in traces)
def head(t, p=0.05): return random.random() < p           # decided at the start: cannot know the outcome
def tail(t, p=0.05): return t["error"] or t["low_score"] or random.random() < p   # decided after the trace finishes
for name, fn in (("head 5%", head), ("tail: errors+low+5%", tail)):
    kept = [t for t in traces if fn(t)]
    print(f"{name:20} kept {len(kept):5d} of {N} ({len(kept)/N*100:4.1f}%) | errors kept {sum(t['error'] for t in kept)}/{n_err} | low-score kept {sum(t['low_score'] for t in kept)}/{n_low}")
# retention: full text shorter-lived than metadata
DAY = 86400
def sweep(store, now, ttl):
    before = len(store); store[:] = [r for r in store if now - r["ts"] < ttl]; return before - len(store)
full = [dict(id=i, ts=i * DAY, text="prompt " + str(i)) for i in range(100)]
print("retention sweep removed", sweep(full, 100 * DAY, 30 * DAY), "of 100 full-text rows (TTL 30 days, synthetic)")
# deletion by user: store a keyed hash of user id, not the raw id, and delete across every store that copied the trace
def uh(user): return hashlib.sha256(b"salt-rotate-me:" + user.encode()).hexdigest()[:12]
stores = {
    "traces":   [dict(trace=1, user=uh("u1"), text="hi"), dict(trace=2, user=uh("u2"), text="yo")],
    "eval_set": [dict(trace=1, user=uh("u1"), text="hi")],
    "vector_cache": [dict(trace=2, user=uh("u2"), text="yo")],
}
def delete_user(user):
    h, report = uh(user), {}
    for name, rows in stores.items():
        n = len(rows); rows[:] = [r for r in rows if r["user"] != h]; report[name] = n - len(rows)
    return report
print("deletion report for u1:", delete_user("u1"))
print("remaining:", {k: len(v) for k, v in stores.items()}, "| backups and provider-side copies are NOT touched by this code")
