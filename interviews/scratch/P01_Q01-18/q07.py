import numpy as np
from sklearn.datasets import make_classification
from sklearn.feature_selection import SelectKBest,f_classif
from sklearn.linear_model import LogisticRegression
from sklearn.model_selection import cross_val_score,train_test_split
from sklearn.pipeline import make_pipeline
rng=np.random.default_rng(0)
X=rng.normal(size=(100,2000)); y=rng.integers(0,2,100)   # pure noise
Xl=SelectKBest(f_classif,k=20).fit_transform(X,y)         # leaky: select on all data
print("leaky  CV acc: %.2f"%cross_val_score(LogisticRegression(),Xl,y,cv=5).mean())
p=make_pipeline(SelectKBest(f_classif,k=20),LogisticRegression())
print("correct CV acc: %.2f"%cross_val_score(p,X,y,cv=5).mean())
# group leakage
from sklearn.model_selection import GroupKFold,KFold
from sklearn.ensemble import RandomForestClassifier
g=np.repeat(np.arange(100),10)                 # 100 users x 10 rows
u=rng.normal(size=(100,5)); Xg=np.repeat(u,10,0)+rng.normal(0,.1,(1000,5))
yg=np.repeat(rng.integers(0,2,100),10)          # label is per-user random
rf=RandomForestClassifier(100,random_state=0)
print("random KFold acc: %.2f"%cross_val_score(rf,Xg,yg,cv=KFold(5,shuffle=True,random_state=0)).mean())
print("GroupKFold acc:   %.2f"%cross_val_score(rf,Xg,yg,cv=GroupKFold(5),groups=g).mean())
