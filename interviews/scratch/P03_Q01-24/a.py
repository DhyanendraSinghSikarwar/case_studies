import numpy as np
# Q1
y = np.array([1]*10 + [0]*990); pred = np.zeros(1000, int)
print("Q1 acc", (y==pred).mean(), "recall", ((pred==1)&(y==1)).sum()/y.sum())
# Q2
TP,FP,FN,TN = 80,40,20,860
p=TP/(TP+FP); r=TP/(TP+FN); s=TN/(TN+FP); f=2*p*r/(p+r)
print("Q2", p, r, s, f, (TP+TN)/(TP+FP+FN+TN))
# Q4
from sklearn.model_selection import KFold, StratifiedKFold
rng=np.random.default_rng(0); y=(rng.random(1000)<0.02).astype(int); X=np.zeros((1000,1))
for nm,cv in [("KFold",KFold(5,shuffle=True,random_state=0)),("Strat",StratifiedKFold(5,shuffle=True,random_state=0))]:
    print("Q4",nm,[int(y[te].sum()) for _,te in cv.split(X,y)], y.sum())
# Q5
from sklearn.metrics import roc_auc_score
rng=np.random.default_rng(0); yt=(rng.random(2000)<0.1).astype(int); s=rng.normal(size=2000)+1.2*yt
pos,neg=s[yt==1],s[yt==0]
pw=((pos[:,None]>neg[None,:]).mean()+0.5*(pos[:,None]==neg[None,:]).mean())
print("Q5",pw,roc_auc_score(yt,s),roc_auc_score(yt,-s),roc_auc_score(yt,rng.random(2000)))
