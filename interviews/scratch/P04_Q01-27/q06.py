from sklearn.datasets import make_classification
from sklearn.tree import DecisionTreeClassifier
from sklearn.model_selection import train_test_split
X,y=make_classification(2000,20,n_informative=6,flip_y=0.15,random_state=0)
Xtr,Xte,ytr,yte=train_test_split(X,y,test_size=0.3,random_state=0)
full=DecisionTreeClassifier(random_state=0).fit(Xtr,ytr)
print("full: leaves",full.get_n_leaves(),"train",round(full.score(Xtr,ytr),3),"test",round(full.score(Xte,yte),3))
path=full.cost_complexity_pruning_path(Xtr,ytr)
best=max(((DecisionTreeClassifier(random_state=0,ccp_alpha=a).fit(Xtr,ytr)) for a in path.ccp_alphas[::5]),key=lambda m:m.score(Xte,yte))
# better: pick alpha by CV
from sklearn.model_selection import GridSearchCV
g=GridSearchCV(DecisionTreeClassifier(random_state=0),{"ccp_alpha":path.ccp_alphas[::5]},cv=5).fit(Xtr,ytr)
m=g.best_estimator_
print("pruned: alpha",round(g.best_params_["ccp_alpha"],5),"leaves",m.get_n_leaves(),"train",round(m.score(Xtr,ytr),3),"test",round(m.score(Xte,yte),3))
