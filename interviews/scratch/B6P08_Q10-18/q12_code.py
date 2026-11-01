import math

rate, f0 = 40, 0.25
failed = rate * f0
assert failed == 10
# Immediate retries (max 3), independent failures at 25%: calls per request
calls_per_req = sum(f0 ** k for k in range(4))
offered = rate * calls_per_req
print("calls per request:", round(calls_per_req, 4), "| offered calls/s:", round(offered, 1))
assert round(calls_per_req, 4) == 1.3281 and round(offered, 1) == 53.1
print("requests failing for good if independent:", round(f0 ** 4 * 100, 2), "%")
assert round(f0 ** 4 * 100, 2) == 0.39

# But a rate limit is not independent. Model: provider accepts L calls/s, rest rejected.
# 25% failing at 40/s means L = 30 (assumption for a 429-style limit).
L = 30
assert L == rate * (1 - f0)
f = f0
for _ in range(200):                      # fixed point of f = 1 - L / offered(f)
    tot = rate * sum(f ** k for k in range(4))
    f = max(0.0, 1 - L / tot)
tot = rate * sum(f ** k for k in range(4))
final_fail = f ** 4
print("with a hard cap of 30/s: attempt failure", round(f * 100, 1), "% | offered", round(tot, 1), "calls/s | requests lost", round(final_fail * 100, 1), "%")
assert 0.70 < f < 0.72 and tot > 100 and abs(final_fail - 0.25) < 0.01

# Retry budget (10% extra calls) + jittered backoff keeps offered load near 40 * 1.1
budget_calls = rate * 1.10
print("with a 10% retry budget: offered at most", budget_calls, "calls/s; the provider still serves only", L, "so goodput is unchanged")
assert budget_calls == 44.0
print("goodput: no retries", min(rate, L), "| 3 immediate retries", L, "| both 30/s, retries only add 62 extra calls/s of load")
assert round(tot - rate) == 62
# Fallback ramp: send 10% of traffic first, check its limit
fb_limit = 20          # illustrative: fallback account allows 20 calls/s (never tested)
print("fallback at 100% would need", rate, "calls/s vs limit", fb_limit, "-> would reject", rate - fb_limit, "/s")
assert rate - fb_limit == 20
print("fallback at 25% needs", rate * 0.25, "calls/s, inside the limit")
assert rate * 0.25 <= fb_limit
