import numpy as np, warnings
warnings.filterwarnings("ignore")
from sklearn.linear_model import Ridge, LinearRegression, Lasso
rng=np.random.default_rng(0); n=500
inc=rng.normal(50000,15000,n); age=rng.normal(35,8,n); yy=0.00005*inc+0.5*age+rng.normal(0,1,n)
Xr=np.c_[inc,age]
for a in [1e3]:
    print("raw",Ridge(alpha=a).fit(Xr,yy).coef_.round(5), "ols",LinearRegression().fit(Xr,yy).coef_.round(5))
Xs=(Xr-Xr.mean(0))/Xr.std(0)
print("std",Ridge(alpha=1e3).fit(Xs,yy).coef_.round(3),"ols",LinearRegression().fit(Xs,yy).coef_.round(3))
print("--- Q4")
from sklearn.model_selection import train_test_split
rng=np.random.default_rng(0)
X=rng.normal(size=(60,40)); w=np.r_[2,-1,1.5,np.zeros(37)]; y=X@w+rng.normal(0,2,60)
Xtr,Xte,ytr,yte=train_test_split(X,y,test_size=.5,random_state=0)
from sklearn.metrics import mean_squared_error as mse
for a in [1e-4,1,10,100,1000]:
    m=Ridge(alpha=a).fit(Xtr,ytr); print(a,round(mse(ytr,m.predict(Xtr)),2),round(mse(yte,m.predict(Xte)),2))
print("--- Q2 hetero")
import statsmodels.api as sm
from statsmodels.stats.diagnostic import het_breuschpagan
x=rng.uniform(1,10,500); y=2*x+rng.normal(0,x*0.5)
Xc=sm.add_constant(x); r=sm.OLS(y,Xc).fit()
print("BP p",round(het_breuschpagan(r.resid,Xc)[1],4),"se classic",r.bse.round(3),"HC3",sm.OLS(y,Xc).fit(cov_type="HC3").bse.round(3))
print("--- Q22 coefs")
from sklearn.linear_model import LogisticRegression
from sklearn.datasets import make_classification
Xc,yc=make_classification(500,10,random_state=0)
for C in [0.001,0.1,10,1000]: print(C,np.abs(LogisticRegression(C=C).fit(Xc,yc).coef_).sum().round(2), np.abs(LogisticRegression(C=C,penalty='l1',solver='liblinear').fit(Xc,yc).coef_).sum().round(2))
