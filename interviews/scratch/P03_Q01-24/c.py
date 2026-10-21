import numpy as np
from sklearn.datasets import make_classification
from sklearn.model_selection import train_test_split, StratifiedKFold, cross_val_score
from sklearn.linear_model import LogisticRegression
from sklearn.ensemble import RandomForestClassifier
from sklearn.metrics import average_precision_score, f1_score, precision_recall_curve
from imblearn.over_sampling import SMOTE
from imblearn.pipeline import Pipeline
X,y=make_classification(n_samples=20000,n_features=20,n_informative=6,weights=[0.98],flip_y=0.02,class_sep=0.8,random_state=0)
Xtr,Xte,ytr,yte=train_test_split(X,y,stratify=y,test_size=0.3,random_state=0)
print("pos rate",y.mean().round(4))
def ap(m): m.fit(Xtr,ytr); return average_precision_score(yte,m.predict_proba(Xte)[:,1])
print("Q8 plain LR AP",round(ap(LogisticRegression(max_iter=1000)),3))
print("Q8 balanced LR AP",round(ap(LogisticRegression(max_iter=1000,class_weight="balanced")),3))
print("Q11 SMOTE pipe AP",round(ap(Pipeline([("s",SMOTE(random_state=0)),("m",LogisticRegression(max_iter=1000))])),3))
# Q10 leak: SMOTE before CV vs inside pipeline
cv=StratifiedKFold(5,shuffle=True,random_state=0)
rf=RandomForestClassifier(100,random_state=0,n_jobs=-1)
Xs,ys=SMOTE(random_state=0).fit_resample(X,y)
leak=cross_val_score(rf,Xs,ys,cv=cv,scoring="average_precision").mean()
ok=cross_val_score(Pipeline([("s",SMOTE(random_state=0)),("m",rf)]),X,y,cv=cv,scoring="average_precision").mean()
print("Q10 leaky AP",round(leak,3),"correct AP",round(ok,3))
# Q12 threshold
m=LogisticRegression(max_iter=1000,class_weight="balanced").fit(Xtr,ytr)
Xv_tr,Xv,yv_tr,yv=train_test_split(Xte,yte,stratify=yte,test_size=0.5,random_state=1)
pv=m.predict_proba(Xv)[:,1]; p,r,t=precision_recall_curve(yv,pv)
f=2*p*r/(p+r+1e-12); i=f[:-1].argmax(); print("Q12 best t",round(t[i],3),"F1",round(f[i],3),"F1@0.5",round(f1_score(yv,pv>0.5),3))
pt=m.predict_proba(Xv_tr)[:,1]; print("Q12 held-out F1 at chosen t",round(f1_score(yv_tr,pt>t[i]),3),"at .5",round(f1_score(yv_tr,pt>0.5),3))
