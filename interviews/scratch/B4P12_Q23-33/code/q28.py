# Q28: autoscaling simulation, 1-second steps, seeded. Abstract units. Startup 90 s.
import random, math
from collections import deque
SEED = 28
T = 7200; STARTUP = 90; CAP = 10              # one replica serves 10 requests/s
rng = random.Random(SEED)
def rate(t):                                   # invented spiky trace (rps): quiet base plus 4 known daily-style peaks and 1 surprise
    base = 0.0 if 1200 <= t < 2300 else 1.5                   # a quiet stretch with no traffic at all
    for s in (900, 2400, 4500):
        if s <= t < s + 240: base = 45
    if 3200 <= t < 4200: base = 25 if (t // 60) % 2 == 0 else 5   # load that oscillates around a threshold
    if 5800 <= t < 5900: base = 60             # surprise spike nobody scheduled
    return base
arr = [sum(1 for _ in range(int(rate(t) * 3)) if rng.random() < 1/3) for t in range(T)]   # poisson-ish integer arrivals/s
def sim(name, min_rep, idle_to_zero=None, predictive=False, cooldown=180):
    ready = min_rep; booting = []; q = deque(); waits = []; rep_s = 0; last_busy = 0; events = 0; ewma = 0.0; last_down = -999
    for t in range(T):
        done = [b for b in booting if b <= t]; booting = [b for b in booting if b > t]; ready += len(done)
        for _ in range(arr[t]): q.append(t)
        cap = ready * CAP; served = 0
        while q and served < cap: waits.append(t - q.popleft()); served += 1
        ewma = 0.8 * ewma + 0.2 * arr[t]
        if arr[t] or q: last_busy = t
        want = math.ceil((ewma + len(q) / 30) / (CAP * 0.7))
        if predictive:                                       # forecast from the known schedule 120 s ahead
            f = 45 if any(s - 120 <= t + 120 and t < s + 240 for s in (900, 2400, 4500)) else 1.5
            want = max(want, math.ceil(f / (CAP * 0.7)))
        floor = min_rep
        if idle_to_zero is not None and t - last_busy < idle_to_zero: floor = max(floor, 1)
        want = max(want, floor)
        have = ready + len(booting)
        if want > have:
            booting += [t + STARTUP] * (want - have); events += want - have
        elif want < ready and t - last_down >= cooldown and not q:
            ready -= 1; last_down = t
        rep_s += ready + len(booting)
    for _ in q: waits.append(T - 0)
    w = sorted(waits); n = len(w)
    cold = sum(1 for x in w if x >= STARTUP); slow = sum(1 for x in w if x > 10)
    print(f"{name:<34}{n:>7}{cold:>10}{slow:>9}{w[int(0.99*n)]:>8}{max(w):>7}{rep_s/3600:>10.1f}{events:>8}")
print(f"{'strategy':<34}{'reqs':>7}{'wait>=90s':>10}{'wait>10s':>9}{'p99 s':>8}{'max s':>7}{'rep-hours':>10}{'boots':>8}")
sim("scale to zero (idle 300 s)", 0, idle_to_zero=300)
sim("min 2 replicas", 2)
sim("predictive pre-scale, min 0", 0, idle_to_zero=300, predictive=True)
sim("predictive + min 1", 1, predictive=True)
sim("min 2, NO cooldown (flapping)", 2, cooldown=0)
