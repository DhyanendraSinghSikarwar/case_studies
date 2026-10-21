import numpy as np
from sklearn.datasets import make_classification
from sklearn.linear_model import LogisticRegression
from sklearn.metrics import f1_score, recall_score, precision_score
from sklearn.model_selection import train_test_split
X,y=make_classification(8000,20,n_informative=8,weights=[0.97],class_sep=1.0,flip_y=0,random_state=0)
Xtr,Xte,ytr,yte=train_test_split(X,y,stratify=y,random_state=0)
def rep(name,pred): print(name,"P",round(precision_score(yte,pred),2),"R",round(recall_score(yte,pred),2),"F1",round(f1_score(yte,pred),2))
m=LogisticRegression(max_iter=2000).fit(Xtr,ytr); rep("plain       ",m.predict(Xte))
mb=LogisticRegression(max_iter=2000,class_weight="balanced").fit(Xtr,ytr); rep("balanced   ",mb.predict(Xte))
s=m.predict_proba(Xtr)[:,1]; ths=np.linspace(0.02,0.9,45)
t=max(ths,key=lambda t:f1_score(ytr,s>=t))      # pick threshold on TRAIN side here for brevity; use a validation split in practice
rep(f"thr={t:.2f}  ",m.predict_proba(Xte)[:,1]>=t)
