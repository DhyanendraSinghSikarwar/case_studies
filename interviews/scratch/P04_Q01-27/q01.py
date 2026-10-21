import numpy as np
def gini(y):
    p = np.bincount(y)/len(y); return 1-(p**2).sum()
def entropy(y):
    p = np.bincount(y)/len(y); p=p[p>0]; return -(p*np.log2(p)).sum()
def best_split(x, y, crit=gini):
    best=(None,-1); parent=crit(y)
    for t in np.unique(x)[:-1]:
        l=y[x<=t]; r=y[x>t]
        gain=parent-(len(l)*crit(l)+len(r)*crit(r))/len(y)
        if gain>best[1]: best=(t,gain)
    return best
x=np.array([22,25,30,35,40,45,50,55]); y=np.array([0,0,0,1,0,1,1,1])
print(round(gini(y),3), round(entropy(y),3))
print(best_split(x,y,gini)); print(best_split(x,y,entropy))
