import numpy as np
rng=np.random.default_rng(0)
P=np.array([[.9,.1,0],[.2,.7,.1],[.1,.2,.7]])
w,v=np.linalg.eig(P.T);pi=np.real(v[:,np.argmin(abs(w-1))]);pi/=pi.sum();print("Q28 pi",pi,pi@P)
A=np.vstack([P.T-np.eye(3),np.ones(3)]);b=np.r_[np.zeros(3),1];print(np.linalg.lstsq(A,b,rcond=None)[0])
print(np.linalg.matrix_power(P,100)[0])
sim=np.array([[.80,.15,.05],[.30,.50,.20],[0,0,1.]])
U=5000;T=12;S=np.zeros((U,T),int);cum=sim.cumsum(1)
for t in range(1,T):
    S[:,t]=(rng.random(U)[:,None]>cum[S[:,t-1]]).sum(1)
cnt=np.zeros((3,3))
np.add.at(cnt,(S[:,:-1].ravel(),S[:,1:].ravel()),1)
Ph=cnt/cnt.sum(1,keepdims=True);print(np.round(Ph,3))
Q=Ph[:2,:2];N=np.linalg.inv(np.eye(2)-Q);print("expected months from active",N[0].sum(),"true",np.linalg.inv(np.eye(2)-sim[:2,:2])[0].sum())
# 2nd-order check: from state 'active' now, does previous state matter?
prev,cur,nxt=S[:,:-2].ravel(),S[:,1:-1].ravel(),S[:,2:].ravel()
for a in [0,1]:
    m=(cur==0)&(prev==a);print("prev",a,"P(next|cur=active)",np.round(np.bincount(nxt[m],minlength=3)/m.sum(),3))
L=np.array([[0,1,1,0],[0,0,1,0],[1,0,0,1],[0,0,1,0]],float)
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
# exact solve check
n=4;out=L.sum(1,keepdims=True);Pm=L/out
G=.85*Pm+.15/n;w,v=np.linalg.eig(G.T);x=np.real(v[:,np.argmax(np.real(w))]);print(x/x.sum())
# dangling case
L2=L.copy();L2[3]=0;print(pagerank(L2))
# peek fast
def peek(nsim=4000,days=14,per=200):
    a=rng.normal(size=(nsim,days,per));b=rng.normal(size=(nsim,days,per))
    n=per*np.arange(1,days+1)
    ca=a.sum(2).cumsum(1);cb=b.sum(2).cumsum(1)
    ca2=(a**2).sum(2).cumsum(1);cb2=(b**2).sum(2).cumsum(1)
    ma,mb=ca/n,cb/n
    va=(ca2-n*ma**2)/(n-1);vb=(cb2-n*mb**2)/(n-1)
    z=(ma-mb)/np.sqrt((va+vb)/n)
    rej=np.abs(z)>1.96
    return rej.any(1).mean(),rej[:,-1].mean()
print("peek",peek())
