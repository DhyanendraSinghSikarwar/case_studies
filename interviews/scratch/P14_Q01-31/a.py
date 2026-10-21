import numpy as np, math
rng=np.random.default_rng(0)
print("Q1", 0.25, 2)
# Q2
def pcoll(n,d=365):
    return 1-np.prod([(d-i)/d for i in range(n)])
n=1
while pcoll(n)<0.5:n+=1
print("Q2",n,pcoll(n),pcoll(23),pcoll(57),pcoll(70))
print("sqrt approx",math.sqrt(2*365*math.log(2)),1.1774*math.sqrt(365))
print("hash 2^32:",1.1774*2**16, "2^64:",1.1774*2**32, "2^128 n",1.1774*2**64)
sim=np.mean([len(set(rng.integers(0,365,23)))<23 for _ in range(100000)]);print("sim23",sim)
# Q3
p=0.01;se=.99;sp=.95
post=se*p/(se*p+(1-sp)*(1-p));print("Q3",post)
# per 10000
print(10000*p*se, 10000*(1-p)*(1-sp))
# Q4
N=100000
car=rng.integers(0,3,N);pick=rng.integers(0,3,N)
# host opens a goat door; switching wins iff pick!=car
print("Q4 stay",np.mean(pick==car),"switch",np.mean(pick!=car))
# Q5
print("Q5 coupon n=6",6*sum(1/k for k in range(1,7)))
for n in [10,100,1000]:print(n,n*sum(1/k for k in range(1,n+1)),n*(math.log(n)+0.5772))
sim=[]
for _ in range(20000):
    seen=set();t=0
    while len(seen)<6:seen.add(rng.integers(6));t+=1
    sim.append(t)
print("sim",np.mean(sim))
# Q7
def sim_pat(pat,N=100000):
    pat=list(pat);tot=0
    for _ in range(N):
        s=[];t=0
        while True:
            s.append(rng.integers(2));t+=1
            if len(s)>=len(pat) and s[-len(pat):]==pat:break
        tot+=t
    return tot/N
print("Q7 HH",sim_pat([1,1],30000),"HT",sim_pat([1,0],30000))
# Q8
k=rng.integers(0,2,(N,2))
atleast=(k.sum(1)>=1);print("Q8",np.mean(k[atleast].sum(1)==2),np.mean(k[k[:,0]==1][:,1]==1))
# Q9
def vn(p,size):
    out=[]
    while len(out)<size:
        a,b=rng.random()<p,rng.random()<p
        if a!=b: out.append(int(a))
    return out
x=vn(0.8,20000);print("Q9 vN mean",np.mean(x))
def uniform_k(p,k):
    # rejection with 3 bits for 7 outcomes
    while True:
        bits=vn(p,3)
        v=bits[0]*4+bits[1]*2+bits[2]
        if v<k: return v
c=np.bincount([uniform_k(0.8,7) for _ in range(7000)],minlength=7)/7000;print(c)
print("exp bits per vN",1/(p*(1-p)) if False else 1/(2*0.8*0.2))
# Q17
M=1_000_000
xy=rng.random((M,2));est=4*np.mean((xy**2).sum(1)<1);print("Q17 pi",est,"se",4*math.sqrt(math.pi/4*(1-math.pi/4)/M))
u=rng.random(M);print("int e^-x2",np.mean(np.exp(-u**2)), "true",0.7468241328)
print("n for +-0.001 at p=.5 95%:",(1.96*0.5/0.001)**2)
# Q20
print("Q20",100/6-20, 100**2/6*(5/6))
# Q21
print("Q21",4/52*3/51,3*13*4/ (52*51)*1, 51/52*3/51, 26/52*25/51)
# Q24
d=np.arange(1,7);E2=sum(m*((m**2-(m-1)**2)/36) for m in d);print("Q24",E2)
for n in [1,2,3,10]:print(n,sum(m*((m/6)**n-((m-1)/6)**n) for m in d), n/(n+1))
# Q25
print("Q25 distinct bdays n=23",365*(1-(364/365)**23),"empty bins m=n=100",100*(1-1/100)**100,100/math.e)
perm=[np.sum(rng.permutation(10)==np.arange(10)) for _ in range(100000)];print("fixed",np.mean(perm))
# Q26
def ruin_sim(i,N,p,T=20000):
    r=0;dur=0
    for _ in range(T):
        x=i;t=0
        while 0<x<N:
            x+=1 if rng.random()<p else -1;t+=1
        r+= x==0;dur+=t
    return r/T,dur/T
print("Q26 fair i=3 N=10: ruin",1-3/10,"dur",3*7,ruin_sim(3,10,.5))
q=.55;i=3;N=10;rr=((1-.45)/.55)
# p=.45 : ruin prob = ((q/p)^i -(q/p)^N)/(1-(q/p)^N), q/p
p_=.45;r=(1-p_)/p_
ruin=(r**i-r**N)/(1-r**N);dur=i/(1-2*p_)-N/(1-2*p_)*(1-r**i)/(1-r**N)
print("p=.45",ruin,dur,ruin_sim(3,10,.45))
# Q27
print("Q27 return prob by 2n: n=",[ (math.comb(2*n,n)/4**n) for n in [1,5,50]])
