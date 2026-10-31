# Q23: provider outage simulation: retries only vs retries + circuit breaker + fallback. Seeded, abstract seconds.
import heapq, random
SEED = 23
DUR, RPS = 3600, 20              # one hour of traffic at 20 requests per second (invented)
OUT_START, OUT_END = 600, 3000   # provider down for 40 minutes (2400 s)
MAX_TRY, BASE, CAP = 3, 1.0, 8.0 # up to 3 attempts, backoff 1s, 2s ... capped, full jitter
TIMEOUT = 2.0                    # an attempt during the outage fails after 2 s

def provider_up(t): return not (OUT_START <= t < OUT_END)

def run(mode):
    rng = random.Random(SEED)
    ev, n = [], 0
    for sec in range(DUR):
        for _ in range(RPS):
            heapq.heappush(ev, (sec + rng.random(), n, 0)); n += 1   # (time, request id, attempts so far)
    total = n
    attempts = served = fb = failed = 0
    fails_in_row, open_until = 0, -1.0
    probing = False
    while ev:
        t, rid, k = heapq.heappop(ev)
        if mode == "breaker" and t < open_until:                      # circuit open: do not touch the provider
            fb += 1; continue
        attempts += 1
        ok = provider_up(t)
        if ok:
            served += 1; fails_in_row = 0
            if mode == "breaker": open_until = -1.0
            continue
        fails_in_row += 1
        if mode == "breaker" and fails_in_row >= 5:                   # trip after 5 failures in a row
            open_until = t + 30.0; fails_in_row = 4                   # half-open: one probe after 30 s, a failed probe re-opens
            fb += 1; continue
        if k + 1 < MAX_TRY:
            delay = rng.uniform(0, min(CAP, BASE * 2 ** k))           # full jitter
            heapq.heappush(ev, (t + TIMEOUT + delay, rid, k + 1))
        elif mode in ("breaker", "retries_fallback"): fb += 1
        else: failed += 1
    return total, served, fb, failed, attempts

print(f"{'mode':<18}{'requests':>9}{'primary_ok':>11}{'fallback':>9}{'failed':>8}{'attempts':>9}{'amplification':>14}")
for mode in ("retries_only", "retries_fallback", "breaker"):
    total, served, fb, failed, attempts = run(mode)
    assert served + fb + failed == total
    print(f"{mode:<18}{total:>9}{served:>11}{fb:>9}{failed:>8}{attempts:>9}{attempts/total:>14.2f}")
# hand check: 2400 s x 20 rps = 48000 requests arrive in the outage; retries_only makes up to 3 attempts for each
print("outage requests:", (OUT_END - OUT_START) * RPS, "-> at most", (OUT_END - OUT_START) * RPS * MAX_TRY, "attempts in the outage")
