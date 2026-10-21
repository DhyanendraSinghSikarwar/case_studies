import numpy as np
from sklearn.metrics import roc_auc_score, brier_score_loss, f1_score
rng=np.random.default_rng(0); y=(rng.random(20000)<0.1).astype(int)
z=rng.normal(size=20000)+1.5*y; p=1/(1+np.exp(-(z-2.2)))
p_bad=p**0.3   # monotone distortion: over-confident
print("Q14 AUC",round(roc_auc_score(y,p),4),round(roc_auc_score(y,p_bad),4),"mean pred",round(p.mean(),3),round(p_bad.mean(),3),"true",y.mean().round(3))
print("Q14 Brier",round(brier_score_loss(y,p),4),round(brier_score_loss(y,p_bad),4))
# Q17
yt=np.array([0]*90+[1]*8+[2]*2); yp=np.array([0]*88+[1]*2 + [1]*6+[0]*2 + [0]*2)
for a in ["micro","macro","weighted"]: print("Q17",a,round(f1_score(yt,yp,average=a),3))
