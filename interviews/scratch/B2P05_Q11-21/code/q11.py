import numpy as np
rng = np.random.default_rng(0)
# SYNTHETIC: a safety classifier scores prompts in [0,1] (higher = more likely unsafe).
# Three populations: clearly benign, benign-but-edgy (shares wording with unsafe), truly unsafe.
n = 2000
benign = rng.beta(2, 8, n)     # mostly low scores
edgy   = rng.beta(4, 5, n)     # overlaps the unsafe region
unsafe = rng.beta(7, 3, n)     # mostly high scores
print("thr  over-refusal(edgy)  over-refusal(benign)  unsafe-compliance")
for thr in [0.3, 0.4, 0.5, 0.6, 0.7, 0.8, 0.9]:
    over_edgy = (edgy >= thr).mean()
    over_ben = (benign >= thr).mean()
    unsafe_ok = (unsafe < thr).mean()   # model complies with an unsafe prompt
    print(f"{thr:.1f}  {over_edgy:18.3f}  {over_ben:20.3f}  {unsafe_ok:17.3f}")
