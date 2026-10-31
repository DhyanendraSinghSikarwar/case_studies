# Q23: stale clicks_last_hour served for 5 hours with a 7-hour lag. Synthetic, seeded, illustrative.
import numpy as np
rng = np.random.default_rng(23)
LAG_H, DURATION_H, RPS = 7, 5, 100
served_requests = RPS * DURATION_H * 3600
print(f"requests scored with a stale feature: {served_requests:,}")
assert served_requests == 1_800_000
# --- freshness check: age = now - feature event time; page when age > 30 min
def age_minutes(now_min, event_min): return now_min - event_min
FRESH_LIMIT = 30
incident_start = 12 * 60                                  # 12:00; lag appears at once
checks = range(incident_start - 10, incident_start + 60)  # one check a minute
first_alert = next(t for t in checks if age_minutes(t, t - (LAG_H*60 if t >= incident_start else 5)) > FRESH_LIMIT)
detect_delay_min = first_alert - incident_start
print(f"with a per-minute age check the alert fires in the first one-minute check ({detect_delay_min} minutes after the lag starts) (the incident ran undetected for {DURATION_H*60} minutes)")
assert detect_delay_min == 0 and DURATION_H * 60 == 300
# --- damage: replay the 5 hours with true versus served feature values
users = 50_000
level = rng.lognormal(1.0, 0.5, users)                    # user's typical clicks per hour
def diurnal(h): return 1 + 0.8 * np.sin(2 * np.pi * (h - 14) / 24)
def clicks(h): return rng.poisson(level * diurnal(h))
w, b, THR = 0.35, -3.4, 0.5
def score(c, other): return 1 / (1 + np.exp(-(w * np.log1p(c) * 3 + other + b)))
other = rng.normal(0, 0.6, users)                         # all other features
rows = []
for h in range(12, 12 + DURATION_H):                      # incident hours 12..16
    s_true = score(clicks(h), other)
    s_stale = score(clicks(h - LAG_H), other)
    flipped = ((s_true >= THR) != (s_stale >= THR)).mean()
    rows.append((h, np.abs(s_true - s_stale).mean(), flipped))
    print(f"hour {h}: mean |score error| = {rows[-1][1]:.3f}, decisions flipped = {flipped:.1%}")
tot_flip = np.mean([r[2] for r in rows])
exp_flips = tot_flip * served_requests
print(f"average flipped share {tot_flip:.1%} -> about {exp_flips:,.0f} of {served_requests:,} decisions to review (projection from the simulation, not measured)")
assert all(0 < r[2] < 0.5 for r in rows) and 0.002 < tot_flip < 0.05
# --- TTL pattern: a stale read returns None, and the service applies the fallback explicitly
def get_feature(store, key, now, ttl):
    v = store.get(key)
    return None if v is None or now - v["ts"] > ttl else v["value"]
store = {"u1": {"value": 7, "ts": 100}}
assert get_feature(store, "u1", now=110, ttl=30) == 7 and get_feature(store, "u1", now=400, ttl=30) is None
print("TTL read: fresh value returned at age 10, None at age 300 (service then uses the declared fallback)")
