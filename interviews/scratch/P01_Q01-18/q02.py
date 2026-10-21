import numpy as np
from sklearn.datasets import make_classification
from sklearn.tree import DecisionTreeClassifier
from sklearn.model_selection import train_test_split
X,y=make_classification(1000,20,n_informative=5,flip_y=.1,random_state=0)
Xtr,Xva,ytr,yva=train_test_split(X,y,test_size=.3,random_state=0)
for d in [None,3]:
    m=DecisionTreeClassifier(max_depth=d,random_state=0).fit(Xtr,ytr)
    print(d,round(m.score(Xtr,ytr),3),round(m.score(Xva,yva),3))
