"""Queue length -> replicas, KEDA/HPA style. Made-up numbers; a model of the rules, not KEDA code.
One tick = 30 s (pollingInterval)."""
import math

TARGET = 50          # messages per pod (queueLength)
RATE = 40            # messages one READY pod finishes per tick
COLD = 4             # ticks (= 120 s) for a new pod to become ready: made-up, GPU/model load can be longer
MAXR, COOLDOWN, STAB = 10, 10, 10   # max replicas; ticks before scale to zero; HPA scale-down window in ticks
ARRIVALS = [0, 0] + [100] * 4 + [400] * 3 + [0] * 20          # messages arriving per tick

def run(min_replicas, verbose):
    queue, pods, window, last_active = 0, [], [], -99      # pods = list of tick when each becomes ready
    first_done, idle_pod_ticks, prev = None, 0, None
    if min_replicas: pods = [-1] * min_replicas              # warm pods already ready
    if verbose: print(f"{'tick':>4} {'arrive':>6} {'queue':>5} {'desired':>7} {'pods':>4} {'ready':>5} {'done':>5}")
    for t, arr in enumerate(ARRIVALS):
        queue += arr
        if queue > 0 or arr > 0: last_active = t
        desired = math.ceil(queue / TARGET)                  # HPA rule for an AverageValue target
        window = (window + [desired])[-STAB:]
        want = min(MAXR, max(window))                        # up: immediate. down: highest of the last STAB ticks
        floor = 1 if (t - last_active) < COOLDOWN else 0     # stay at 1 until cooldown passes
        want = max(want, floor, min_replicas)
        while len(pods) < want: pods.append(t + COLD)        # new pod: ready COLD ticks later
        while len(pods) > want: pods.pop()                   # remove the newest first
        ready = sum(1 for r in pods if r <= t)
        done = min(queue, ready * RATE); queue -= done
        if done and first_done is None: first_done = t
        if queue == 0 and arr == 0: idle_pod_ticks += len(pods)
        if verbose and (t <= 12 or len(pods) != prev):     # print early ticks and every change in pod count
            print(f"{t:>4} {arr:>6} {queue:>5} {desired:>7} {len(pods):>4} {ready:>5} {done:>5}")
        prev = len(pods)
    return first_done, idle_pod_ticks

print("=== minReplicaCount 0 ===")
f0, idle0 = run(0, True)
f1, idle1 = run(1, False)
print()
print(f"first message processed at tick: min=0 -> {f0} ({(f0 - 2) * 30} s after the first message at tick 2);  min=1 -> {f1} ({(f1 - 2) * 30} s)")
print(f"pod-ticks spent with an empty queue: min=0 -> {idle0};  min=1 -> {idle1}")
