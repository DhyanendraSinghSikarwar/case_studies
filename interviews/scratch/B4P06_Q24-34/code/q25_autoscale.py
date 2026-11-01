# Q25: replica maths and a spike simulation. All numbers are inputs; no cluster.
import math

def replicas_needed(in_flight, target_per_replica, min_r=1, max_r=50):
    """Desired replicas from requests in flight (Little's law: in_flight = rps * latency)."""
    return max(min_r, min(max_r, math.ceil(in_flight / target_per_replica)))

def simulate(rps_at, secs, service_ms, conc_per_replica, start_delay, min_r, budget_ms, target, tick=1):
    """Per-second fluid simulation. Each replica serves conc/service_s req/s.
    Backlog grows when arrivals exceed capacity. A request arriving in a second waits
    backlog/capacity seconds; counts as late if wait + service > budget."""
    replicas, pending, backlog, late, total = min_r, [], 0.0, 0.0, 0.0
    log = []
    for t in range(secs):
        pending_ready = [p for p in pending if p <= t]
        replicas += len(pending_ready); pending = [p for p in pending if p > t]
        arrivals = rps_at(t)
        cap = replicas * conc_per_replica / (service_ms / 1000)
        wait_ms = (backlog / cap) * 1000 if cap else 1e9
        total += arrivals
        if wait_ms + service_ms > budget_ms: late += arrivals
        backlog = max(0.0, backlog + arrivals - cap)
        in_flight = arrivals * service_ms / 1000   # Little: rps x seconds; queued work is not counted here
        want = replicas_needed(in_flight, target, min_r)
        have = replicas + len(pending)
        for _ in range(max(0, want - have)): pending.append(t + start_delay)
        if t % 30 == 0: log.append((t, arrivals, replicas, len(pending), round(wait_ms)))
    return late, total, log

if __name__ == "__main__":
    assert replicas_needed(0, 4) == 1
    assert replicas_needed(40, 4) == 10
    assert replicas_needed(41, 4) == 11
    assert replicas_needed(1000, 4, max_r=20) == 20
    print("replica function tests passed")
    print("worked: 200 rps * 0.100 s = 20 in flight; target 3 per replica (capacity 4, so headroom) ->", replicas_needed(200*0.1, 3), "replicas")
    spike = lambda t: 20 if t < 60 else 200
    for delay in (90, 10):
        late, total, log = simulate(spike, 300, 100, 4, delay, min_r=1, budget_ms=500, target=3)
        print(f"start-up delay {delay}s, min replicas 1: late {late:.0f} of {total:.0f} requests ({100*late/total:.1f}%)")
        if delay == 90:
            for row in log[:6]: print("  t=%3d rps=%3d ready=%2d starting=%2d wait_ms=%d" % row)
    late, total, _ = simulate(spike, 300, 100, 4, 90, min_r=7, budget_ms=500, target=3)
    print(f"start-up delay 90s, min replicas 7 (pre-warmed): late {late:.0f} of {total:.0f} ({100*late/total:.1f}%)")
