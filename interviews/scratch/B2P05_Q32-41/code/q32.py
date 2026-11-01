# Standalone, numpy only. SYNTHETIC data: a made-up reward model (RM) scored against made-up human labels.
import numpy as np
rng = np.random.default_rng(0)
N = 20000
true_gap = rng.normal(0, 1.5, N)              # hidden true quality difference (chosen minus rejected) for each pair
p_human = 1 / (1 + np.exp(-true_gap))         # humans prefer A over B with this probability (label noise built in)
human_pick_A = rng.random(N) < p_human        # observed human label: True = A preferred
noise_ceiling = np.mean(np.maximum(p_human, 1 - p_human))   # best possible accuracy against these noisy labels

def rm_delta(scale, noise, g):                # RM score difference = scale * (true gap + RM error)
    return scale * (true_gap + rng.normal(0, noise, N) + g)

def ece(prob_A, y, bins=10):                  # expected calibration error on P(A preferred)
    conf = np.where(prob_A >= .5, prob_A, 1 - prob_A); pred = prob_A >= .5; correct = pred == y
    edges = np.linspace(.5, 1, bins + 1); out = 0
    for lo, hi in zip(edges[:-1], edges[1:]):
        m = (conf > lo) & (conf <= hi)
        if m.any(): out += m.mean() * abs(correct[m].mean() - conf[m].mean())
    return out

print(f"noise ceiling (best possible accuracy on these labels): {noise_ceiling:.3f}")
for name, scale, noise, shift in [("good RM, calibrated scale", 1.0, 0.5, 0.0),
                                  ("overconfident RM (x4 score scale)", 4.0, 0.5, 0.0),
                                  ("worse RM (more error)", 1.0, 2.0, 0.0)]:
    d = rm_delta(scale, noise, shift); p = 1 / (1 + np.exp(-d))
    acc = np.mean((d > 0) == human_pick_A)
    print(f"{name:42s} accuracy {acc:.3f}  ECE {ece(p, human_pick_A):.3f}")

# Best-of-n probe: RM picks the top of n candidates; how often does a (noisy) human judge prefer it to a random candidate?
def bon_win(n, noise, trials=4000):
    wins = 0
    for _ in range(trials):
        q = rng.normal(0, 1.5, n); rm = q + rng.normal(0, noise, n)
        pick, other = np.argmax(rm), rng.integers(n)
        if other == pick: other = (pick + 1) % n
        wins += rng.random() < 1 / (1 + np.exp(-(q[pick] - q[other])))
    return wins / trials
print("best-of-n win rate vs a random candidate (human-style noisy judge):")
for n in (2, 8, 32): print(f"  n={n:2d}  good RM {bon_win(n, 0.5):.3f}   weak RM {bon_win(n, 2.0):.3f}")
