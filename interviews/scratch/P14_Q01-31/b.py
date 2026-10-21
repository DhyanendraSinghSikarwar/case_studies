import numpy as np, scipy.stats as st, pandas as pd, statsmodels.api as sm
from statsmodels.stats.diagnostic import het_breuschpagan, het_white
rng=np.random.default_rng(0)
# Q11 heteroscedasticity
n=500;x=rng.uniform(1,10,n);y=2+3*x+rng.normal(0,x)  # sd grows with x
X=sm.add_constant(x);m=sm.OLS(y,X).fit()
print("BP p",het_breuschpagan(m.resid,X)[1],"White p",het_white(m.resid,X)[1])
print("naive se",m.bse,"HC3 se",m.get_robustcov_results('HC3').bse)
w=sm.WLS(y,X,weights=1/x**2).fit();print("WLS se",w.bse)
# Q22 influence
x=rng.normal(size=30);y=1+2*x+rng.normal(0,.5,30);x[0]=6;y[0]=-5
m=sm.OLS(y,sm.add_constant(x)).fit();inf=m.get_influence()
h=inf.hat_matrix_diag;cd=inf.cooks_distance[0]
print("Q22 lev0",h[0],"thr",2*2/30,"cook0",cd[0],"thr",4/30,"max other cook",np.sort(cd)[-2], "slope",m.params[1])
m2=sm.OLS(y[1:],sm.add_constant(x[1:])).fit();print("slope w/o",m2.params[1])
# Q13/14 beta-binomial
a,b,k,n=1,1,30,200
post=st.beta(a+k,b+n-k);print("Q14 mean",post.mean(),post.interval(.95))
from statsmodels.stats.proportion import proportion_confint
print("wilson",proportion_confint(k,n,method='wilson'))
a,b=20,180
post=st.beta(a+k,b+n-k);print("informative prior(20,180) mean",post.mean(),post.interval(.95))
# Q18
for (a,b) in [(1,1),(20,180),(200,1800)]:
    for (k,n) in [(3,20),(300,2000)]:
        p=st.beta(a+k,b+n-k);print((a,b),(k,n),round(p.mean(),4),np.round(p.interval(.95),4))
# Q15 CUPED
N=20000;pre=rng.normal(10,3,N);y0=0.8*pre+rng.normal(0,2,N)
t=rng.integers(0,2,N);y=y0+0.2*t
th=np.cov(y,pre)[0,1]/np.var(pre,ddof=1);yc=y-th*(pre-pre.mean())
def diff(v):
    d=v[t==1].mean()-v[t==0].mean();se=np.sqrt(v[t==1].var(ddof=1)/(t==1).sum()+v[t==0].var(ddof=1)/(t==0).sum());return d,se
print("Q15 theta",th,"raw",diff(y),"cuped",diff(yc),"rho2",np.corrcoef(y,pre)[0,1]**2,"var ratio",yc.var()/y.var())
# Q16 peeking
def peek(nsim=2000,days=14,per=200,peeks=True):
    fp=0
    for _ in range(nsim):
        a=rng.normal(size=(days,per));b=rng.normal(size=(days,per))
        rej=False
        for d in range(1,days+1) if peeks else [days]:
            x=a[:d].ravel();y=b[:d].ravel()
            z=(x.mean()-y.mean())/np.sqrt(x.var(ddof=1)/len(x)+y.var(ddof=1)/len(y))
            if abs(z)>1.96:rej=True;break
        fp+=rej
    return fp/nsim
print("Q16 peek",peek(),"single",peek(peeks=False))
# Q31 bayes AB
A=st.beta(1+120,1+1000-120);B=st.beta(1+140,1+1000-140)
s=500000;a=A.rvs(s,random_state=1);b=B.rvs(s,random_state=2)
print("Q31 P(B>A)",np.mean(b>a),"EL choose B",np.mean(np.maximum(a-b,0)),"EL choose A",np.mean(np.maximum(b-a,0)))
from statsmodels.stats.proportion import proportions_ztest
print("z test",proportions_ztest([140,120],[1000,1000]))
print("lift CI",np.percentile(b/a-1,[2.5,97.5]))
