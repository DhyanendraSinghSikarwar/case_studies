import numpy as np
from sklearn.metrics import f1_score, classification_report
y=np.array([0]*90+[1]*8+[2]*2)
p=np.array([0]*88+[1]*2 + [1]*6+[0]*2 + [2]*1+[0]*1)
print(len(y),len(p))
for a in ["micro","macro","weighted"]: print(a,round(f1_score(y,p,average=a),3))
print(classification_report(y,p,digits=2,zero_division=0))
