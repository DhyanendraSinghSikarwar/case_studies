# EMULATION of Kafka consumer semantics in pure Python. No broker, no Kafka client was run.
import json, random
random.seed(19)

def make_msg(i):
    r = random.random()
    if r < 0.06:  return i, b"{not json"                                   # parse failure
    if r < 0.12:  return i, json.dumps({"card": None, "amt": 5}).encode()   # null key
    if r < 0.18:  return i, json.dumps({"card": f"c{i%5}", "amt": "x"}).encode()  # schema mismatch
    return i, json.dumps({"card": f"c{i%5}", "amt": 10 + i % 7, "flaky": i % 17 == 0}).encode()

class Poison(Exception): pass          # never worth retrying
class Transient(Exception): pass       # worth retrying

def parse(raw):
    try: d = json.loads(raw)
    except ValueError as e: raise Poison(f"parse_error: {e}")
    if d.get("card") is None: raise Poison("null_key")
    if not isinstance(d.get("amt"), (int, float)): raise Poison("schema_mismatch: amt not number")
    return d

attempts = {}
def process(off, d):
    attempts[off] = attempts.get(off, 0) + 1
    if d.get("flaky") and (attempts[off] <= 2 or off == 34):   # fails twice then works; offset 34 never works
        raise Transient("sink timeout")

log, dlq, done = [], [], []
PRODUCE_PER_TICK, MAX_POLL, MAX_RETRIES, TICKS = 10, 4, 3, 14
consumers = 1
committed = 0
for tick in range(1, TICKS + 1):
    if tick <= 8:                                   # producer burst for 8 ticks
        for _ in range(PRODUCE_PER_TICK):
            log.append(make_msg(len(log)))
    if tick == 6:
        consumers = 2                               # scale out after lag alarm (same group, 2 partitions assumed)
    budget = MAX_POLL * consumers                   # pull-based: consumer only asks for what it can handle
    while budget and committed < len(log):
        off, raw = log[committed]
        try:
            d = parse(raw); 
            for _try in range(MAX_RETRIES):
                try: process(off, d); done.append(off); break
                except Transient: pass              # a real consumer sleeps with backoff here
            else:
                raise Poison("retries_exhausted")
        except Poison as e:
            dlq.append({"topic": "tx", "partition": 0, "offset": off, "error": str(e),
                        "attempts": attempts.get(off, 0), "payload": raw.decode(), "tick": tick})
        committed += 1; budget -= 1                 # commit AFTER the message is done or parked
    print(f"tick={tick:2d} consumers={consumers} produced={len(log):3d} committed={committed:3d} lag={len(log)-committed:3d} dlq={len(dlq)}")

print("processed ok:", len(done), "| in DLQ:", len(dlq), "| flaky ones that succeeded after retry:",
      sum(1 for o in done if attempts[o] > 1))
for r in dlq[:4]: print(r)
reasons = {}
for r in dlq: reasons[r["error"].split(":")[0]] = reasons.get(r["error"].split(":")[0], 0) + 1
print("DLQ by reason:", dict(sorted(reasons.items())))
