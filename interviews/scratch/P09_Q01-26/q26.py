import numpy as np
rng=np.random.default_rng(0)
x=rng.normal(5,3,size=(8,4,6,6))  # N,C,H,W
g,b,eps=np.ones((1,4,1,1)),np.zeros((1,4,1,1)),1e-5
mu=x.mean((0,2,3),keepdims=True); var=x.var((0,2,3),keepdims=True)
y=g*(x-mu)/np.sqrt(var+eps)+b
print(np.round(y.mean((0,2,3)),3), np.round(y.std((0,2,3)),3))
# inverted dropout
p=0.5; a=rng.normal(size=(1000,)); m=(rng.random(a.shape)>p)/(1-p); print(round(a.mean(),3),round((a*m).mean(),3), round(abs(((a**2)).mean()),2))
