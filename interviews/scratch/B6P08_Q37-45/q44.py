# Q44: feature view v2; 3 of 7 consumers read v2, 4 read v1; producer bug; rollback deadlock (invented)
from graphlib import TopologicalSorter

consumers = {"A": "v2", "B": "v2", "C": "v2", "D": "v1", "E": "v1", "F": "v1", "G": "v1"}
traffic = {"A": 30, "B": 10, "C": 5, "D": 25, "E": 15, "F": 10, "G": 5}   # share of revenue, invented
assert sum(traffic.values()) == 100
v2 = [m for m, v in consumers.items() if v == "v2"]
assert len(v2) == 3 and len(consumers) - len(v2) == 4
print("v2 readers:", v2, "carry", sum(traffic[m] for m in v2), "% of revenue")
assert sum(traffic[m] for m in v2) == 45

# Naive rollback: producer back to v1-only schema -> the 3 v2 readers break
broken = sum(traffic[m] for m in v2)
print("naive producer rollback breaks", broken, "% of revenue")

# Rollback order is the REVERSE of the deploy order: consumers first, then producer.
deps = {"producer v2": set(), "A": {"producer v2"}, "B": {"producer v2"}, "C": {"producer v2"}}
deploy = list(TopologicalSorter(deps).static_order())
rollback = deploy[::-1]
print("deploy order  :", deploy)
print("rollback order:", rollback)
assert deploy[0] == "producer v2" and rollback[-1] == "producer v2"

# Decision rule (a judgement, written as code so it can be reviewed): ask where the bug lives first
def choose(bug_hits_v1_readers, v1_view_still_published, prior_models_available, patch_hours, tolerable_hours=4):
    if bug_hits_v1_readers:
        return "wider incident: bug also hits v1 readers, fix forward fast and roll back only in the consumers-first order"
    if patch_hours <= tolerable_hours:
        return "fix forward: patch the producer as v2.1, leave v1 readers alone"
    if v1_view_still_published and prior_models_available:
        return "consumers first: repoint A,B,C to v1 view and prior model, then roll the producer back"
    return "no safe rollback: mitigate (manual override or fallback) and fix forward"
cases = [(False, True, True, 2), (False, True, True, 12), (False, False, True, 12), (True, True, True, 2)]
for c in cases:
    print(c, "->", choose(*c))
assert choose(*cases[0]).startswith("fix forward: patch")
assert choose(*cases[1]).startswith("consumers first")
assert choose(*cases[2]).startswith("no safe rollback")
assert choose(*cases[3]).startswith("wider incident")

# Schema compatibility check that would have stopped the deadlock (breaking vs additive)
v1s = {"user_id": "int", "spend_30d": "float", "n_orders": "int"}
v2s = {"user_id": "int", "spend_30d": "float", "orders_count": "int", "region": "str"}
def diff(old, new):
    removed = sorted(set(old) - set(new)); added = sorted(set(new) - set(old))
    retyped = sorted(k for k in set(old) & set(new) if old[k] != new[k])
    return {"removed": removed, "added": added, "retyped": retyped, "breaking": bool(removed or retyped)}
d = diff(v1s, v2s)
print("v1 -> v2:", d)
assert d == {"removed": ["n_orders"], "added": ["orders_count", "region"], "retyped": [], "breaking": True}
# additive-only change is safe to serve in place:
assert diff(v1s, {**v1s, "region": "str"})["breaking"] is False

# Deprecation timeline: serve v1 and v2 side by side until all consumers moved
migrated = {m: 0 for m in consumers}
for m in v2: migrated[m] = 1
remaining = [m for m, x in migrated.items() if not x]
print("consumers still on v1 (block v1 retirement):", remaining)
assert remaining == ["D", "E", "F", "G"]
