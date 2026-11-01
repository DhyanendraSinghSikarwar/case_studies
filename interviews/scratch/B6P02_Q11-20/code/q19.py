# Q19: nightly retrain versus schedule versus trigger (illustrative simulation, seeded, numpy only)
import numpy as np
rng = np.random.default_rng(19)

DAYS, RUNS = 180, 400
FRESH = 90.0          # accuracy (%) of a freshly trained model, before retrain noise
DECAY = 0.03          # accuracy points lost per day of model age (illustrative; the real value is the thing to measure)
RETRAIN_SD = 0.25     # run-to-run noise of one retrain, in accuracy points (data sampling + seed)
GLITCH_P = 0.02       # chance a retrain is trained on a corrupted extract
GLITCH_HIT = 3.0      # accuracy points lost by a glitch model
COST = 1.0            # cost units per retrain run (compute + review); report counts as well
GATE_SD = 0.3         # the champion-challenger gate measures accuracy with this noise (points)

def simulate(policy, gate):
    acc_log = np.zeros((RUNS, DAYS)); retrains = np.zeros(RUNS); bad_live = np.zeros(RUNS)
    for r in range(RUNS):
        level = FRESH + rng.normal(0, RETRAIN_SD)      # the live model's accuracy when deployed
        age = 0; last_obs = level
        for d in range(DAYS):
            acc = level - DECAY * age
            acc_log[r, d] = acc
            obs = acc + rng.normal(0, 0.15)            # matured-label weekly estimate (noisy)
            retrain = (policy == "nightly") or \
                      (policy == "weekly" and d % 7 == 6) or \
                      (policy == "monthly" and d % 30 == 29) or \
                      (policy == "trigger" and obs < FRESH - 1.0)
            if retrain:
                retrains[r] += 1
                cand = FRESH + rng.normal(0, RETRAIN_SD)
                glitch = rng.random() < GLITCH_P
                if glitch: cand -= GLITCH_HIT
                # gate: deploy only if candidate looks at least as good as the live model, measured with noise
                deploy = True
                if gate:
                    deploy = (cand + rng.normal(0, GATE_SD)) >= (acc + rng.normal(0, GATE_SD)) - 0.2
                if deploy:
                    level, age = cand, 0
                    if glitch: bad_live[r] += 1
                else:
                    age += 1
            else:
                age += 1
    return acc_log, retrains, bad_live

rows = []
for policy, gate in [("nightly", False), ("nightly", True), ("weekly", True), ("monthly", True), ("trigger", True)]:
    a, rt, bl = simulate(policy, gate)
    rows.append((policy, gate, a.mean(), (a < 88.5).mean(), rt.mean(), bl.mean()))
print("policy   gate  mean acc  days below 88.5  retrains/180d  glitch models deployed")
for p, g, m, f, rt, bl in rows:
    print(f"{p:8} {str(g):5} {m:8.3f}  {100*f:12.1f}%  {rt:12.1f}  {bl:10.2f}")
R = {(p, g): (m, f, rt, bl) for p, g, m, f, rt, bl in rows}
# Claims that go into the answer
assert R[("nightly", False)][3] > 1.0                      # nightly without a gate ships glitch models
assert R[("nightly", True)][3] < R[("nightly", False)][3]  # a gate removes most of them
assert R[("weekly", True)][0] > R[("monthly", True)][0]    # some retraining beats too little
print(f"nightly+gate vs weekly+gate: mean accuracy difference {R[('nightly', True)][0]-R[('weekly', True)][0]:+.3f} points for {R[('nightly', True)][2]-R[('weekly', True)][2]:.0f} extra retrains")
# Back-of-envelope: average age under a schedule of T days is (T-1)/2 days (age 0 right after training)
for T in (1, 7, 30):
    print(f"schedule every {T:2d} days: mean age {(T-1)/2:.1f} days -> average decay loss {(T-1)/2*DECAY:.3f} points")
assert abs((7 - 1) / 2 * DECAY - 0.09) < 1e-12 and abs((30 - 1) / 2 * DECAY - 0.435) < 1e-12
