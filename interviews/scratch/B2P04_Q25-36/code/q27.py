# Synthetic mixed-batch sampler with target ratios. Sources are fake lists of example ids; no real data.
import random
from collections import Counter
random.seed(0)
TARGET = {"task_extract": 0.60, "task_summarise": 0.20, "general_replay": 0.15, "safety_refusal": 0.05}
POOLS = {k: [f"{k}_{i}" for i in range(n)] for k, n in
         {"task_extract": 5000, "task_summarise": 1500, "general_replay": 800, "safety_refusal": 200}.items()}

def mixed_stream(target, pools, batch_size=32):
    """Deficit scheduler: for every slot pick the source furthest below its target share so far.
    Batch-level counts are rounded, but the running ratio converges to the target."""
    names = list(target)
    given = {n: 0 for n in names}
    iters = {n: iter(random.sample(pools[n], len(pools[n]))) for n in names}
    seen = 0
    while True:
        batch = []
        for _ in range(batch_size):
            seen += 1
            n = max(names, key=lambda k: target[k] * seen - given[k])
            given[n] += 1
            try:
                batch.append(next(iters[n]))
            except StopIteration:                    # small pools repeat: more epochs than the big pool
                iters[n] = iter(random.sample(pools[n], len(pools[n])))
                batch.append(next(iters[n]))
        random.shuffle(batch)
        yield batch

gen = mixed_stream(TARGET, POOLS)
counts, total = Counter(), 0
for _ in range(500):
    b = next(gen)
    counts.update(x.rsplit("_", 1)[0] for x in b); total += len(b)
print("batch size 32, 500 batches =", total, "examples")
for k, v in TARGET.items():
    print(f"{k:15s} target {v:.2%}  realised {counts[k]/total:.2%}")
# epochs per source: how many times each pool was passed
for k in TARGET:
    print(f"{k:15s} pool {len(POOLS[k]):5d}  seen {counts[k]:6d}  -> {counts[k]/len(POOLS[k]):.1f} epochs")
