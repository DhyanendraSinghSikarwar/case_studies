import numpy as np
from sklearn.neighbors import NearestNeighbors
# Q9 SMOTE from scratch
def smote(X_min, n_new, k=5, seed=0):
    rng = np.random.default_rng(seed)
    nn = NearestNeighbors(n_neighbors=k+1).fit(X_min)
    idx = nn.kneighbors(X_min, return_distance=False)[:, 1:]   # drop self
    base = rng.integers(0, len(X_min), n_new)
    nbr = idx[base, rng.integers(0, k, n_new)]
    lam = rng.random((n_new, 1))
    return X_min[base] + lam * (X_min[nbr] - X_min[base])
rng=np.random.default_rng(1); Xm=rng.normal(size=(30,2))
new=smote(Xm,100)
print("Q9",new.shape, "within min/max box:", bool((new.min(0)>=Xm.min(0)).all() and (new.max(0)<=Xm.max(0)).all()))
# Q19
def prf(y,p):
    tp=((p==1)&(y==1)).sum(); fp=((p==1)&(y==0)).sum(); fn=((p==0)&(y==1)).sum()
    pr=tp/(tp+fp) if tp+fp else 0.0; rc=tp/(tp+fn) if tp+fn else 0.0
    return pr, rc, (2*pr*rc/(pr+rc) if pr+rc else 0.0)
def pr_curve(y,s):
    o=np.argsort(-s,kind="stable"); y=y[o]; s=s[o]
    tp=np.cumsum(y); fp=np.cumsum(1-y)
    last=np.r_[np.diff(s)!=0,True]          # one point per distinct threshold (ties)
    tp,fp,th=tp[last],fp[last],s[last]
    return tp/(tp+fp), tp/y.sum(), th
def ap(y,s):
    p,r,_=pr_curve(y,s); return np.sum(np.diff(np.r_[0,r])*p)
from sklearn.metrics import precision_recall_curve, average_precision_score, precision_recall_fscore_support
rng=np.random.default_rng(0); y=(rng.random(5000)<0.05).astype(int); s=np.round(rng.normal(size=5000)+1.5*y,1)
print("Q19 AP mine",round(ap(y,s),6),"sk",round(average_precision_score(y,s),6))
print("Q19 prf mine",np.round(prf(y,(s>1).astype(int)),4),"sk",np.round(precision_recall_fscore_support(y,(s>1).astype(int),average="binary")[:3],4))
# Q13 log loss
def logloss(y,p,eps=1e-15):
    p=np.clip(p,eps,1-eps); return -np.mean(y*np.log(p)+(1-y)*np.log(1-p))
from sklearn.metrics import log_loss
y=np.array([1,0,1,1,0]); p=np.array([.9,.2,.6,.99,.5]); print("Q13",round(logloss(y,p),4),round(log_loss(y,p),4))
print("Q13 confident wrong",round(-np.log(0.01),3),"vs hedged",round(-np.log(0.4),3))
# Q18 F-beta
P,R=0.5,0.9
for b in [0.5,1,2]: print("Q18 beta",b,round((1+b*b)*P*R/(b*b*P+R),3))
