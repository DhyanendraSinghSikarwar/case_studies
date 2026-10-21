from sklearn.datasets import make_classification
from sklearn.ensemble import RandomForestClassifier
from sklearn.model_selection import cross_val_score
X,y=make_classification(3000,20,n_informative=8,flip_y=0.1,random_state=0)
for kw in [dict(),dict(min_samples_leaf=5),dict(max_depth=4),dict(max_features=2),dict(max_features=0.8),dict(n_estimators=20)]:
    m=RandomForestClassifier(**{"n_estimators":200,"random_state":0,"n_jobs":-1,**kw})
    print(kw, cross_val_score(m,X,y,cv=5).mean().round(3))
