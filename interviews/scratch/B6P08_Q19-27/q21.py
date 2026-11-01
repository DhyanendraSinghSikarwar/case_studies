# Q21: blue/green cold start. Illustrative numbers; simple deterministic model, not a benchmark.
BASE_P99_MS, BAD_P99_MS, BAD_SECONDS = 120, 2400, 180
RPS = 500                                   # illustrative traffic
assert BAD_P99_MS / BASE_P99_MS == 20
exposed_bigbang = RPS * BAD_SECONDS         # all traffic hits the cold pods for 3 minutes
slow_min = exposed_bigbang // 100           # p99 above 2.4 s means at least 1% of requests were slower
print(f"big-bang switch: {exposed_bigbang:,} requests in the 3-minute window, at least {slow_min:,} slower than 2.4 s")
assert exposed_bigbang == 90_000 and slow_min == 900
# --- readiness with warm-up: a cold pod answers the first requests slowly, then settles (decay model)
import math
def cold_latency_ms(i, steady=120, first=2400, tau=6):      # i-th request after start
    return steady + (first - steady) * math.exp(-i / tau)
THRESH = 2 * BASE_P99_MS                                    # ready only when warm latency < 240 ms
def warmup_requests_needed(window=5):
    i = 0
    while True:
        i += 1
        if i >= window and all(cold_latency_ms(j) < THRESH for j in range(i - window, i)):
            return i
n_warm = warmup_requests_needed()
print(f"synthetic warm-up requests before the pod reports ready: {n_warm}")
assert cold_latency_ms(0) == 2400 and cold_latency_ms(n_warm) < THRESH and cold_latency_ms(n_warm - 6) >= THRESH
# --- staged shift with an automatic abort rule: p99 over a 60 s stage window must stay under 2x baseline
stages = [5, 25, 50, 100]                                   # percent of traffic
STAGE_S = 60
def run(pods_warm):
    served_cold = 0
    for pct in stages:
        exposed = RPS * pct // 100 * STAGE_S
        if not pods_warm:                                   # gate trips in the first stage
            served_cold += exposed
            return pct, served_cold
    return 100, 0
stage_hit, cold_requests = run(pods_warm=False)
print(f"staged shift with unwarmed pods: abort in the {stage_hit}% stage, {cold_requests:,} requests exposed")
assert stage_hit == 5 and cold_requests == 1_500
assert exposed_bigbang / cold_requests == 60                # 60 times fewer requests exposed
print(f"exposure ratio big-bang / staged: {exposed_bigbang // cold_requests}x")
print("abort rule: p99 > 240 ms (2 x 120) for 60 s in any stage -> send 100% back to blue, keep blue for >= 30 min")
