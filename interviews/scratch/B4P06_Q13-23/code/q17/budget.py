# budget.py : planning inputs (invented, NOT measurements). Checks the p99 budget adds up and prints the capacity sketch.
import math, sys
TARGET_MS = 50
BUDGET = {                       # ms at p99, per hop. Hops add up in the worst case here (conservative on purpose)
    "network client->gateway":     5,
    "gateway + auth":              3,
    "request parse + validation":  2,
    "feature lookup (cache/store)": 12,
    "model inference":             10,
    "response + serialisation":    2,
    "network back":                5,
}
SLACK_MS = 5                     # kept in reserve for GC, noisy neighbours, retries
total = sum(BUDGET.values())
for k, v in BUDGET.items(): print(f"{k:<32}{v:>4} ms")
print(f"{'sum of hops':<32}{total:>4} ms\n{'reserve':<32}{SLACK_MS:>4} ms\n{'target':<32}{TARGET_MS:>4} ms")
assert total + SLACK_MS <= TARGET_MS, f"over budget by {total + SLACK_MS - TARGET_MS} ms"
print("budget OK: hops + reserve <= target, headroom", TARGET_MS - total - SLACK_MS, "ms")
# capacity sketch for 2000 rps peak. per_replica_rps is an invented planning input until you measure it.
per_replica_rps, util, spare = 150, 0.6, 2
print("replicas:", math.ceil(2000 / (per_replica_rps * util)) + spare, "(2000 / (150*0.6) = 22.2 -> 23, +2 spare)")
# the check really fails when a hop grows
BUDGET["feature lookup (cache/store)"] = 25
try:
    assert sum(BUDGET.values()) + SLACK_MS <= TARGET_MS, f"over budget by {sum(BUDGET.values()) + SLACK_MS - TARGET_MS} ms"
except AssertionError as e: print("feature store at 25 ms ->", e)
