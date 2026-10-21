import numpy as np, pandas as pd, warnings
warnings.filterwarnings("ignore")
from sklearn.linear_model import *
print("--- Q11/Q23")
from sklearn.datasets import make_regression
X,y=make_regression(300,30,n_informative=5,noise=20,random_state=0)
lc=LassoCV(cv=5,random_state=0).fit(X,y)
mean=lc.mse_path_.mean(1); se=lc.mse_path_.std(1)/np.sqrt(5)
i=mean.argmin(); thr=mean[i]+se[i]
alpha_1se=lc.alphas_[np.where(mean<=thr)[0].min()]  # alphas descending => first = largest
print("alpha_min",round(lc.alpha_,3),"alpha_1se",round(alpha_1se,3))
print("nonzero min",int((lc.coef_!=0).sum()),"1se",int((Lasso(alpha=alpha_1se).fit(X,y).coef_!=0).sum()))
rc=RidgeCV(alphas=np.logspace(-2,3,20)).fit(X,y); print("ridge alpha",round(rc.alpha_,2))
print("--- Q13")
from sklearn.feature_selection import SelectKBest,f_regression,RFE
print("filter",np.where(SelectKBest(f_regression,k=5).fit(X,y).get_support())[0])
print("wrapper",np.where(RFE(LinearRegression(),n_features_to_select=5).fit(X,y).support_)[0])
print("embedded",np.where(LassoCV(cv=5,random_state=0).fit(X,y).coef_!=0)[0][:10])
print("--- Q14")
rng=np.random.default_rng(0); n=1000
Xr=rng.normal(size=(n,3)); yr=Xr@[2,-1,.5]+3+rng.normal(0,.5,n)
Xb=np.c_[np.ones(n),Xr]
w_ne=np.linalg.solve(Xb.T@Xb,Xb.T@yr)
w=np.zeros(4)
for _ in range(500): w-=0.1*(2/n)*Xb.T@(Xb@w-yr)
print("normal eq",w_ne.round(3),"GD",w.round(3))
print("--- Q15")
yt=np.array([10,12,11,13,12.]); yp=np.array([11,11,12,12,12.]); yo=yt.copy(); yo[0]=100
for nm,t in [("clean",yt),("outlier",yo)]:
    e=t-yp; print(nm,"MAE",np.abs(e).mean().round(1),"RMSE",np.sqrt((e**2).mean()).round(1))
print("--- Q16")
rng=np.random.default_rng(0); z=rng.normal(size=400)
Xc=np.c_[z+rng.normal(0,.05,400),z+rng.normal(0,.05,400),z+rng.normal(0,.05,400),rng.normal(size=(400,3))]
yc=3*z+rng.normal(size=400)
print("lasso",Lasso(alpha=.1).fit(Xc,yc).coef_.round(2))
print("enet ",ElasticNet(alpha=.1,l1_ratio=.5).fit(Xc,yc).coef_.round(2))
print("--- Q17")
rng=np.random.default_rng(0); city=rng.integers(0,3,100); D=np.eye(3)[city]
full=np.c_[np.ones(100),D]; print("rank with all 3 dummies + intercept:",np.linalg.matrix_rank(full),"of",full.shape[1])
red=np.c_[np.ones(100),D[:,1:]]; print("drop first:",np.linalg.matrix_rank(red),"of",red.shape[1])
print("--- Q18")
rng=np.random.default_rng(0); n=500
inc=rng.normal(50000,15000,n); age=rng.normal(35,8,n); yy=0.0002*inc+0.5*age+rng.normal(0,1,n)
Xr=np.c_[inc,age]
print("ridge raw",Ridge(alpha=10).fit(Xr,yy).coef_.round(5))
Xs=(Xr-Xr.mean(0))/Xr.std(0)
print("ridge std",Ridge(alpha=10).fit(Xs,yy).coef_.round(2),"OLS std",LinearRegression().fit(Xs,yy).coef_.round(2))
print("--- Q19")
from sklearn.preprocessing import MinMaxScaler,StandardScaler,RobustScaler
v=np.array([[10],[12],[11],[13],[12],[1000.]])
for s in [MinMaxScaler(),StandardScaler(),RobustScaler()]: print(type(s).__name__,s.fit_transform(v).ravel().round(2))
print("--- Q20")
rng=np.random.default_rng(0); a=rng.normal(size=300); b=rng.normal(size=300); c=a+b
y2=a+2*b+rng.normal(0,.1,300)
X3=np.c_[a,b,c]
print("rank",np.linalg.matrix_rank(X3))
print("ols",LinearRegression().fit(X3,y2).coef_.round(2))
print("ridge",Ridge(alpha=1).fit(X3,y2).coef_.round(2))
print("lasso",Lasso(alpha=.01).fit(X3,y2).coef_.round(2))
c2=c+rng.normal(0,.01,300); X4=np.c_[a,b,c2]; print("cond",np.linalg.cond(X4.T@X4).round(-3))
print("--- Q21")
Xs=rng.normal(size=(50,4)); Xs=np.c_[Xs,Xs[:,0]]; ys=Xs[:,0]*2+rng.normal(size=50)
lam=1.0
w=np.linalg.solve(Xs.T@Xs+lam*np.eye(5),Xs.T@ys)
print(w.round(3), Ridge(alpha=lam,fit_intercept=False).fit(Xs,ys).coef_.round(3))
print("--- Q22")
from sklearn.datasets import make_classification
Xc,yc=make_classification(500,10,random_state=0)
for C in [0.001,0.1,10,1000]:
    print(C,np.abs(LogisticRegression(C=C).fit(Xc,yc).coef_).sum().round(2))
print("--- Q24")
from sklearn.preprocessing import SplineTransformer,PolynomialFeatures
from sklearn.pipeline import make_pipeline
from sklearn.model_selection import cross_val_score
rng=np.random.default_rng(0); x=rng.uniform(-3,3,(1000,1)); yb=(rng.random(1000)<1/(1+np.exp(-(x[:,0]**2-2)))).astype(int)
for nm,m in [("linear",LogisticRegression()),("poly2",make_pipeline(PolynomialFeatures(2),LogisticRegression())),("spline",make_pipeline(SplineTransformer(n_knots=6),LogisticRegression()))]:
    print(nm,cross_val_score(m,x,yb,cv=5,scoring="roc_auc").mean().round(3))
print("--- Q25")
rng=np.random.default_rng(0); x=rng.uniform(0,10,(100,1)); y=2*x[:,0]+1+rng.normal(0,1,100); y[:5]+=60
print("ols slope",LinearRegression().fit(x,y).coef_.round(2),"huber",HuberRegressor().fit(x,y).coef_.round(2))
q=QuantileRegressor(quantile=.5,alpha=0,solver="highs").fit(x,y); print("median reg",q.coef_.round(2))
print("--- Q26")
rng=np.random.default_rng(0); x=rng.uniform(0,10,(5000,1)); ytrue=np.exp(1+0.2*x[:,0]+rng.normal(0,.8,5000))
m=LinearRegression().fit(x,np.log(ytrue)); res=np.log(ytrue)-m.predict(x)
naive=np.exp(m.predict(x)); smear=naive*np.mean(np.exp(res))
print("mean actual",ytrue.mean().round(2),"naive",naive.mean().round(2),"smeared",smear.mean().round(2))
