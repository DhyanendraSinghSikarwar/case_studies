# Q43: failover simulation with replication lag. Seeded. Abstract time in seconds.
import random
random.seed(43)
TPS = 200            # decisions per second
def sim(design, lag_s, detect_s, switch_s, fail_t=1000, horizon=1200):
    lost = stale_until = 0; served_stale = 0
    down = detect_s + switch_s
    if design == "active-passive":   # warm standby, async replication
        lost = int(TPS * down)                       # decisions with no answer while failing over
        stale_window = lag_s                         # feature writes not yet replicated
        decisions_log_lost = int(TPS * lag_s)        # log entries not replicated
    elif design == "active-active":  # both serve; traffic shifts, shared async feature replication
        lost = int(TPS * detect_s * 0.5)             # half of traffic sees errors until health check
        stale_window = lag_s
        decisions_log_lost = int(TPS * lag_s * 0.5)  # only the failed region's share
    else:                            # per-region independent: no cross-region state, no cross-region cover
        lost = int(TPS * 0.5 * 3600)               # failed region's users stay down for an assumed 1 h until it returns
        stale_window = 0                             # each region has its own features, no replica lag
        decisions_log_lost = 0                       # regional log stays; but users pinned there are down w/o failover
    return lost, stale_window, decisions_log_lost
print(f"{'design':26s}{'lost reqs':>10s}{'stale win s':>12s}{'log entries lost':>18s}  idle capacity")
idle = {"active-passive": "high (standby ~100%)", "active-active": "low (headroom ~ 50%)", "per-region independent": "low, but no cross-region cover"}
for d in idle:
    jitter = random.uniform(0.9, 1.1)
    r = sim(d, lag_s=5 * jitter, detect_s=30, switch_s=120 if d == "active-passive" else 10)
    print(f"{d:26s}{r[0]:>10d}{r[1]:>12.1f}{r[2]:>18d}  {idle[d]}")
print("residency: per-region independent keeps data in region; replication across regions needs a residency check")
