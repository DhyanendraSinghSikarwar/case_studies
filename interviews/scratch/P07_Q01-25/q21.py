import numpy as np
rng = np.random.default_rng(0)
p = np.array([0.04, 0.05, 0.06, 0.10]); T = 5000
def run(policy):
    a = np.ones(4); b = np.ones(4); n = np.zeros(4); s = np.zeros(4); reg = 0
    for t in range(T):
        if policy == "eps": arm = rng.integers(4) if rng.random() < .1 else np.argmax(s/np.maximum(n,1))
        elif policy == "ucb": arm = t if t < 4 else np.argmax(s/n + np.sqrt(2*np.log(t+1)/n))
        else: arm = np.argmax(rng.beta(a, b))
        r = rng.random() < p[arm]; n[arm]+=1; s[arm]+=r; a[arm]+=r; b[arm]+=1-r
        reg += p.max() - p[arm]
    return reg
for pol in ("eps","ucb","ts"):
    print(pol, round(np.mean([run(pol) for _ in range(10)]), 1))
