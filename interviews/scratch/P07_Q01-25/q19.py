import numpy as np, lightgbm as lgb
from sklearn.metrics import ndcg_score
rng = np.random.default_rng(0)
nq, per = 300, 20
X = rng.normal(size=(nq*per, 5))
score = X[:,0] + .5*X[:,1] + rng.normal(0,.5,nq*per)
y = np.digitize(score, np.quantile(score, [.5,.8,.95]))      # graded labels 0..3
group = [per]*nq                                             # rows must be contiguous per query
tr = slice(0, 240*per); va = slice(240*per, None)
m = lgb.LGBMRanker(objective="lambdarank", n_estimators=100, learning_rate=.1,
                   min_child_samples=5, random_state=0, n_jobs=1, verbose=-1)
m.fit(X[tr], y[tr], group=[per]*240, eval_set=[(X[va], y[va])], eval_group=[[per]*60],
      eval_at=[5], eval_metric="ndcg")
pred = m.predict(X[va])
print("val NDCG@5:", round(ndcg_score(y[va].reshape(60,per), pred.reshape(60,per), k=5), 3))
print("random   :", round(ndcg_score(y[va].reshape(60,per), rng.random((60,per)), k=5), 3))
