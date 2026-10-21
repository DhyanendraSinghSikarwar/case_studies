import numpy as np
from sklearn.tree import DecisionTreeRegressor
rng=np.random.default_rng(0)
X=rng.uniform(0,6,(300,1)); y=np.sin(X[:,0])+rng.normal(0,0.2,300)
lr=0.1; F=np.full_like(y,y.mean()); trees=[]
for m in range(100):
    resid=y-F                         # negative gradient of 0.5*(y-F)^2
    t=DecisionTreeRegressor(max_depth=2).fit(X,resid)
    F+=lr*t.predict(X); trees.append(t)
    if m in (0,9,99): print(m+1,"trees, train MSE",round(np.mean((y-F)**2),4))
