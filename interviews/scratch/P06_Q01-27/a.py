import numpy as np, pandas as pd, warnings
warnings.filterwarnings("ignore")
from statsmodels.tsa.stattools import adfuller, kpss, acf, pacf
from statsmodels.tsa.arima_process import ArmaProcess
from statsmodels.tsa.seasonal import seasonal_decompose
rng=np.random.default_rng(0)
# Q1
n=300
rw=np.cumsum(rng.normal(size=n))
def tests(x,name):
    a=adfuller(x)[1]; k=kpss(x,regression="c",nlags="auto")[1]
    print(f"{name}: ADF p={a:.3f}  KPSS p={k:.3f}")
tests(rw,"random walk"); tests(np.diff(rw),"differenced")
# Q2
idx=pd.date_range("2020-01",periods=72,freq="MS")
t=np.arange(72)
add=pd.Series(100+2*t+10*np.sin(2*np.pi*t/12)+rng.normal(0,2,72),idx)
mul=pd.Series((100+2*t)*(1+0.2*np.sin(2*np.pi*t/12))+rng.normal(0,2,72),idx)
for nm,s,m in [("add",add,"additive"),("mul",mul,"multiplicative")]:
    d=seasonal_decompose(s,model=m,period=12)
    print(nm,m,"seasonal range",d.seasonal.min().round(2),d.seasonal.max().round(2),"resid sd",d.resid.std().round(2))
# Q6 over-diff
x=ArmaProcess([1,-0.6],[1]).generate_sample(500,distrvs=rng.normal) 
d1=np.diff(x); d2=np.diff(x,2)
print("var x,d1,d2",x.var().round(2),d1.var().round(2),d2.var().round(2))
print("acf1 of d2",acf(d2,nlags=1)[1].round(2))
rw2=np.cumsum(rng.normal(size=500))
print("rw var d0,d1,d2",rw2.var().round(1),np.diff(rw2).var().round(2),np.diff(rw2,2).var().round(2),"acf1 of d2",acf(np.diff(rw2,2),nlags=1)[1].round(2))
# Q7
ar=ArmaProcess([1,-0.7],[1]).generate_sample(2000,distrvs=rng.normal)
ma=ArmaProcess([1],[1,0.7]).generate_sample(2000,distrvs=rng.normal)
print("AR1 acf",acf(ar,nlags=4)[1:].round(2),"pacf",pacf(ar,nlags=4)[1:].round(2))
print("MA1 acf",acf(ma,nlags=4)[1:].round(2),"pacf",pacf(ma,nlags=4)[1:].round(2))
