import numpy as np
rng=np.random.default_rng(0)
n=200000; z=rng.integers(0,2,n)             # assignment
comp=rng.random(n)<0.3                        # would-be compliers (see feature if assigned)
d=z*comp                                      # actually exposed
y=rng.normal(10,3,n)+0.5*d                    # true effect of exposure 0.5
itt=y[z==1].mean()-y[z==0].mean()
comp_rate=d[z==1].mean()-d[z==0].mean()
print("ITT",round(itt,3),"compliance",round(comp_rate,3),"CACE",round(itt/comp_rate,3))
print("naive exposed-vs-not (per-protocol)", round(y[d==1].mean()-y[d==0].mean(),3))
