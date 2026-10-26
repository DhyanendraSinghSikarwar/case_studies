import random
import pytest
from feature import W, OnlineCounter, batch_count, schema_errors, freshness_ok

def make_events(n, seed, disorder):
    rng = random.Random(seed)
    evs = [{"user": rng.choice(["a", "b", "c"]), "ts": 10_000 + i * 97 + rng.randint(0, 60), "amount": float(rng.randint(1, 500))}
           for i in range(n)]
    if disorder:   # arrival order differs from event-time order (late events)
        for i in range(0, n - 5, 5):
            evs[i], evs[i + 3] = evs[i + 3], evs[i]
    return evs

def test_unit_basic_count():
    c = OnlineCounter()
    for t in (100, 200, 300):
        c.update({"user": "a", "ts": t, "amount": 1.0})
    assert c.get("a", 300) == 3
    assert c.get("b", 300) == 0

def test_unit_window_edge_is_exclusive():
    c = OnlineCounter()
    c.update({"user": "a", "ts": 0, "amount": 1.0})
    c.update({"user": "a", "ts": 10, "amount": 1.0})
    assert c.get("a", W - 1) == 2      # time only moves forward when we query
    assert c.get("a", W) == 1          # ts=0 is exactly W old, window is (now-W, now]

def test_parity_sorted_stream():
    evs = sorted(make_events(120, 1, disorder=False), key=lambda e: e["ts"])
    c = OnlineCounter()
    for e in evs:
        c.update(e)
    for now in range(10_000, 25_000, 411):
        for u in "abc":
            assert c.get(u, now) == batch_count(evs, u, now)

def test_replay_disordered_log_matches_batch_after_every_event():
    log = make_events(120, 2, disorder=True)     # the logged stream, in ARRIVAL order
    c, seen = OnlineCounter(), []
    for e in log:
        c.update(e); seen.append(e)
        now = max(x["ts"] for x in seen)
        for u in "abc":
            assert c.get(u, now) == batch_count(seen, u, now), (u, now)

def test_schema_rejects_bad_records():
    assert schema_errors({"user": "a", "ts": 1, "amount": 2.0}) == []
    assert schema_errors({"user": "", "ts": "1", "amount": 2.0}) == ["bad type ts", "empty user"]
    assert "missing amount" in schema_errors({"user": "a", "ts": 1})

@pytest.mark.parametrize("last,now,ok", [(1000, 1500, True), (1000, 1900, True), (1000, 1901, False)])
def test_freshness(last, now, ok):
    assert freshness_ok(last, now) is ok
