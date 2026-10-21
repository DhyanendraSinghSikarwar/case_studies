import numpy as np, pandas as pd
from scipy.special import inv_boxcox
from scipy.stats import boxcox
rng=np.random.default_rng(3)
# Q11 metrics
y=np.array([0,1,0,2,0,1,0,3.]); f=np.array([0.5,1,0.5,1.5,0.5,1,0.5,2])
print("MAE",np.abs(y-f).mean(),"WAPE",np.abs(y-f).sum()/y.sum())
yy=np.array([200,150,300,1.0]); ff=np.array([210,140,310,3.0])
print("MAPE",np.mean(np.abs(yy-ff)/yy).round(3),"WAPE",(np.abs(yy-ff).sum()/yy.sum()).round(3))
# MASE
tr=np.array([10,12,11,13,12,14,13,15.]); te=np.array([14,16.]); fc=np.array([15,15.])
scale=np.mean(np.abs(np.diff(tr))); print("MASE",(np.abs(te-fc).mean()/scale).round(2))
# Q24 back-transform bias
x=rng.normal(3,0.5,100000); yv=np.exp(x)
print("mean y",yv.mean().round(2),"exp(mean log)",np.exp(x.mean()).round(2),"exp(mu+s2/2)",np.exp(x.mean()+x.var()/2).round(2),"median y",np.median(yv).round(2))
b,lam=boxcox(yv[:1000]); print("lambda",round(lam,2)); print(np.allclose(inv_boxcox(b,lam),yv[:1000]))
# Q26 conformal-ish / bootstrap quick
resid=rng.normal(0,5,500); pt=100.0
print("bootstrap 80% interval",(pt+np.quantile(resid,[0.1,0.9])).round(1))
# Q17 white noise vs random walk
wn=rng.normal(size=1000); rw=np.cumsum(wn)
print("wn best forecast = mean; MAE mean",np.abs(wn[1:]-wn.mean()).mean().round(2)," rw naive MAE",np.abs(np.diff(rw)).mean().round(2),"rw mean-forecast MAE",np.abs(rw[1:]-rw.mean()).mean().round(2))
# Q14 pandas cleaning
s=pd.Series([1,2,np.nan,4,100,6],index=pd.to_datetime(["2024-01-01","2024-01-02","2024-01-03","2024-01-05","2024-01-06","2024-01-07"]))
s=s.asfreq("D"); print(s.isna().sum()); 
med=s.rolling(5,center=True,min_periods=1).median(); mad=(s-med).abs().rolling(5,center=True,min_periods=1).median()
out=(s-med).abs()>5*mad.clip(lower=0.5); print(out.sum()); print(s.mask(out).interpolate().round(1).tolist())
