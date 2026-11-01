# Q38: retry amplification; 1,000 rps normal, capacity 1,500 rps, 5 s slowdown (invented numbers)
from collections import deque

NORMAL, CAP, SLOW_S, RETRIES = 1000, 1500, 5, 3
# Simple arithmetic first
peak_offered = NORMAL * (1 + RETRIES)
print("worst-case offered load", peak_offered, "= x", round(peak_offered / CAP, 2), "of capacity")
assert peak_offered == 4000 and round(peak_offered / CAP, 2) == 2.67
assert NORMAL / CAP < 0.67            # normally 67% utilised, 33% headroom
# Amplification: the offered load a request-level retry creates in the 5 s window
offered = [NORMAL * (1 + min(s, RETRIES)) for s in range(SLOW_S)]
print("offered load per second during slowdown", offered)
assert offered == [1000, 2000, 3000, 4000, 4000]

def sim(shed_dead, retry_cap, horizon=40):
    """1-second steps. Server completes up to CAP attempts per second (0 during the slowdown),
    oldest first. An attempt only counts if it is served in the second it arrived
    (client timeout = 1 s). Timed-out requests are retried next second, up to RETRIES.
    shed_dead: server drops attempts whose client already gave up (cheap) instead of working on them.
    retry_cap: max retries admitted per second (None = unlimited)."""
    q = deque()                     # [arrival_second, count]
    retry_in = 0                    # retries arriving next second, by attempt number
    carry = [0] * (RETRIES + 1)     # carry[k] = attempts of number k arriving now
    goodput = []
    peak = 0
    for t in range(horizon):
        arr = [0] * (RETRIES + 1)
        arr[0] = NORMAL
        for k in range(1, RETRIES + 1):
            arr[k] = carry[k]
        if retry_cap is not None:
            extra = sum(arr[1:])
            if extra > retry_cap:                       # client-side retry budget
                scale = retry_cap / extra
                arr = [arr[0]] + [int(x * scale) for x in arr[1:]]
        total = sum(arr); peak = max(peak, total)
        q.append([t, arr])
        cap = 0 if t < SLOW_S else CAP
        served_ok = 0
        newq = deque()
        for ts, a in q:
            n = sum(a)
            if ts < t and shed_dead:
                continue                                # dead work dropped at no cost
            take = min(n, cap)
            cap -= take
            if ts == t:
                served_ok += take
            if take < n:                                # unserved remainder stays queued
                keep = [x * (n - take) // n if n else 0 for x in a]
                newq.append([ts, keep])
        q = newq
        goodput.append(served_ok)
        # attempts not served this second time out; they come back as next attempt number
        fail = [0] * (RETRIES + 1)
        for ts, a in q:
            if ts == t:
                fail = a
        carry = [0] * (RETRIES + 1)
        for k in range(RETRIES):
            carry[k + 1] = fail[k]
    return goodput, peak

def recovery(g):
    for t in range(SLOW_S, len(g)):
        if g[t] >= 0.95 * NORMAL:
            return t - SLOW_S
    return None

for name, shed, cap in [("naive: FIFO, retries unlimited", False, None),
                        ("server drops dead work", True, None),
                        ("drop dead work + retry budget 100/s", True, 100)]:
    g, pk = sim(shed, cap)
    print(f"{name:40} peak offered {pk:5}  secs to recover after slowdown:", recovery(g),
          " goodput t=5..9:", g[5:10])

g_naive, _ = sim(False, None)
g_shed, _ = sim(True, None)
g_best, pk_best = sim(True, 100)
assert recovery(g_naive) is None                    # in this simple model it never recovers
assert recovery(g_shed) is not None
assert recovery(g_best) is not None and recovery(g_best) <= recovery(g_shed)
assert pk_best <= NORMAL + 100
