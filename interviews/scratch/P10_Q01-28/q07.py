import numpy as np
from scipy.stats import norm
rng=np.random.default_rng(0)
sims,days,n=2000,14,500   # users per arm per day, NO true effect
fp=0
for _ in range(sims):
    a=rng.binomial(1,0.1,(days,n)).cumsum().reshape(-1) if False else None
    ca=rng.binomial(n,0.1,days).cumsum(); cb=rng.binomial(n,0.1,days).cumsum()
    N=n*np.arange(1,days+1)
    pa,pb=ca/N,cb/N; pp=(ca+cb)/(2*N)
    z=(pb-pa)/np.sqrt(2*pp*(1-pp)/N)
    if (np.abs(z)>1.96).any(): fp+=1
print("false positive rate with daily peeking:", fp/sims)
