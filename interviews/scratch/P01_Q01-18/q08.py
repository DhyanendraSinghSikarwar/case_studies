import numpy as np
from sklearn.pipeline import make_pipeline
from sklearn.impute import SimpleImputer
from sklearn.preprocessing import StandardScaler
from sklearn.linear_model import LogisticRegression
from sklearn.model_selection import train_test_split
from sklearn.datasets import make_classification
X,y=make_classification(500,5,random_state=0)
X[np.random.default_rng(0).random(X.shape)<.1]=np.nan
Xtr,Xte,ytr,yte=train_test_split(X,y,test_size=.2,random_state=0,stratify=y)
pipe=make_pipeline(SimpleImputer(strategy="median"),StandardScaler(),LogisticRegression())
pipe.fit(Xtr,ytr); print(round(pipe.score(Xte,yte),3))
# scale sensitivity of KNN
from sklearn.neighbors import KNeighborsClassifier
from sklearn.tree import DecisionTreeClassifier
Xc=np.nan_to_num(X); Xs=Xc.copy(); Xs[:,0]*=1000
for nm,m in [("knn",KNeighborsClassifier()),("tree",DecisionTreeClassifier(random_state=0))]:
    for lab,A in [("orig",Xc),("col0 x1000",Xs)]:
        a,b,c,d=train_test_split(A,y,test_size=.2,random_state=0)
        print(nm,lab,round(m.fit(a,c).score(b,d),3))
