import numpy as np, xgboost as xgb, shap, optuna
from sklearn.datasets import make_classification
from sklearn.model_selection import train_test_split, cross_val_score, StratifiedKFold
optuna.logging.set_verbosity(optuna.logging.WARNING)
X,y=make_classification(3000,10,n_informative=5,random_state=0)
Xtr,Xte,ytr,yte=train_test_split(X,y,test_size=0.3,random_state=0)
m=xgb.XGBClassifier(n_estimators=100,max_depth=3,random_state=0).fit(Xtr,ytr)
ex=shap.TreeExplainer(m); sv=ex(Xte)       # sv.values are in log-odds (margin) space
print(sv.values.shape, np.allclose(sv.values[0].sum()+sv.base_values[0], m.predict(Xte[:1],output_margin=True)[0],atol=1e-3))
imp=np.abs(sv.values).mean(0); print("global top3:",np.argsort(-imp)[:3], "builtin gain top3:",np.argsort(-m.feature_importances_)[:3])
print("row0 contributions top:",np.argsort(-np.abs(sv.values[0]))[:3], sv.values[0][np.argsort(-np.abs(sv.values[0]))[:3]].round(2))
# optuna
def objective(trial):
    p=dict(max_depth=trial.suggest_int("max_depth",3,8),learning_rate=trial.suggest_float("learning_rate",0.02,0.3,log=True),
           subsample=trial.suggest_float("subsample",0.6,1.0),colsample_bytree=trial.suggest_float("colsample_bytree",0.5,1.0),
           min_child_weight=trial.suggest_int("min_child_weight",1,10),reg_lambda=trial.suggest_float("reg_lambda",1e-2,10,log=True))
    return cross_val_score(xgb.XGBClassifier(n_estimators=150,random_state=0,**p),Xtr,ytr,cv=StratifiedKFold(3,shuffle=True,random_state=0),scoring="roc_auc").mean()
st=optuna.create_study(direction="maximize",sampler=optuna.samplers.TPESampler(seed=0)); st.optimize(objective,n_trials=15)
print(round(st.best_value,4), {k:(round(v,3) if isinstance(v,float) else v) for k,v in st.best_params.items()})
print("DONE")
