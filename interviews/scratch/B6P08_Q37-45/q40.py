# Q40: preemptible training, 20 h run, 4 interruptions, checkpoint every 3 h (invented numbers)
import math, random
import numpy as np

RUN_H, N_INT, CK_H = 20, 4, 3.0
exp_loss = N_INT * CK_H / 2
worst_loss = N_INT * CK_H
print("expected lost work", exp_loss, "h | worst case", worst_loss, "h")
assert exp_loss == 6.0 and worst_loss == 12.0
print("expected total compute", RUN_H + exp_loss, "h | worst", RUN_H + worst_loss, "h")
assert RUN_H + exp_loss == 26.0 and RUN_H + worst_loss == 32.0

# Check the 'half an interval' average by simulation: preemption at a uniform random time
rnd = random.Random(3)
losses = [(rnd.uniform(0, 1000) % CK_H) for _ in range(100_000)]
print("simulated mean loss per preemption", round(sum(losses) / len(losses), 3), "max", round(max(losses), 3))
assert abs(sum(losses) / len(losses) - 1.5) < 0.02 and max(losses) < 3.0

# Choosing the interval: Young's first-order rule T = sqrt(2 * C * MTBF), C = cost of one checkpoint
C_h = 3 / 60                       # 3 minutes per checkpoint (invented)
mtbf_h = RUN_H / N_INT             # 5 h between interruptions
t_opt = math.sqrt(2 * C_h * mtbf_h)
print("Young interval (h):", round(t_opt, 2), "=", round(t_opt * 60), "min")
assert round(t_opt, 2) == 0.71

def overhead(T):                   # checkpoint cost + expected re-done work, hours over the run
    return (RUN_H / T) * C_h + N_INT * T / 2
for T in (3.0, 1.0, t_opt, 0.25):
    print(f"interval {T:5.2f} h -> overhead {overhead(T):5.2f} h")
assert overhead(t_opt) < overhead(3.0) and overhead(t_opt) < overhead(0.25)
assert round(overhead(3.0), 2) == 6.33 and round(overhead(t_opt), 2) == 2.83

# Does resume give the same model? Toy logistic regression, minibatch SGD, seeded shuffle.
def make_data():
    g = np.random.default_rng(0)
    X = g.normal(size=(400, 5)); y = (X @ np.array([1, -2, 0.5, 0, 1.5]) + g.normal(size=400) > 0) * 1.0
    return X, y

def train(steps, state=None, stop_at=None, save_rng=True):
    X, y = make_data()
    if state is None:
        w = np.zeros(5); v = np.zeros(5); step = 0; rng = np.random.default_rng(42)
    else:
        w, v, step = state["w"].copy(), state["v"].copy(), state["step"]
        rng = np.random.default_rng(42) if not save_rng else np.random.default_rng()
        if save_rng: rng.bit_generator.state = state["rng"]
    while step < steps:
        idx = rng.choice(len(X), 32, replace=False)
        p = 1 / (1 + np.exp(-X[idx] @ w)); grad = X[idx].T @ (p - y[idx]) / 32
        v = 0.9 * v + grad; w = w - 0.1 * v; step += 1      # momentum = optimizer state
        if stop_at is not None and step == stop_at:
            return {"w": w, "v": v, "step": step, "rng": rng.bit_generator.state}
    return {"w": w, "v": v, "step": step, "rng": rng.bit_generator.state}

full = train(200)
ck = train(200, stop_at=120)                         # preempted: checkpoint at step 120
resumed = train(200, state=ck)                       # weights + momentum + rng + step restored
no_rng = train(200, state=ck, save_rng=False)        # forgot the RNG state
no_mom = dict(ck); no_mom["v"] = np.zeros(5)         # forgot the optimizer state
no_mom = train(200, state=no_mom)
print("resume exact:", np.array_equal(full["w"], resumed["w"]))
print("without rng state exact:", np.array_equal(full["w"], no_rng["w"]))
print("without optimizer state exact:", np.array_equal(full["w"], no_mom["w"]))
assert np.array_equal(full["w"], resumed["w"])
assert not np.array_equal(full["w"], no_rng["w"]) and not np.array_equal(full["w"], no_mom["w"])
