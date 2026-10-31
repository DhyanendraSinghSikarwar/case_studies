"""Q32: PURE-PYTHON EMULATION of a Kafka-like log -> consumer job -> online store.
Not real Kafka. Failure schedule is seeded, so the run is repeatable."""
import random

rng = random.Random(7)
USERS = ["u1", "u2", "u3"]

# --- intended truth: per-user sequence of events, seq starts at 1 and is assigned by the producer
truth_events = []
seq = {u: 0 for u in USERS}
for _ in range(12):
    u = rng.choice(USERS)
    seq[u] += 1
    truth_events.append({"user": u, "seq": seq[u], "amount": rng.randint(10, 99)})

# --- hop 1: producer. Retries after a lost ack append the SAME event twice (no idempotent producer).
log = []                          # the "partition": list index = offset
for e in truth_events:
    log.append(dict(e))
    if rng.random() < 0.25:       # ack lost, producer retries -> duplicate record at a new offset
        log.append(dict(e))
print(f"intended events={len(truth_events)}  records in log={len(log)} (duplicates from producer retry={len(log) - len(truth_events)})")

# --- expected final online values
exp = {}
for e in truth_events:
    d = exp.setdefault(e["user"], {"count": 0, "last_amount": None, "seq": 0})
    d["count"] += 1; d["last_amount"] = e["amount"]; d["seq"] = e["seq"]

# --- hop 3: consumer job with an "online store" sink.
class Naive:
    def __init__(self): self.s = {}
    def apply(self, e):
        d = self.s.setdefault(e["user"], {"count": 0, "last_amount": None, "seq": 0})
        d["count"] += 1                      # non-idempotent increment
        d["last_amount"] = e["amount"]       # blind overwrite
        d["seq"] = e["seq"]

class Guarded:
    """Upsert guard: only apply the next unseen version for a key (seq == stored+1)."""
    def __init__(self): self.s = {}; self.skipped = 0; self.gaps = 0
    def apply(self, e):
        d = self.s.setdefault(e["user"], {"count": 0, "last_amount": None, "seq": 0})
        if e["seq"] <= d["seq"]:
            self.skipped += 1; return        # duplicate or older replay: ignore
        if e["seq"] > d["seq"] + 1:
            self.gaps += 1; return           # a gap: do not apply out of order, raise an alert
        d["count"] += 1; d["last_amount"] = e["amount"]; d["seq"] = e["seq"]

def run_job(sink, crash_at, rewind_to):
    """Process in batches of 5; write sink first, commit offset after (at-least-once).
    crash_at: after writing this batch number, crash BEFORE committing offset -> batch replays.
    rewind_to: at the end an operator resets the consumer to this offset to 'reprocess'."""
    committed = 0
    crashed = False
    while committed < len(log):
        batch = log[committed:committed + 5]
        for e in batch:
            sink.apply(e)
        if not crashed and committed // 5 == crash_at:
            crashed = True               # crash between sink write and offset commit
            continue                     # restart: re-read from the same committed offset
        committed += len(batch)
    # operator rewinds offsets and reprocesses everything from rewind_to
    for e in log[rewind_to:]:
        sink.apply(e)
    # a slow backfill job finishes last and replays the OLDEST records into the same store
    for e in log[:3]:
        sink.apply(e)

for name, sink in (("NAIVE (blind increment + overwrite)", Naive()), ("GUARDED (seq guard)", Guarded())):
    run_job(sink, crash_at=1, rewind_to=3)
    ok = sink.s == exp
    print(f"\n{name}: final == expected? {ok}")
    for u in USERS:
        print(f"  {u}: got {sink.s.get(u)}  expected {exp.get(u)}")
    if isinstance(sink, Guarded):
        print(f"  guard skipped {sink.skipped} duplicate/old records, gaps seen={sink.gaps}")

# --- gap detection: a record is LOST (e.g. acks=0 on a real producer); guard must alert, not silently skip
lossy = [e for e in log if not (e["user"] == "u1" and e["seq"] == 2)]
g = Guarded()
for e in lossy:
    g.apply(e)
print(f"\nLOST-RECORD case (u1 seq 2 removed from log): gaps seen={g.gaps}, u1 stuck at seq={g.s['u1']['seq']} (alert instead of wrong value)")
