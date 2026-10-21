import numpy as np
from sklearn.metrics import roc_auc_score, average_precision_score, f1_score, precision_score, recall_score
# Q6/Q7/Q31-style: 1% positives, AUC high, precision low
rng=np.random.default_rng(0)
n=100000; y=(rng.random(n)<0.01).astype(int); s=rng.normal(size=n)+2.0*y
print("Q6 AUC",round(roc_auc_score(y,s),3),"AP",round(average_precision_score(y,s),3),"baseline",y.mean().round(4))
for t in [1.0,2.0]:
    p=(s>t).astype(int)
    print("Q7 thr",t,"prec",round(precision_score(y,p),3),"rec",round(recall_score(y,p),3),"F1",round(f1_score(y,p),3))
# FP counts at thr 1.0
p=(s>1.0); print("FP",int((p&(y==0)).sum()),"TP",int((p&(y==1)).sum()))
