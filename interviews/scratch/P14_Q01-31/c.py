import numpy as np, scipy.stats as st
rng=np.random.default_rng(0)
# Q28 stationary
P=np.array([[.9,.1,0],[.2,.7,.1],[.1,.2,.7]])
w,v=np.linalg.eig(P.T);pi=np.real(v[:,np.argmin(abs(w-1))]);pi/=pi.sum();print("Q28 pi",pi,pi@P)
A=np.vstack([P.T-np.eye(3),np.ones(3)]);b=np.r_[np.zeros(3),1];print(np.linalg.lstsq(A,b,rcond=None)[0])
print(np.linalg.matrix_power(P,100)[0])
# Q29 churn chain: states 0 active,1 dormant,2 churned (absorbing)
rows=[]
sim=np.array([[.80,.15,.05],[.30,.50,.20],[0,0,1.]])
# simulate user paths
def path(T=12):
    s=0;out=[s]
    for _ in range(T-1):
        s=rng.choice(3,p=sim[s]);out.append(s)
    return out
paths=[path() for _ in range(5000)]
counts=np.zeros((3,3))
for p in paths:
    for a,b in zip(p[:-1],p[1:]):counts[a,b]+=1
Ph=counts/counts.sum(1,keepdims=True);print("Q29 est",np.round(Ph,3))
Q=Ph[:2,:2];Nf=np.linalg.inv(np.eye(2)-Q);print("N",Nf,"expected months to churn from active",Nf[0].sum(),"true",np.linalg.inv(np.eye(2)-sim[:2,:2])[0].sum())
# Markov check: P(next|current,prev) 2nd order
c2={}
for p in paths:
    for a,b,c in zip(p[:-2],p[1:-1],p[2:]):
        if b==0:c2.setdefault(a,np.zeros(3))[c]+=1
print({k:np.round(v/v.sum(),3) for k,v in c2.items()})
# Q30 pagerank
L=np.array([[0,1,1,0],[0,0,1,0],[1,0,0,1],[0,0,1,0]],float)  # i links to j
def pagerank(L,d=.85,tol=1e-10):
    n=len(L);out=L.sum(1,keepdims=True)
    P=np.where(out>0,L/np.where(out>0,out,1),1/n)
    r=np.ones(n)/n
    for it in range(1000):
        r2=d*r@P+(1-d)/n
        if np.abs(r2-r).sum()<tol:return r2,it
        r=r2
    return r,it
r,it=pagerank(L);print("Q30",r,r.sum(),it)
import networkx as nx
G=nx.from_numpy_array(L,create_using=nx.DiGraph);print(nx.pagerank(G,alpha=.85))
