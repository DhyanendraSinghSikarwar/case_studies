import numpy as np, pandas as pd, warnings
warnings.filterwarnings("ignore")
from statsmodels.tsa.arima.model import ARIMA
from statsmodels.tsa.statespace.sarimax import SARIMAX
from statsmodels.tsa.holtwinters import ExponentialSmoothing
from statsmodels.stats.diagnostic import acorr_ljungbox
from sklearn.model_selection import TimeSeriesSplit
rng=np.random.default_rng(1)
# Q5 baselines + Q8 ARIMA on seasonal series
n=120; t=np.arange(n)
y=pd.Series(100+0.5*t+12*np.sin(2*np.pi*t/12)+rng.normal(0,3,n),pd.date_range("2015-01",periods=n,freq="MS"))
tr,te=y[:-12],y[-12:]
mae=lambda a,b: np.mean(np.abs(np.asarray(a)-np.asarray(b)))
naive=np.repeat(tr.iloc[-1],12); snaive=tr.iloc[-12:].values; ma=np.repeat(tr.iloc[-12:].mean(),12)
print("naive",mae(te,naive).round(2),"snaive",mae(te,snaive).round(2),"MA12",mae(te,ma).round(2))
# Q8
res={}
for o in [(1,1,0),(1,1,1),(2,1,2),(0,1,1)]:
    m=ARIMA(tr,order=o).fit(); res[o]=(m.aic,m.bic)
    print("ARIMA",o,"AIC",round(m.aic,1),"BIC",round(m.bic,1))
# Q20 SARIMA
sm=SARIMAX(tr,order=(0,1,1),seasonal_order=(0,1,1,12)).fit(disp=False)
print("SARIMA AIC",round(sm.aic,1),"MAE",mae(te,sm.forecast(12)).round(2))
# Q21 HW
hw=ExponentialSmoothing(tr,trend="add",seasonal="add",seasonal_periods=12).fit()
print("HW MAE",mae(te,hw.forecast(12)).round(2),"alpha",round(hw.params["smoothing_level"],2))
# Q25 residuals
r=sm.resid[13:]
print(acorr_ljungbox(r,lags=[12],model_df=2))
r2=ARIMA(tr,order=(1,0,0)).fit().resid
print("bad model LB p",acorr_ljungbox(r2,lags=[12])["lb_pvalue"].iloc[0])
# Q19
X=np.arange(20).reshape(-1,1)
for tr_i,te_i in TimeSeriesSplit(n_splits=3,test_size=3,gap=2).split(X):
    print("train",tr_i[0],"-",tr_i[-1],"test",te_i[0],"-",te_i[-1])
