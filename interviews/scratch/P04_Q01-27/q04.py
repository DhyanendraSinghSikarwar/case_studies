import numpy as np
from sklearn.datasets import make_classification
from sklearn.tree import DecisionTreeClassifier
from sklearn.ensemble import RandomForestClassifier
from sklearn.model_selection import cross_val_score
X,y=make_classification(2000,20,n_informative=8,flip_y=0.1,random_state=0)
for n,m in [("tree",DecisionTreeClassifier(random_state=0)),
  ("RF",RandomForestClassifier(300,random_state=0,n_jobs=-1))]:
    print(n, cross_val_score(m,X,y,cv=5).mean().round(3))
print("unique frac in bootstrap:", len(np.unique(np.random.default_rng(0).integers(0,10000,10000)))/10000)
