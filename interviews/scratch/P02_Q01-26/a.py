import numpy as np, pandas as pd, warnings
warnings.filterwarnings("ignore")
from sklearn.linear_model import LinearRegression, LogisticRegression, Lasso, Ridge, ElasticNet, LassoCV, RidgeCV, HuberRegressor, SGDRegressor
print("--- Q1")
rng=np.random.default_rng(0)
x=rng.normal(size=(200,1)); y=(x[:,0]+rng.normal(0,.5,200)>0).astype(int)
lin=LinearRegression().fit(x,y); p=lin.predict(np.array([[-3.],[3.]]))
print("linear preds at x=-3,3:",p.round(2))
print("logit preds:",LogisticRegression().fit(x,y).predict_proba(np.array([[-3.],[3.]]))[:,1].round(3))
print("--- Q3")
z=np.array([-4,-2,0,2,4.]); s=1/(1+np.exp(-z)); print(s.round(3), np.log(s/(1-s)).round(1))
print("--- Q5")
from sklearn.datasets import make_regression
X,y=make_regression(200,20,n_informative=4,noise=10,random_state=0)
Xs=(X-X.mean(0))/X.std(0)
for n,m in [("lasso",Lasso(alpha=5)),("ridge",Ridge(alpha=500))]:
    m.fit(Xs,y); print(n,"zeros:",int((np.abs(m.coef_)<1e-8).sum()),"of 20")
print("--- Q6")
from sklearn.metrics import r2_score
rng=np.random.default_rng(1)
Xn=rng.normal(size=(60,30)); yn=rng.normal(size=60)
tr,te=slice(0,30),slice(30,60)
m=LinearRegression().fit(Xn[tr],yn[tr])
r2=m.score(Xn[tr],yn[tr]); n,k=30,30
print("train R2",round(r2,3),"test R2",round(m.score(Xn[te],yn[te]),2))
# adj r2 with 10 noise features
m2=LinearRegression().fit(Xn[tr][:,:5],yn[tr]); r=m2.score(Xn[tr][:,:5],yn[tr]); print("5 noise feats R2",round(r,3),"adj",round(1-(1-r)*(29)/(30-5-1),3))
print("--- Q7")
import statsmodels.api as sm
rng=np.random.default_rng(2); n=5000
dist=rng.uniform(1,10,n); prime=rng.integers(0,2,n)
lg=-2+0.3*dist-0.8*prime; yy=rng.random(n)<1/(1+np.exp(-lg))
D=pd.DataFrame({"dist_km":dist,"prime":prime})
res=sm.Logit(yy.astype(int),sm.add_constant(D)).fit(disp=0)
print(res.params.round(2).to_dict(),"OR",np.exp(res.params).round(2).to_dict())
print("--- Q8")
from statsmodels.stats.outliers_influence import variance_inflation_factor as vif
rng=np.random.default_rng(3); a=rng.normal(size=500); b=a+rng.normal(0,.1,500); c=rng.normal(size=500)
yv=2*a+rng.normal(size=500)
Xv=pd.DataFrame({"a":a,"b":b,"c":c})
Xc=sm.add_constant(Xv)
print({col:round(vif(Xc.values,i),1) for i,col in enumerate(Xc.columns) if col!="const"})
r=sm.OLS(yv,Xc).fit(); print(r.params.round(2).to_dict(), r.bse.round(2).to_dict())
r2_=sm.OLS(yv,sm.add_constant(Xv[["a","c"]])).fit(); print("drop b se_a",r2_.bse["a"].round(2))
print("--- Q9")
rng=np.random.default_rng(0); X=rng.normal(size=(500,3)); w_true=np.array([1.5,-2,0.]); y=(rng.random(500)<1/(1+np.exp(-(X@w_true+.5)))).astype(float)
Xb=np.c_[np.ones(500),X]; w=np.zeros(4)
sig=lambda z:1/(1+np.exp(-z))
loss=lambda w:-np.mean(y*np.log(sig(Xb@w))+(1-y)*np.log(1-sig(Xb@w)))
for i in range(2000):
    g=Xb.T@(sig(Xb@w)-y)/500; w-=0.5*g
print("w",w.round(2),"loss",round(loss(w),4))
# gradient check
w0=rng.normal(size=4); g=Xb.T@(sig(Xb@w0)-y)/500
num=np.array([(loss(w0+1e-6*e)-loss(w0-1e-6*e))/2e-6 for e in np.eye(4)])
print("max grad err",np.abs(g-num).max()<1e-6)
print("sklearn",LogisticRegression(penalty=None).fit(X,y).coef_.round(2))
print("--- Q10")
df=pd.DataFrame({"city":["BLR","DEL","MUM","BLR"]})
print(pd.get_dummies(df,drop_first=True,dtype=int))
