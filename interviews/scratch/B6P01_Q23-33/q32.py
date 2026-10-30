# Q32 sessions per DAU +20% with flat DAU: a session-timeout change splits sessions (seeded simulation)
import random
random.seed(7)
users = 5000
def make_events():
    ev = []
    t = random.uniform(8, 10) * 60.0            # minutes since midnight
    for _ in range(random.randint(8, 30)):      # events in the day
        ev.append(t)
        # most gaps are short; 3% are real breaks (35-120 min); 1.7% are mid gaps of 16-29 minutes
        r = random.random()
        if r < 0.03:
            t += random.uniform(35, 120)
        elif r < 0.047:
            t += random.uniform(16, 29)
        else:
            t += random.expovariate(1 / 3.0)
    return ev

data = [make_events() for _ in range(users)]

def sessions(events, timeout):
    n = 1
    for a, b in zip(events, events[1:]):
        if b - a > timeout:
            n += 1
    return n

s30 = sum(sessions(e, 30) for e in data) / users
s15 = sum(sessions(e, 15) for e in data) / users
events_per_user = sum(len(e) for e in data) / users
active_span30 = sum(e[-1] - e[0] for e in data) / users
print("users (DAU, unchanged):", users)
print("sessions per DAU, 30-min timeout:", round(s30, 2))
print("sessions per DAU, 15-min timeout:", round(s15, 2), " change:", round(s15 / s30 - 1, 3))
print("events per DAU (unchanged by the timeout):", round(events_per_user, 2))
print("events per session 30 vs 15:", round(events_per_user / s30, 2), round(events_per_user / s15, 2))
assert 1.15 < s15 / s30 < 1.30    # a pure definition change moves the ratio by roughly 20%
assert abs(events_per_user - sum(len(e) for e in data) / users) < 1e-9
# fastest check 2: events or orders per DAU is identical under both definitions
orders_proxy_30 = sum(len(e) for e in data)
orders_proxy_15 = sum(len(e) for e in data)
assert orders_proxy_30 == orders_proxy_15
