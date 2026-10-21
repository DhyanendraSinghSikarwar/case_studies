import numpy as np
from sklearn.model_selection import learning_curve
from sklearn.tree import DecisionTreeRegressor
from sklearn.linear_model import LinearRegression
rng=np.random.default_rng(0)
X=rng.uniform(-3,3,(600,1)); y=np.sin(2*X[:,0])+rng.normal(0,.3,600)
for name,m in [("linear (high bias)",LinearRegression()),("deep tree (high variance)",DecisionTreeRegressor(random_state=0))]:
    n,tr,va=learning_curve(m,X,y,train_sizes=[.1,.3,.6,1.0],cv=5,scoring="neg_mean_squared_error")
    print(name); print(" n   ",n); print(" train",np.round(-tr.mean(1),3)); print(" val  ",np.round(-va.mean(1),3))
