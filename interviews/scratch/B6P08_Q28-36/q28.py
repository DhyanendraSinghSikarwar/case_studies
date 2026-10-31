# Illustrative numbers only. Backlog, drain time, shedding and cost for a GPU service during a traffic jump.
import math
base, cap, peak, load_s = 400, 500, 900, 90
per_pod = 125                       # req/s one GPU pod can serve (illustrative)
assert cap // per_pod == 4
# 1. Backlog with no shedding: arrivals minus service for 90 s.
backlog = (peak - cap) * load_s
assert backlog == 36000
wait_last = backlog / cap           # seconds the last queued request waits at t=90
assert wait_last == 72.0
# 2. Real timeline: autoscaler on a queue signal still needs time to notice (scrape + evaluate).
detect_s = 15
backlog_real = (peak - cap) * (detect_s + load_s)
assert backlog_real == 42000
# 3. Drain after new capacity arrives depends on how many pods you ask for.
def drain(new_cap, backlog=backlog_real):
    return backlog / (new_cap - peak)
need_pods = math.ceil(peak * 1.3 / per_pod)       # 30% headroom
assert need_pods == 10
print('drain with 8 pods (1000/s):', round(drain(8 * per_pod)), 's')
print('drain with 10 pods (1250/s):', round(drain(10 * per_pod)), 's')
assert round(drain(1000)) == 420 and round(drain(1250)) == 120
# 4. Bounded queue: a 2 s client timeout means a queue deeper than cap*2 only holds dead requests.
timeout_s = 2
qmax = cap * timeout_s
assert qmax == 1000
q = shed = served = 0
for t in range(load_s):               # per-second simulation, jump at t=0
    arrive = peak
    take = min(cap, arrive + q)        # serve up to capacity
    served += take
    q = q + arrive - take
    if q > qmax:
        shed += q - qmax; q = qmax
assert served == 45000
arrivals = peak * load_s
assert arrivals == 81000 and shed + q + served == arrivals
print('served', served, 'queued', q, 'shed', shed, 'shed share', round(shed / arrivals, 3))
assert shed == 35000 and round(shed / arrivals, 3) == 0.432
# 5. Warm headroom: pods needed to absorb the jump with zero scaling vs the cost of holding them.
hold_pods = math.ceil(peak / per_pod)
extra = hold_pods - cap // per_pod
assert hold_pods == 8 and extra == 4
pod_hour = 10                          # illustrative cost units per pod-hour
standby_day = extra * pod_hour * 24
loss_per_spike = shed * 0.05           # 0.05 units of value per failed request (illustrative)
print('standby cost/day', standby_day, 'loss per spike', loss_per_spike, 'break-even spikes/day', round(standby_day / loss_per_spike, 2))
assert standby_day == 960 and loss_per_spike == 1750.0
# 6. Escalation rules written down (illustrative thresholds)
rules = {'shed_if_queue_wait_s_over': 2, 'manual_scale_if_no_new_pod_after_s': 120, 'page_human_if_quota_blocked': True}
assert rules['manual_scale_if_no_new_pod_after_s'] > detect_s
