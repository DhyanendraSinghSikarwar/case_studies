import numpy as np
from sklearn.datasets import make_classification
from sklearn.model_selection import train_test_split
from sklearn.ensemble import RandomForestClassifier, GradientBoostingClassifier
from sklearn.linear_model import LogisticRegression
from sklearn.svm import LinearSVC
from sklearn.naive_bayes import GaussianNB
from sklearn.calibration import calibration_curve, CalibratedClassifierCV
from sklearn.metrics import roc_auc_score, brier_score_loss, log_loss
def ece(y,p,bins=10):
    b=np.minimum((p*bins).astype(int),bins-1); e=0
    for k in range(bins):
        m=b==k
        if m.any(): e+=m.mean()*abs(y[m].mean()-p[m].mean())
    return e
X,y=make_classification(n_samples=30000,n_features=20,n_informative=8,weights=[0.9],flip_y=0.03,random_state=0)
Xtr,Xte,ytr,yte=train_test_split(X,y,test_size=0.4,stratify=y,random_state=0)
Xte,Xcal,yte,ycal=train_test_split(Xte,yte,test_size=0.5,stratify=yte,random_state=0)
models={"logreg":LogisticRegression(max_iter=1000),"rf":RandomForestClassifier(200,random_state=0,n_jobs=-1),"nb":GaussianNB()}
for n,m in models.items():
    m.fit(Xtr,ytr); p=m.predict_proba(Xte)[:,1]
    print("Q21/22",n,"AUC",round(roc_auc_score(yte,p),3),"Brier",round(brier_score_loss(yte,p),4),"ECE",round(ece(yte,p),4))
# Q20 Platt vs isotonic on RF using held-out cal set
rf=models["rf"]
from sklearn.isotonic import IsotonicRegression
praw_cal=rf.predict_proba(Xcal)[:,1]; praw=rf.predict_proba(Xte)[:,1]
iso=IsotonicRegression(out_of_bounds="clip").fit(praw_cal,ycal)
eps=1e-6; lg=lambda p: np.log(np.clip(p,eps,1-eps)/(1-np.clip(p,eps,1-eps)))
platt=LogisticRegression().fit(lg(praw_cal).reshape(-1,1),ycal)
pp=platt.predict_proba(lg(praw).reshape(-1,1))[:,1]; pi=iso.predict(praw)
for n,p in [("raw",praw),("platt",pp),("isotonic",pi)]:
    print("Q20",n,"Brier",round(brier_score_loss(yte,p),4),"ECE",round(ece(yte,p),4),"AUC",round(roc_auc_score(yte,p),4))
# Q23 prior correction
Xb,yb=Xtr,ytr
lr=LogisticRegression(max_iter=1000,class_weight="balanced").fit(Xb,yb)
pb=lr.predict_proba(Xte)[:,1]
pi_true=ytr.mean(); w=pi_true/(1-pi_true)  # balanced => model thinks prior .5
pc=w*pb/(w*pb+(1-pb)) if False else None
# correction: odds_true = odds_bal * (pi/(1-pi)) / (0.5/0.5)
odds=pb/(1-pb)*w; pc=odds/(1+odds)
print("Q23 true rate",round(yte.mean(),3),"mean balanced",round(pb.mean(),3),"mean corrected",round(pc.mean(),3),"ECE bal",round(ece(yte,pb),3),"ECE corr",round(ece(yte,pc),3))
# Q24 cost threshold
cfp,cfn=1,20; t=cfp/(cfp+cfn); p=LogisticRegression(max_iter=1000).fit(Xtr,ytr).predict_proba(Xte)[:,1]
def cost(th): pr=p>th; return ((pr&(yte==0)).sum()*cfp+((~pr)&(yte==1)).sum()*cfn)
grid=np.linspace(0.02,0.9,89); best=grid[np.argmin([cost(g) for g in grid])]
print("Q24 theory t",round(t,3),"grid best",round(best,2),"cost@.5",cost(.5),"cost@theory",cost(t),"cost@best",cost(best))
