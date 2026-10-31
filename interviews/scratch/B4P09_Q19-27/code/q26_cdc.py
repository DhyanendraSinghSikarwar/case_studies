# EMULATION of Debezium-style change events. No Debezium, database or Kafka was run.
import json
def ev(lsn, op, key, before, after):
    return {"lsn": lsn, "op": op, "key": key, "before": before, "after": after}

# Source table customers(id PK, tier). Events in COMMIT order (lsn). 'r' = snapshot read.
truth_log = [
    ev(1, "r", 1, None, {"id": 1, "tier": "silver"}),      # initial snapshot
    ev(2, "r", 2, None, {"id": 2, "tier": "silver"}),
    ev(3, "u", 1, {"id": 1, "tier": "silver"}, {"id": 1, "tier": "gold"}),
    ev(4, "c", 3, None, {"id": 3, "tier": "silver"}),
    ev(5, "u", 1, {"id": 1, "tier": "gold"}, {"id": 1, "tier": "platinum"}),
    ev(6, "u", 2, {"id": 2, "tier": "silver"}, {"id": 2, "tier": "gold"}),
    ev(7, "d", 2, {"id": 2, "tier": "gold"}, None),        # delete (a tombstone message follows in Kafka)
    ev(8, "u", 3, {"id": 3, "tier": "silver"}, {"id": 3, "tier": "gold"}),
]
# What actually arrives: lsn 5 before lsn 3 (retry or two partitions), and the delete (7) before the update (6).
arrival = [truth_log[i] for i in (0, 1, 3, 4, 2, 6, 5, 7)]
print("arrival lsn order:", [e["lsn"] for e in arrival])

def naive(events, handle_deletes=True):
    state = {}
    for e in events:                                # arrival order, no version check
        if e["op"] in ("r", "c", "u"): state[e["key"]] = e["after"]["tier"]
        elif handle_deletes: state.pop(e["key"], None)
    return state

def correct(events):
    state, last_lsn, history = {}, {}, []
    for e in events:
        k = e["key"]
        if e["lsn"] <= last_lsn.get(k, -1): continue         # stale / duplicate for this key: drop it
        last_lsn[k] = e["lsn"]                                # keep lsn even after a delete (tombstone for ordering)
        if e["op"] == "d":
            state.pop(k, None)
        else:
            state[k] = e["after"]["tier"]
        history.append((k, e["lsn"], e["op"], e["after"]["tier"] if e["after"] else None))
    return state, history

def truth(events): return correct(sorted(events, key=lambda e: e["lsn"]))[0]

print("source truth    :", truth(truth_log))
print("naive, no deletes:", naive(arrival, False), "<- deleted customer 2 stays; 1 stuck on 'gold'")
print("naive, arrival   :", naive(arrival), "<- 1 stuck on 'gold'; deleted customer 2 is back (update after delete)")
st, hist = correct(arrival)
print("lsn-guarded     :", st)

# History table (SCD2-style): close the previous row when a newer version arrives.
def scd2(events):
    rows = {}   # key -> list of [tier, valid_from_lsn, valid_to_lsn]
    for e in sorted(events, key=lambda e: e["lsn"]):          # a real job orders by (key, lsn) per partition
        k = e["key"]; r = rows.setdefault(k, [])
        if r and r[-1][2] is None: r[-1][2] = e["lsn"]
        if e["op"] != "d": r.append([e["after"]["tier"], e["lsn"], None])
    return rows
for k, r in sorted(scd2(truth_log).items()): print("history", k, r)
# guard check for duplicates: replay the whole arrival stream twice, result must not change
print("idempotent under replay:", correct(arrival + arrival)[0] == st)
print("matches truth:", st == truth(truth_log))
