import numpy as np
churn   =np.array([1,1,1,1,0,0, 1,0,0,0])        # 10 customers
premium =np.array([0,0,0,0,0,0, 1,1,1,1])        # feature A: plan (0=Basic,1=Premium)
longten =np.array([0,0,0,0,1,0, 0,1,1,1])        # feature B: tenure > 12 months
def gini(y): p=y.mean(); return 1-p**2-(1-p)**2
def ent(y):
    p=y.mean(); return 0 if p in (0,1) else -(p*np.log2(p)+(1-p)*np.log2(1-p))
for name,f in [("plan",premium),("tenure>12",longten)]:
    for cn,c in [("gini",gini),("entropy",ent)]:
        w=sum((f==v).mean()*c(churn[f==v]) for v in (0,1))
        print(name,cn,"parent",round(c(churn),3),"child",round(w,3),"gain",round(c(churn)-w,3))
