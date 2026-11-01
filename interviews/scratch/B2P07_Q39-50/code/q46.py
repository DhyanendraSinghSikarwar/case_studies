# Standalone, numpy only. SYNTHETIC judge: every probability and bias below is ASSUMED. Shows why single-order judging misleads and what the swap fixes.
import numpy as np
rng = np.random.default_rng(11)
sig = lambda x: 1 / (1 + np.exp(-x)); logit = lambda p: np.log(p / (1 - p))
# ASSUMED "true" preference for system A (graph-style) over B (vector RAG) by question type, if judged by a perfect judge
TRUE_A = {"global": 0.65, "local": 0.45, "lookup": 0.35}
N_PER = 400                      # questions per type
POS_BIAS = 0.7                   # ASSUMED: judge favours whatever is shown first (logit units)
LEN_BIAS = 0.8                   # ASSUMED: judge favours the longer answer (per unit of relative length difference)
LEN_A_OVER_B = 0.4               # ASSUMED: A's answers are 40 percent longer on average
def judge(first_is_A, true_pA, rel_len_A_minus_B):
    """Return True if A wins this single judgement."""
    z = logit(true_pA) + LEN_BIAS * rel_len_A_minus_B                       # length bias favours A when A is longer
    z_first = z + (POS_BIAS if first_is_A else -POS_BIAS)                   # position bias favours whoever is first
    return rng.random() < sig(z_first)

def run(order, per_type_n=N_PER, len_diff=LEN_A_OVER_B):
    res = {}
    for t, p in TRUE_A.items():
        wins, flips = [], 0
        for _ in range(per_type_n):
            # per-question latent: this question's true preference is p plus noise, so questions differ
            pq = float(np.clip(p + rng.normal(0, 0.1), 0.02, 0.98)); L = len_diff + rng.normal(0, 0.1)
            if order == "A_first": w = judge(True, pq, L)
            elif order == "B_first": w = judge(False, pq, L)
            else:                                                            # swap: judge both orders, average; flag disagreements
                w1, w2 = judge(True, pq, L), judge(False, pq, L); w = (float(w1) + float(w2)) / 2; flips += (w1 != w2)
            wins.append(w)
        res[t] = (float(np.mean(wins)), flips / per_type_n)
    return res

print("ASSUMED true A-over-B preference:", TRUE_A, "| position bias", POS_BIAS, "| length bias", LEN_BIAS, "| A is", int(LEN_A_OVER_B * 100), "percent longer")
print(f"{'judging protocol':28s}" + "".join(f"{t:>10s}" for t in TRUE_A) + "   (A win rate; 0.5 = no preference)")
for name, order, ld in [("A always first", "A_first", LEN_A_OVER_B), ("B always first", "B_first", LEN_A_OVER_B),
                        ("both orders averaged", "swap", LEN_A_OVER_B), ("both orders + length-matched", "swap", 0.0)]:
    r = run(order, len_diff=ld); print(f"{name:28s}" + "".join(f"{r[t][0]:>10.2f}" for t in TRUE_A) + (f"   order-flip rate {np.mean([r[t][1] for t in TRUE_A]):.2f}" if order == "swap" else ""))
r = run("A_first"); r2 = run("B_first")
assert r["lookup"][0] > r2["lookup"][0] + 0.2                                 # the order alone moves the win rate a lot
# repeated runs: report mean and spread over 10 repeats, not one run
reps = [run("swap")["global"][0] for _ in range(10)]
print("global, swap protocol, 10 repeated runs: mean %.3f, min %.3f, max %.3f" % (np.mean(reps), min(reps), max(reps)))

# cost-matched view: indexing cost is part of the comparison (ASSUMED numbers, same units for both)
index_cost = {"A (graph-style)": 11.0, "B (vector)": 1.0}; per_q = {"A (graph-style)": 0.18, "B (vector)": 0.01}
mix = {"global": 0.1, "local": 0.5, "lookup": 0.4}                              # ASSUMED production question mix
for nq in (1000, 20000):
    tot = {k: index_cost[k] + nq * per_q[k] for k in index_cost}; print(f"  total cost for {nq} queries:", {k: round(v, 1) for k, v in tot.items()})
rr = run("swap"); print("mix-weighted A win rate (swap protocol):", round(sum(mix[t] * rr[t][0] for t in mix), 2), "| global-only:", round(rr["global"][0], 2))
