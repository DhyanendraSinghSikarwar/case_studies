# Q28: queue consumer simulation: at-least-once duplicates, dedupe by event id, micro-batches, poison -> DLQ, lag.
import random
from collections import deque
random.seed(1)
def score_batch(events):                      # stand-in model; raises on a poison event
    for e in events:
        if e["x"] is None: raise ValueError(f"bad payload in event {e['id']}")
    return [int(e["x"] > 0.5) for e in events]

queue = deque()
for i in range(40): queue.append({"id": i, "x": random.random()})
queue[10]["x"] = None                          # poison event
for i in (3, 3, 17, 25, 25):                   # broker redelivers: at-least-once duplicates
    queue.append(dict(queue[i]) if i != 10 else None)
produced = len(queue)
seen, results, dlq, polls, max_lag, scored_calls = set(), {}, [], 0, 0, 0
BATCH = 8
while queue:
    max_lag = max(max_lag, len(queue))
    batch = [queue.popleft() for _ in range(min(BATCH, len(queue)))]; polls += 1
    fresh = []
    for e in batch:
        if e["id"] in seen: continue           # duplicate: skip (idempotent)
        seen.add(e["id"]); fresh.append(e)
    try:
        for e, s in zip(fresh, score_batch(fresh)): results[e["id"]] = s
        scored_calls += 1
    except ValueError:
        for e in fresh:                        # isolate the poison: retry one by one
            try: results[e["id"]] = score_batch([e])[0]
            except ValueError as err: dlq.append((e["id"], str(err)))
print(f"messages on queue {produced}, polls {polls}, max lag {max_lag}")
print(f"scored {len(results)}, duplicates skipped {produced - len(seen)}, dead-lettered {len(dlq)}: {dlq}")
assert len(results) + len(dlq) == len(seen) == 40
print("check: scored + dead-lettered == unique ids (40):", len(results) + len(dlq))
