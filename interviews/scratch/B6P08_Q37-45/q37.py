# Q37: rate limit of 200,000 tokens/min; demand 150 req/min x 1,500 tokens (invented numbers)
import random
from collections import deque

LIMIT = 200_000
RPM, TOK = 150, 1_500
demand = RPM * TOK
over = demand - LIMIT
print("demand", demand, "over", over, "share of demand", round(over / demand, 4),
      "share of limit", round(over / LIMIT, 4))
assert demand == 225_000 and over == 25_000
assert round(over / demand, 3) == 0.111 and round(over / LIMIT, 3) == 0.125

# Sustained overload: a client-side queue only moves the pain into waiting time.
backlog = 0
for minute in range(1, 61):
    backlog += over            # tokens that cannot be sent this minute pile up
wait_min = backlog / LIMIT     # how long a new request waits behind the backlog
print("backlog after 60 min (tokens)", backlog, "wait for a new request (min)", wait_min)
assert backlog == 1_500_000 and wait_min == 7.5

# What it takes to fit: cut demand by 11.1%, i.e. fewer requests or fewer tokens each
max_rpm = LIMIT // TOK                  # 133 requests/min at 1,500 tokens
max_tok = LIMIT // RPM                  # 1,333 tokens per request at 150/min
print("fits at", max_rpm, "req/min or", max_tok, "tokens/request")
assert max_rpm == 133 and max_tok == 1333

# Bursty arrivals: a sliding 60 s window limit, Poisson arrivals, seed fixed.
def run(keys, seed=7, secs=1800, rate_per_s=RPM / 60, tok=TOK):
    """Limit is shared by the whole organisation, whatever key signs the request
    (an ASSUMPTION about the provider; check its docs)."""
    rnd = random.Random(seed)
    win = deque()           # (time, tokens) accepted in the last 60 s, shared
    used = rejected = total = 0
    t = 0.0
    while t < secs:
        t += rnd.expovariate(rate_per_s)
        key = rnd.randrange(keys)           # which key sent it: irrelevant to the limit
        while win and win[0][0] <= t - 60:
            used -= win.popleft()[1]
        total += 1
        if used + tok > LIMIT:
            rejected += 1
        else:
            win.append((t, tok)); used += tok
    return rejected / total

r1, r4 = run(1), run(4)
print("rejected share, 1 key:", round(r1, 3), "| 4 keys, same org limit:", round(r4, 3))
assert r1 == r4                                   # same arrivals, same shared bucket
assert 0.08 < r1 < 0.16                           # near the 11% overload, burstiness adds a bit

# Same traffic, but trimmed 15% by caching + shorter prompts: bursts still hit, far less
TOK2 = int(TOK * 0.85)
r_trim = run(1, tok=TOK2)
print("trimmed demand", RPM * TOK2, "headroom", LIMIT - RPM * TOK2, "rejected share", round(r_trim, 3))
assert r_trim < 0.05 < r1
assert RPM * TOK2 == 191_250 and LIMIT - RPM * TOK2 == 8_750
