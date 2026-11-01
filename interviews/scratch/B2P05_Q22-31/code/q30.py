import numpy as np
# SYNTHETIC toy: a policy over 5 responses (softmax of logits). Data was sampled from pi_0 (offline).
# How far from usable is that data as the policy moves? Look at importance ratios pi_theta / pi_0.
rng = np.random.default_rng(6)
sm = lambda z: np.exp(z - z.max()) / np.exp(z - z.max()).sum()
pi0 = sm(np.zeros(5))                     # data-generating policy: uniform
direction = np.array([2.0, 1.0, 0.0, -1.0, -2.0])
samples = rng.choice(5, 20000, p=pi0)     # fixed offline dataset
print("shift  KL(pi||pi0)  max ratio  ESS fraction  frac of data with ratio<0.2")
for shift in [0, 0.25, 0.5, 1.0, 1.5, 2.0]:
    pi = sm(shift*direction)
    ratio = pi[samples] / pi0[samples]
    ess = ratio.sum()**2 / (ratio**2).sum() / len(ratio)     # effective sample size fraction
    kl = (pi*np.log(pi/pi0)).sum()
    print(f"{shift:4.2f}   {kl:9.3f}  {ratio.max():9.2f}  {ess:12.3f}  {np.mean(ratio<0.2):.3f}")
