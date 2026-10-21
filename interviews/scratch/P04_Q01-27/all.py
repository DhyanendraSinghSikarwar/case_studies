import numpy as np, time
import xgboost as xgb
from sklearn.datasets import make_classification, make_regression
from sklearn.model_selection import train_test_split, cross_val_score, RandomizedSearchCV
from sklearn.ensemble import RandomForestClassifier, ExtraTreesClassifier, AdaBoostClassifier, GradientBoostingClassifier
from sklearn.metrics import roc_auc_score, average_precision_score
from sklearn.inspection import permutation_importance
from sklearn.linear_model import LinearRegression
from sklearn.tree import DecisionTreeRegressor
print("=== Q9/11/19 early stopping, lr vs trees")
X,y=make_classification(6000,20,n_informative=8,flip_y=0.1,random_state=0)
Xtr,Xtmp,ytr,ytmp=train_test_split(X,y,test_size=0.4,random_state=0)
Xva,Xte,yva,yte=train_test_split(Xtmp,ytmp,test_size=0.5,random_state=0)
for lr in (0.3,0.05):
    m=xgb.XGBClassifier(n_estimators=2000,learning_rate=lr,max_depth=4,subsample=0.8,colsample_bytree=0.8,
        early_stopping_rounds=50,eval_metric="auc",random_state=0)
    m.fit(Xtr,ytr,eval_set=[(Xva,yva)],verbose=False)
    print(lr,"best_iter",m.best_iteration,"val auc",round(m.best_score,4),"test auc",round(roc_auc_score(yte,m.predict_proba(Xte)[:,1]),4))
print("=== Q12/22 MDI vs permutation with noise high-card feature")
rng=np.random.default_rng(0)
Xs,ys=make_classification(2000,5,n_informative=3,n_redundant=0,flip_y=0.2,random_state=0)
noise=rng.normal(size=(2000,1))   # continuous noise = many unique values
Xn=np.hstack([Xs,noise]); 
Xa,Xb,ya,yb=train_test_split(Xn,ys,test_size=0.3,random_state=0)
rf=RandomForestClassifier(300,random_state=0,min_samples_leaf=1).fit(Xa,ya)
print("train acc",round(rf.score(Xa,ya),3),"test acc",round(rf.score(Xb,yb),3))
print("MDI   ",rf.feature_importances_.round(3))
pi=permutation_importance(rf,Xb,yb,n_repeats=10,random_state=0)
print("perm  ",pi.importances_mean.round(3))
print("=== Q23 correlated")
Xc=Xs[:,:3].copy(); Xc=np.hstack([Xc,Xc[:,[0]]+rng.normal(0,0.05,(2000,1))])  # col3 ~ copy of col0
Xa,Xb,ya,yb=train_test_split(Xc,ys,test_size=0.3,random_state=0)
rf=RandomForestClassifier(300,random_state=0,min_samples_leaf=5).fit(Xa,ya)
pi=permutation_importance(rf,Xb,yb,n_repeats=10,random_state=0)
print("perm with dup:",pi.importances_mean.round(3))
rf2=RandomForestClassifier(300,random_state=0,min_samples_leaf=5).fit(Xa[:,:3],ya)
pi2=permutation_importance(rf2,Xb[:,:3],yb,n_repeats=10,random_state=0)
print("perm no dup  :",pi2.importances_mean.round(3))
print("=== Q13 native TreeSHAP additivity")
m=xgb.XGBClassifier(n_estimators=100,max_depth=3,random_state=0).fit(Xtr,ytr)
c=m.get_booster().predict(xgb.DMatrix(Xte[:5]),pred_contribs=True)
raw=m.predict(Xte[:5],output_margin=True)
print(c.shape, np.allclose(c.sum(1),raw,atol=1e-4))
print("mean |shap| top3 features:", np.argsort(-np.abs(m.get_booster().predict(xgb.DMatrix(Xte),pred_contribs=True)[:,:-1]).mean(0))[:3])
try:
    import shap; print("shap", shap.__version__)
except Exception as e: print("no shap",e)
print("=== Q14 NaN")
Xm=Xtr.copy(); mask=np.random.default_rng(1).random(Xm.shape)<0.2; Xm[mask]=np.nan
Xtm=Xte.copy(); Xtm[np.random.default_rng(2).random(Xtm.shape)<0.2]=np.nan
m=xgb.XGBClassifier(n_estimators=100,max_depth=4,random_state=0).fit(Xm,ytr)
print("xgb with 20% NaN, test auc",round(roc_auc_score(yte,m.predict_proba(Xtm)[:,1]),3))
print("=== Q16 hand table: see q16")
print("=== Q17 regression split")
x=np.array([1,2,3,10,11,12.]); yy=np.array([5,6,5,20,21,19.])
def sse(v): return ((v-v.mean())**2).sum()
for t in (2.5,6.5,10.5): 
    l=yy[x<=t]; r=yy[x>t]; print(t, round(sse(l)+sse(r),2), l.mean().round(2), r.mean().round(2))
print("total SSE",round(sse(yy),2))
print("=== Q18 OOB")
rf=RandomForestClassifier(300,oob_score=True,random_state=0).fit(Xtr,ytr)
print("OOB acc",round(rf.oob_score_,4),"test acc",round(rf.score(Xte,yte),4))
print("=== Q20/21")
for n,mm in [("RF",RandomForestClassifier(200,random_state=0)),("ET",ExtraTreesClassifier(200,random_state=0)),
  ("AdaBoost",AdaBoostClassifier(n_estimators=200,random_state=0)),("GBM",GradientBoostingClassifier(n_estimators=200,random_state=0))]:
    t0=time.time(); mm.fit(Xtr,ytr); print(n,"test auc",round(roc_auc_score(yte,mm.predict_proba(Xte)[:,1]),4),"fit s",round(time.time()-t0,1))
print("=== Q24 imbalance")
Xi,yi=make_classification(20000,20,n_informative=6,weights=[0.98],flip_y=0.01,random_state=0)
Xa,Xb,ya,yb=train_test_split(Xi,yi,test_size=0.3,stratify=yi,random_state=0)
spw=(ya==0).sum()/(ya==1).sum()
for n,kw in [("plain",{}),("spw",{"scale_pos_weight":spw})]:
    m=xgb.XGBClassifier(n_estimators=300,max_depth=4,learning_rate=0.1,random_state=0,**kw).fit(Xa,ya)
    p=m.predict_proba(Xb)[:,1]
    print(n,"PR-AUC",round(average_precision_score(yb,p),3),"ROC-AUC",round(roc_auc_score(yb,p),3),"mean p",round(p.mean(),3),"true rate",round(yb.mean(),3))
print("=== Q27 extrapolation")
xt=np.linspace(0,10,200)[:,None]; yt=2*xt[:,0]+np.random.default_rng(0).normal(0,0.5,200)
xo=np.array([[12.],[15.]])
print("tree",DecisionTreeRegressor(max_depth=5).fit(xt,yt).predict(xo).round(1),"linear",LinearRegression().fit(xt,yt).predict(xo).round(1),"truth",[24,30])
import lightgbm as lgb
print("lgb linear_tree",lgb.LGBMRegressor(linear_tree=True,n_estimators=50,verbose=-1,min_child_samples=5).fit(xt,yt).predict(xo).round(1))
lin=LinearRegression().fit(xt,yt); res=yt-lin.predict(xt)
tr=DecisionTreeRegressor(max_depth=3).fit(xt,res)
print("linear+tree residual",(lin.predict(xo)+tr.predict(xo)).round(1))
print("=== Q25 lightgbm")
for nl,md in [(31,-1),(255,-1),(31,5)]:
    m=lgb.LGBMClassifier(n_estimators=200,num_leaves=nl,max_depth=md,learning_rate=0.05,verbose=-1,random_state=0).fit(Xtr,ytr)
    print(nl,md,"test auc",round(roc_auc_score(yte,m.predict_proba(Xte)[:,1]),4))
print("=== Q26")
try:
    import optuna; print("optuna",optuna.__version__)
except Exception as e: print("no optuna")
from scipy.stats import randint, uniform, loguniform
rs=RandomizedSearchCV(xgb.XGBClassifier(n_estimators=150,random_state=0),{"max_depth":randint(3,9),"learning_rate":loguniform(0.02,0.3),
 "subsample":uniform(0.6,0.4),"colsample_bytree":uniform(0.5,0.5),"min_child_weight":randint(1,10)},n_iter=10,cv=3,scoring="roc_auc",random_state=0)
rs.fit(Xtr,ytr); print(rs.best_score_.round(4),{k:round(v,3) for k,v in rs.best_params_.items()})
print("DONE")
