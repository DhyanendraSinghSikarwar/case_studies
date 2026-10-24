# TOY: retry storms, jitter, retry-after, circuit breaker. Simulated server and clients (synthetic), seeded.
import random
random.seed(11)
# A. 200 clients all got 429 at t=0. Server handles at most 40 requests per 1-second slot, else 429.
def simulate(policy, n=200, cap=40, slots=40, base=1.0, cap_delay=16.0):
    pending = {i: 0.0 for i in range(n)}   # client -> next attempt time
    attempts = {i: 0 for i in range(n)}
    load = [0] * slots; done = {}
    for t in range(slots):
        due = [c for c, at in pending.items() if int(at) <= t and c not in done]
        random.shuffle(due)
        for k, c in enumerate(due):
            load[t] += 1
            if k < cap and t > 0: done[c] = t
            else:
                attempts[c] += 1
                exp = min(cap_delay, base * 2 ** attempts[c])
                pending[c] = t + (exp if policy == "no_jitter" else random.uniform(0, exp))
    return load[:12], len(done), sum(load)
for pol in ("no_jitter", "full_jitter"):
    prof, ndone, total = simulate(pol)
    print(f"{pol:12} requests per 1s slot (first 12): {prof}\n{'':12} finished={ndone}/200 in 40s, total requests sent={total}")

# B. honour Retry-After, give up after a deadline
def call_with_retries(server, deadline=10.0, max_attempts=5):
    t, waited = 0.0, []
    for a in range(max_attempts):
        status, retry_after = server(t)
        if status == 200: return "ok", a + 1, t
        wait = retry_after if retry_after is not None else min(8.0, 2 ** a) * random.random()
        if t + wait > deadline: return "gave_up_deadline", a + 1, t
        t += wait
    return "gave_up_attempts", max_attempts, round(t, 1)
print("B retry-after 3s server:", call_with_retries(lambda t: (200, None) if t >= 3 else (429, 3.0)))
print("B hopeless server      :", call_with_retries(lambda t: (503, None)))

# C. circuit breaker
class Breaker:
    def __init__(self, threshold=3, cooldown=5.0): self.th, self.cd, self.fails, self.opened = threshold, cooldown, 0, None
    def allow(self, now):
        if self.opened is None: return True
        if now - self.opened >= self.cd: return True       # half-open: let one probe through
        return False
    def record(self, ok, now):
        if ok: self.fails, self.opened = 0, None
        else:
            self.fails += 1
            if self.fails >= self.th: self.opened = now
br, sent, skipped = Breaker(), 0, 0
for now in range(0, 14):
    provider_up = now >= 9                                  # provider recovers at t=9
    if br.allow(now): sent += 1; br.record(provider_up, now)
    else: skipped += 1
print("C breaker: calls sent to provider =", sent, "| short-circuited =", skipped, "of 14 ticks")

# D. fallback behaves differently: same JSON task, primary returns strict JSON, fallback adds prose
import json
def primary(_): return '{"label": "refund"}'
def fallback(_): return 'Sure! Here is the answer: {"label": "refund"}'
for name, fn in (("primary", primary), ("fallback", fallback)):
    try: print(name, "parses:", json.loads(fn("x")))
    except json.JSONDecodeError: print(name, "FAILS strict json.loads -> needs its own prompt tests or a tolerant parser")
