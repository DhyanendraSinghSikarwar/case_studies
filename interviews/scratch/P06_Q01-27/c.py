import numpy as np, pandas as pd, lightgbm as lgb, warnings
warnings.filterwarnings("ignore")
rng=np.random.default_rng(2)
# Q10 features w/o leakage, Q15 direct vs recursive, Q23 calendar, Q26 quantile, Q27 global
dates=pd.date_range("2022-01-01",periods=400)
rows=[]
for s in range(20):
    base=rng.uniform(20,100); amp=rng.uniform(0.1,0.4)
    v=base*(1+amp*np.sin(2*np.pi*np.arange(400)/7))*(1+0.001*np.arange(400))+rng.normal(0,base*0.08,400)
    rows.append(pd.DataFrame({"series":s,"date":dates,"y":v}))
df=pd.concat(rows).sort_values(["series","date"]).reset_index(drop=True)
g=df.groupby("series")["y"]
for l in (1,7,14): df[f"lag{l}"]=g.shift(l)
df["roll7"]=g.transform(lambda x:x.shift(1).rolling(7).mean())   # shift(1) BEFORE rolling
df["dow"]=df.date.dt.dayofweek
df["sin7"]=np.sin(2*np.pi*df.dow/7); df["cos7"]=np.cos(2*np.pi*df.dow/7)
df["series"]=df["series"].astype("category")
feats=["series","lag1","lag7","lag14","roll7","dow"]
d=df.dropna(); cut=pd.Timestamp("2023-02-01")
tr=d[d.date<cut]; te=d[d.date>=cut]
m=lgb.LGBMRegressor(n_estimators=300,learning_rate=0.05,verbose=-1,random_state=0).fit(tr[feats],tr.y)
p=m.predict(te[feats])
print("global LGBM WAPE",(np.abs(te.y-p).sum()/te.y.sum()).round(3))
print("seasonal naive WAPE",(np.abs(te.y-te.lag7).sum()/te.y.sum()).round(3))
# leaky version
d2=df.copy(); d2["roll7_leak"]=d2.groupby("series")["y"].transform(lambda x:x.rolling(7).mean()); d2=d2.dropna()
tr2=d2[d2.date<cut]; te2=d2[d2.date>=cut]; f2=["series","lag1","lag7","roll7_leak"]
m2=lgb.LGBMRegressor(n_estimators=300,learning_rate=0.05,verbose=-1,random_state=0).fit(tr2[f2],tr2.y)
print("leaky roll WAPE",(np.abs(te2.y-m2.predict(te2[f2])).sum()/te2.y.sum()).round(3))
# Q26 quantile
q={a:lgb.LGBMRegressor(objective="quantile",alpha=a,n_estimators=200,learning_rate=0.05,verbose=-1,random_state=0).fit(tr[feats],tr.y) for a in (0.1,0.9)}
lo,hi=q[0.1].predict(te[feats]),q[0.9].predict(te[feats])
print("80% interval coverage",np.mean((te.y>=lo)&(te.y<=hi)).round(3))
# Q15 direct vs recursive for one series, h=7
s0=df[df.series==0].reset_index(drop=True)["y"].values
H=7
def mk(y,lags=(1,2,3,7)):
    mx=max(lags); X=np.array([[y[i-l] for l in lags] for i in range(mx,len(y))]); return X,y[mx:]
train=s0[:350]; test=s0[350:350+H]
X,Y=mk(train)
mr=lgb.LGBMRegressor(n_estimators=200,verbose=-1,random_state=0).fit(X,Y)
hist=list(train); rec=[]
for h in range(H):
    x=np.array([[hist[-l] for l in (1,2,3,7)]]); yhat=mr.predict(x)[0]; rec.append(yhat); hist.append(yhat)
direct=[]
for h in range(1,H+1):
    lags=[l for l in (7,8,9,14)]  # all >= h
    Xh=np.array([[train[i-l] for l in lags] for i in range(14,len(train)-h+1)]); Yh=np.array([train[i+h-1] for i in range(14,len(train)-h+1)])
    # features at origin t=i-1: lags relative to origin
    Xh=np.array([[train[o-l+1] for l in (1,2,3,7)] for o in range(13,len(train)-h)]); Yh=np.array([train[o+h] for o in range(13,len(train)-h)])
    mh=lgb.LGBMRegressor(n_estimators=200,verbose=-1,random_state=0).fit(Xh,Yh)
    o=len(train)-1; direct.append(mh.predict(np.array([[train[o-l+1] for l in (1,2,3,7)]]))[0])
print("recursive MAE",np.abs(test-rec).mean().round(2),"direct MAE",np.abs(test-direct).mean().round(2))
