import numpy as np
from sklearn.datasets import make_classification
from sklearn.linear_model import LogisticRegression
from sklearn.metrics import f1_score, average_precision_score
from sklearn.model_selection import train_test_split
X,y=make_classification(6000,20,n_informative=5,weights=[0.97],flip_y=0.01,random_state=0)
Xtr,Xte,ytr,yte=train_test_split(X,y,stratify=y,random_state=0)
for cw in [None,"balanced"]:
    m=LogisticRegression(max_iter=2000,class_weight=cw).fit(Xtr,ytr)
    s=m.predict_proba(Xte)[:,1]
    print(cw,"F1",round(f1_score(yte,m.predict(Xte)),3),"PR-AUC",round(average_precision_score(yte,s),3))
# threshold tuning on probs
ths=np.linspace(0.05,0.95,19); best=max(ths,key=lambda t:f1_score(yte,s>=t)); print("best thr (balanced)",round(best,2))
