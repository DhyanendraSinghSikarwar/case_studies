import numpy as np
rng = np.random.default_rng(0)
# SYNTHETIC: a "refusal score" per prompt; harmful prompts score higher on average.
n = 5000
harmful = rng.normal(0.70, 0.18, n)   # score on unsafe prompts
benign  = rng.normal(0.35, 0.18, n)   # score on benign-but-edgy prompts
print("refuse if score >= t")
print(" t    unsafe_compliance  over_refusal")
for t in [0.2, 0.3, 0.4, 0.5, 0.6, 0.7, 0.8]:
    unsafe_comply = np.mean(harmful < t)    # harmful prompt answered
    over_refuse   = np.mean(benign >= t)    # benign prompt refused
    print(f"{t:.1f}  {unsafe_comply:17.3f}  {over_refuse:12.3f}")
# Pareto front over a fine sweep: a threshold is dominated if another is better on both axes
ts = np.linspace(0, 1, 101)
pts = np.array([(np.mean(harmful < t), np.mean(benign >= t)) for t in ts])
def dominated(i):
    return np.any((pts[:,0] <= pts[i,0]) & (pts[:,1] <= pts[i,1]) & ((pts[:,0] < pts[i,0]) | (pts[:,1] < pts[i,1])))
print("non-dominated thresholds:", int(sum(not dominated(i) for i in range(len(ts)))), "of", len(ts))
# a tuned (better) model shifts the curve: separation 0.35 -> 0.50
harmful2 = rng.normal(0.85, 0.18, n)
t = 0.6
print(f"t=0.6 base: unsafe {np.mean(harmful<t):.3f}, over-refusal {np.mean(benign>=t):.3f}")
print(f"t=0.6 better separation: unsafe {np.mean(harmful2<t):.3f}, over-refusal {np.mean(benign>=t):.3f}")
