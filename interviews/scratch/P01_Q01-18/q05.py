import numpy as np
from sklearn.datasets import make_classification
from sklearn.linear_model import LogisticRegression
from sklearn.model_selection import StratifiedKFold, cross_val_score
X,y=make_classification(500,10,weights=[.9],random_state=0)
cv=StratifiedKFold(5,shuffle=True,random_state=0)
s=cross_val_score(LogisticRegression(max_iter=1000),X,y,cv=cv,scoring="roc_auc")
print(np.round(s,3), round(s.mean(),3), round(s.std(),3))
