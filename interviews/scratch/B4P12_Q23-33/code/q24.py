# Q24: staged rollout of a bad model to a 100,000 device fleet. Seeded numpy. Abstract, sandbox-only numbers.
import numpy as np
SEED = 24
N = 100_000
rng = np.random.default_rng(SEED)
app = rng.choice([1, 2, 3], size=N, p=[0.25, 0.45, 0.30])      # three app versions; model v2 needs app >= 2
eligible = np.flatnonzero(app >= 2)                              # capability check: 75,000 devices
order = rng.permutation(eligible)                                # random cohort order
STAGES = [0.005, 0.02, 0.10, 0.50, 1.0]                          # share of eligible devices
SESS = 20                                                        # sessions per device during one soak window
BASE_CRASH, BAD_CRASH = 0.005, 0.03                              # crash per session: old model vs bad model
GATE_CRASH = 0.015                                               # halt when stage crash rate is above this
BASE_CONF, DROP = 0.80, 0.12                                     # mean top-class confidence; silent-bad model drops it
GATE_CONF_DROP = 0.05

def simulate(scenario, proxy_gate):
    exposed = 0
    for i, s in enumerate(STAGES):
        cohort = order[: int(len(order) * s)]
        new = cohort                                             # every device in the cohort runs the new model
        crash_p = BAD_CRASH if scenario == "crashy" else BASE_CRASH
        crashes = rng.binomial(SESS, crash_p, size=len(new)).sum()
        crash_rate = crashes / (SESS * len(new))
        conf = BASE_CONF - (DROP if scenario == "silent" else 0) + rng.normal(0, 0.02)
        exposed = len(cohort)
        halted = crash_rate > GATE_CRASH or (proxy_gate and BASE_CONF - conf > GATE_CONF_DROP)
        print(f"  stage {i+1} ({s:>5.1%}): exposed={exposed:>6} crash_rate={crash_rate:.4f} conf={conf:.3f} -> {'HALT' if halted else 'go'}")
        if halted: return exposed
    return exposed

print("eligible devices:", len(eligible), "of", N)
for name, scen, proxy in [("A crashy model, crash gate only", "crashy", False),
                          ("B silent accuracy loss, crash gate only", "silent", False),
                          ("C silent accuracy loss, crash + confidence-proxy gate", "silent", True)]:
    print(name); e = simulate(scen, proxy)
    print(f"  => devices exposed when it stopped: {e}\n")
