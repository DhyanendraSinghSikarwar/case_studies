"""maxSurge / maxUnavailable arithmetic and a tick-by-tick rollout sketch."""
import math, sys, yaml

def resolve(v, replicas, round_up):
    if isinstance(v, str) and v.endswith("%"):
        x = replicas * int(v[:-1]) / 100
        return math.ceil(x) if round_up else math.floor(x)      # surge rounds up, unavailable rounds down
    return int(v)

def limits(replicas, surge="25%", unavail="25%"):
    s, u = resolve(surge, replicas, True), resolve(unavail, replicas, False)
    if s == 0 and u == 0:
        raise ValueError("both zero: rollout can never make progress (API rejects it)")
    return s, u, replicas + s, replicas - u        # surge, unavailable, max total, min available

def simulate(replicas, surge, unavail, new_is_ready=True):
    s, u, max_total, min_avail = limits(replicas, surge, unavail)
    old, new, new_ready, ticks = replicas, 0, 0, []
    for t in range(1, 40):
        new_ready = new if new_is_ready else 0
        new += max(0, min(replicas - new, max_total - (old + new)))          # create new pods up to surge
        ready_now = old + new_ready                                           # old are ready, new count when ready
        old -= max(0, min(old, ready_now - min_avail))                        # delete old while availability allows
        ticks.append((t, old, new, old + new_ready))
        if old == 0 and new == replicas:
            break
    return ticks

for r, s, u in [(10, "25%", "25%"), (4, 1, 0), (3, "25%", "25%"), (9, "25%", 0)]:
    su, un, mt, ma = limits(r, s, u)
    print(f"replicas={r} maxSurge={s} maxUnavailable={u}: surge={su} unavailable={un} max_total={mt} min_available={ma}")

print("\nrollout 4 replicas, maxSurge=1, maxUnavailable=0 (tick, old, new_created, ready)")
for row in simulate(4, 1, 0):
    print(row)
print("\nbad model whose pods never become Ready (4 replicas, surge 1, unavail 0): first ticks")
for row in simulate(4, 1, 0, new_is_ready=False)[:4]:
    print(row, "<- old pods kept, rollout stuck")
print("\ncanary split by replica count: 9 stable + 1 canary ->", 1 / (9 + 1) * 100, "% of requests (roughly, per-connection)")

docs = [d for d in yaml.safe_load_all(open(sys.argv[1])) if d]
canary = docs[0]
print("kserve file parses; canaryTrafficPercent =", canary["spec"]["predictor"]["canaryTrafficPercent"])
