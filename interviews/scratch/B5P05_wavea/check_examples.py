# Runs every example printed in the Part 5 prompts against brute-force / independent reference code, plus exhaustive checks of the claims
# (uniqueness, equivalences, call budgets, non-termination). Run: python3 -I check_examples.py
import bisect, itertools, math, random, sys
from functools import lru_cache
def ok(name, got, exp): assert got == exp, (name, got, exp)
random.seed(5)
# ---- reference solvers (all brute force / linear) ----
def idx(a,t): return a.index(t) if t in a else -1
def ins(a,t): return sum(1 for v in a if v<t)
# 1
ok('q1',[idx([-1,0,3,5,9,12],9),idx([-1,0,3,5,9,12],2),idx([5],5),idx([5],4)],[4,-1,0,-1])
# 2
ok('q2',[ins([1,3,5,6],5),ins([1,3,5,6],2),ins([1,3,5,6],7),ins([1,3,5,6],0),ins([],3)],[2,1,4,0,0])
# 3 isqrt
def isq(x): return max(r for r in range(0,50000) if r*r<=x)
ok('q3',[isq(4),isq(8),isq(0),isq(1),isq(2147395599),isq(2147395600)],[2,2,0,1,46339,46340])
assert math.isqrt(2147395599)==46339 and 46341**2>2**31-1>46340**2
# 4
def fl(a,t):
    p=[i for i,v in enumerate(a) if v==t]; return [p[0],p[-1]] if p else [-1,-1]
ok('q4',[fl([5,7,7,8,8,10],8),fl([5,7,7,8,8,10],6),fl([],0),fl([1],1),fl([2,2,2,2],2)],[[3,4],[-1,-1],[-1,-1],[0,0],[0,3]])
# 5 rotated
ok('q5',[idx([4,5,6,7,0,1,2],0),idx([4,5,6,7,0,1,2],3),idx([1],0),idx([3,1],1),idx([1,3],3)],[4,-1,-1,1,1])
# 6
ok('q6',[min(x) for x in ([3,4,5,1,2],[4,5,6,7,0,1,2],[11,13,15,17],[2,1],[7])],[1,0,11,1,7])
# 7 koko
def koko(p,h): return next(k for k in range(1,max(p)+1) if sum(-(-x//k) for x in p)<=h)
ok('q7',[koko([3,6,7,11],8),koko([30,11,23,4,20],5),koko([30,11,23,4,20],6),koko([5],5)],[4,30,23,1])
# 8 ship
def days(w,c):
    d=1;cur=0
    for x in w:
        if cur+x>c: d+=1;cur=0
        cur+=x
    return d
def ship(w,D): return next(c for c in range(max(w),sum(w)+1) if days(w,c)<=D)
ok('q8',[ship(list(range(1,11)),5),ship([3,2,2,4,1,4],3),ship([1,2,3,1,1],4),ship([7],1)],[15,6,3,7])
# 9 peak: any
def peaks(a):
    n=len(a); g=lambda i:a[i] if 0<=i<n else -math.inf
    return [i for i in range(n) if g(i)>g(i-1) and g(i)>g(i+1)]
ok('q9',[peaks([1,2,3,1]),peaks([1,2,1,3,5,6,4]),peaks([1]),peaks([2,1]),peaks([1,2])],[[2],[1,5],[0],[0],[1]])
# 10
M=[[1,3,5,7],[10,11,16,20],[23,30,34,60]]
ok('q10',[any(3 in r for r in M),any(13 in r for r in M),any(1 in r for r in [[1]]),any(3 in r for r in [[1],[3]])],[True,False,True,True])
# 11 bisect
a=[1,2,2,2,3,5]
lb=lambda a,x:sum(v<x for v in a); ub=lambda a,x:sum(v<=x for v in a)
fl_=lambda a,x:max([v for v in a if v<=x],default=None); su=lambda a,x:min([v for v in a if v>x],default=None)
ok('q11',[lb(a,2),ub(a,2),ub(a,2)-lb(a,2),sum(2<=v<=3 for v in a),fl_(a,4),su(a,5),lb(a,0),ub(a,9)],[1,4,3,4,3,None,0,6])
assert all(bisect.bisect_left(a,x)==lb(a,x) and bisect.bisect_right(a,x)==ub(a,x) for x in range(-1,8))
# 12 median
def med(a,b):
    s=sorted(a+b); n=len(s); return float(s[n//2]) if n%2 else (s[n//2-1]+s[n//2])/2
ok('q12',[med([1,3],[2]),med([1,2],[3,4]),med([],[5]),med([0,0],[0,0]),med([1,2,3],[])],[2.0,2.5,5.0,0.0,2.0])
# 13 split array: DP reference + claim exactly-k == at-most-k
def split_dp(nums,k,exact=True):
    n=len(nums); pre=[0]
    for x in nums: pre.append(pre[-1]+x)
    INF=float('inf')
    @lru_cache(None)
    def f(i,j): # i elems consumed, j pieces left
        if j==0: return 0 if i==n else INF
        if i==n: return INF if exact else 0
        return min((max(pre[m]-pre[i],f(m,j-1)) for m in range(i+1,n+1)),default=INF)
    return f(0,k)
ok('q13',[split_dp((7,2,5,10,8),2),split_dp((1,2,3,4,5),2),split_dp((1,4,4),3),split_dp((5,),1)],[18,9,4,5])
for _ in range(400):
    n=random.randint(1,7); nums=tuple(random.randint(0,6) for _ in range(n)); k=random.randint(1,n)
    ex=split_dp(nums,k,True)
    # at-most-k via predicate
    am=next(S for S in range(max(nums),sum(nums)+1) if days(list(nums),S)<=k) if max(nums)>0 else 0
    assert ex==am,(nums,k,ex,am)
# 14
sq=lambda x:any(r*r==x for r in range(0,46341))
ok('q14',[sq(16),sq(14),sq(1),sq(2),sq(2147395600),sq(2147483647)],[True,False,True,False,True,False])
# 15 first bad: call budget exhaustive
def fbv(n,f):
    calls=0
    def bad(v):
        nonlocal calls; calls+=1; return v>=f
    lo,hi=1,n
    while lo<hi:
        mid=(lo+hi)//2
        if bad(mid): hi=mid
        else: lo=mid+1
    return lo,calls
for n in range(1,300):
    for f in range(1,n+1):
        r,c=fbv(n,f); assert r==f and c<=math.ceil(math.log2(n)),(n,f,r,c)
assert fbv(10**9,10**9)==(10**9,30) or fbv(10**9,10**9)[1]<=30
assert fbv(5,4)[0]==4 and fbv(1,1)[0]==1 and fbv(2,2)[0]==2
# 26
def nxt(L,t): return next((c for c in L if c>t),L[0])
ok('q26',[nxt(['c','f','j'],'a'),nxt(['c','f','j'],'c'),nxt(['c','f','j'],'j'),nxt(list('xxyy'),'z'),nxt(list('xxyy'),'x')],['c','f','c','x','y'])
# 16 rotated w/ dups
ok('q16',[3 in [2,5,6,0,0,1,2] ,0 in [2,5,6,0,0,1,2],0 in [1,0,1,1,1],2 in [1,1,1,1],0 in [1,1,1,1,0,1,1]][::1][1:2]+[3 in [2,5,6,0,0,1,2],0 in [1,0,1,1,1],2 in [1,1,1,1],0 in [1,1,1,1,0,1,1]],[True,False,True,False,True])
# 17
ok('q17',[min(x) for x in ([1,3,5],[2,2,2,0,1],[10,1,10,10,10],[3,3,1,3],[2,2,2,2])],[1,0,1,1,2])
# 18 bouquets
def bq(bd,m,k):
    if len(bd)<m*k: return -1
    for d in sorted(set(bd)):
        run=cnt=0
        for x in bd:
            if x<=d:
                run+=1
                if run==k: cnt+=1; run=0
            else: run=0
        if cnt>=m: return d
ok('q18',[bq([1,10,3,10,2],3,1),bq([1,10,3,10,2],3,2),bq([7,7,7,7,12,7,7],2,3),bq([1,10,2,9,3,8,4,7,5,6],4,2)],[3,-1,12,9])
# 19 aggressive cows: brute over subsets
def cows(st,c):
    return max(min(b-a for a,b in zip(s,s[1:])) for s in itertools.combinations(sorted(st),c))
ok('q19',[cows([1,2,4,8,9],3),cows([1,2,3,4,7],3),cows([5,4,3,2,1,10**9],2),cows([1,2],2)],[3,3,10**9-1,1])
# 20 allocate books: brute over cuts
def books(p,m):
    n=len(p)
    if m>n: return -1
    best=10**18
    for cuts in itertools.combinations(range(1,n),m-1):
        b=(0,)+cuts+(n,); best=min(best,max(sum(p[b[i]:b[i+1]]) for i in range(m)))
    return best
ok('q20',[books([12,34,67,90],2),books([25,46,28,49,24],4),books([10,20],3),books([10,20],2),books([5,5,5,5],1)],[113,71,-1,20,20])
# 21 matrix II
M2=[[1,4,7,11,15],[2,5,8,12,19],[3,6,9,16,22],[10,13,14,17,24],[18,21,23,26,30]]
ok('q21',[any(5 in r for r in M2),any(20 in r for r in M2),-5 in [-5]],[True,False,True])
# 22 mountain
def mountain(A,t,budget=None):
    calls=0
    def get(i):
        nonlocal calls; calls+=1; return A[i]
    n=len(A); lo,hi=0,n-1
    while lo<hi:
        m=(lo+hi)//2
        if get(m)<get(m+1): lo=m+1
        else: hi=m
    p=lo
    l,h=0,p
    while l<h:
        m=(l+h)//2
        if get(m)<t: l=m+1
        else: h=m
    if get(l)==t: return l,calls
    l,h=p,n-1
    while l<h:
        m=(l+h)//2
        if get(m)>t: l=m+1
        else: h=m
    return (l if get(l)==t else -1),calls
ok('q22',[mountain([1,2,3,4,5,3,1],3)[0],mountain([0,1,2,4,2,1],3)[0],mountain([1,5,2],2)[0],mountain([1,5,2],5)[0]],[2,-1,2,1])
def mk(n):
    pk=random.randint(1,n-2); L=sorted(random.sample(range(0,3*n),pk)); R=sorted(random.sample(range(0,3*n),n-pk),reverse=True)
    top=max(L[-1],R[0])+1; return L+[top]+R[:-0 or None] if False else None
worst=0
for n in list(range(3,60))+[10**4]*3:
    for _ in range(20):
        pk=random.randint(1,n-2)
        vals=random.sample(range(0,5*n),n); pk_val=max(vals); rest=[v for v in vals if v!=pk_val]
        left=sorted(rest[:pk]); right=sorted(rest[pk:],reverse=True); A=left+[pk_val]+right
        assert all(A[i]<A[i+1] for i in range(pk)) and all(A[i]>A[i+1] for i in range(pk,n-1))
        for t in random.sample(A,3)+[-1]:
            r,c=mountain(A,t); exp=A.index(t) if t in A else -1
            assert r==exp; worst=max(worst,c)
assert worst<100,worst
print('mountain worst calls',worst)
# 23 k closest: exhaustive tie-rule
def kc(arr,k,x): return sorted(sorted(arr,key=lambda v:(abs(v-x),v))[:k])
ok('q23',[kc([1,2,3,4,5],4,3),kc([1,2,3,4,5],4,-1),kc([1,3],1,2),kc([1,1,2,3,4,5],3,4),kc([1,2,3,4,5],2,10)],[[1,2,3,4],[1,2,3,4],[1],[3,4,5],[4,5]])
def kc_bs(arr,k,x):
    lo,hi=0,len(arr)-k
    while lo<hi:
        m=(lo+hi)//2
        if x-arr[m]>arr[m+k]-x: lo=m+1
        else: hi=m
    return arr[lo:lo+k]
for _ in range(3000):
    n=random.randint(1,8); arr=sorted(random.randint(0,6) for _ in range(n)); k=random.randint(1,n); x=random.randint(-2,9)
    # alternative tie-break check: pick by (|d|, index) gives the same VALUE list
    alt=sorted(sorted(range(n),key=lambda i:(abs(arr[i]-x),i))[:k]); alt=[arr[i] for i in alt]
    assert kc(arr,k,x)==kc_bs(arr,k,x)==sorted(alt),(arr,k,x)
# 24 single
def single(a):
    from collections import Counter; return [v for v,c in Counter(a).items() if c==1]
ok('q24',[single(x) for x in ([1,1,2,3,3,4,4,8,8],[3,3,7,7,10,11,11],[5],[1,2,2],[1,1,2])],[[2],[10],[5],[1],[2]])
# 25 kth matrix
def kth(M,k): return sorted(v for r in M for v in r)[k-1]
ok('q25',[kth([[1,5,9],[10,11,13],[12,13,15]],8),kth([[-5]],1),kth([[1,2],[1,3]],2),kth([[1,2],[1,3]],3)],[13,-5,1,2])
# 27 cut wood
def wood(L,k): return max([l for l in range(1,max(L)+1) if sum(x//l for x in L)>=k],default=0)
ok('q27',[wood([232,124,456],7),wood([5,5,5],2),wood([1,2],10),wood([5,5,5],3),wood([5,5,5],4)],[114,5,0,5,2])
# 28 bisect key
people=[('ann',22),('bob',30),('cy',30),('di',41)]
kf=lambda t:t[1]
b=list(people); bisect.insort_right(b,('zed',30),key=kf)
ok('q28',[bisect.bisect_left(people,30,key=kf),b,bisect.bisect_left(range(100),50,key=lambda v:v*v)],[1,[('ann',22),('bob',30),('cy',30),('zed',30),('di',41)],8])
# claim: bisect_left key not applied to x -> compare 30 against keys directly (already shown); insort applies key to x:
b2=list(people); bisect.insort_left(b2,('zed',30),key=kf); ok('q28b',b2.index(('zed',30)),1)
assert sys.version_info>=(3,10)
# 29 templates
def t1(pred,n):
    lo,hi=0,n
    while lo<hi:
        m=(lo+hi)//2
        if pred(m): hi=m
        else: lo=m+1
    return lo
def t2(pred,n):
    lo,hi=-1,n-1
    while lo<hi:
        m=(lo+hi+1)//2
        if pred(m): lo=m
        else: hi=m-1
    return lo
a=[0,0,1,1,1]
ok('q29',[t1(lambda i:a[i]==1,5),t2(lambda i:a[i]==0,5),t1(lambda i:False,5),t2(lambda i:False,5),t1(lambda i:True,5),t2(lambda i:True,5)],[2,1,5,-1,0,4])
# exhaustive: templates match linear scans on all monotone predicates
for n in range(0,12):
    for f in range(0,n+1):
        assert t1(lambda i:i>=f,n)==f and t2(lambda i:i<f,n)==f-1
# infinite loop claim: lo=mid with mid=(lo+hi)//2 at lo=3,hi=4
lo,hi=3,4; assert (lo+hi)//2==3
# 30 exponential
def expo(hidden,t):
    S=2147483647; calls=0
    def get(i):
        nonlocal calls; calls+=1; return hidden[i] if i<len(hidden) else S
    hi=1
    while get(hi)<t: hi*=2
    lo=hi//2; 
    while lo<=hi:
        m=(lo+hi)//2; v=get(m)
        if v==t: return m
        if v<t: lo=m+1
        else: hi=m-1
    return -1
ok('q30',[expo([-1,0,3,5,9,12],9),expo([-1,0,3,5,9,12],2),expo([7],7),expo([7],8)],[4,-1,0,-1])
# hidden[0] with start hi=1: handle target at index 0 or 1
for n in range(1,40):
    h=sorted(random.sample(range(-50,50),n))
    for t in range(-55,55):
        got=expo(h,t) if t>h[0] or True else None
        exp=h.index(t) if t in h else -1
        assert got==exp,(h,t,got,exp)
# 31 float sqrt
def fsq(x,it=100):
    lo,hi=0.0,max(1.0,x)
    for _ in range(it): 
        m=(lo+hi)/2
        if m*m<=x: lo=m
        else: hi=m
    return lo
for x,e in ((2,1.41421356),(0.25,0.5),(0,0),(10**6,1000)): assert abs(fsq(x)-e)<=1e-6
assert abs(fsq(0.25,100)-0.5)<1e-6
def bad_hi(x):
    lo,hi=0.0,x
    for _ in range(100):
        m=(lo+hi)/2
        if m*m<=x: lo=m
        else: hi=m
    return lo
assert abs(bad_hi(0.25)-0.5)>1e-3   # hi = x is wrong for x<1 (0.25 -> converges to 0.25)
def eps_loop(x,eps,cap=10**6):
    lo,hi=0.0,max(1.0,x); n=0
    while hi-lo>eps:
        n+=1
        if n>cap: return None
        m=(lo+hi)/2
        if m*m<=x: lo=m
        else: hi=m
    return n
assert eps_loop(10**6,1e-15) is None and eps_loop(10**6,1e-9) is not None and abs(eps_loop(2,1e-9)-31)<=3
# 32 kth root
def iroot(x,n):
    lo,hi=0,x
    while lo<hi:
        m=(lo+hi+1)//2
        if m**n<=x: lo=m
        else: hi=m-1
    return lo
ok('q32',[iroot(27,3),iroot(125,3),iroot(80,4),iroot(10**18,2),iroot(0,5),iroot(1,60)],[3,5,2,10**9,0,1])
assert int(125**(1/3))==4
# 33 monotone
def days2(w,c): return days(w,c) if max(w)<=c else None
ok('q33a',[(days2([1,2,3],c)==2) for c in range(1,8)],[False,False,True,True,True,False,False])
arr=[5,-10,5,5]
ok('q33b',[any(sum(arr[i:i+L])>=10 for i in range(len(arr)-L+1)) for L in range(1,5)],[False,True,False,False])
# 34 kth missing
def kmiss(a,k):
    s=set(a); c=0; v=0
    while c<k:
        v+=1
        if v not in s: c+=1
    return v
ok('q34',[kmiss([2,3,4,7,11],5),kmiss([1,2,3,4],2),kmiss([5,6],1),kmiss([1,3],1),kmiss([2],3)],[9,6,1,2,4])
def kmiss_bs(a,k):
    lo,hi=0,len(a)
    while lo<hi:
        m=(lo+hi)//2
        if a[m]-(m+1)>=k: hi=m
        else: lo=m+1
    return k+lo
for _ in range(1000):
    a=sorted(random.sample(range(1,15),random.randint(1,8))); k=random.randint(1,10); assert kmiss(a,k)==kmiss_bs(a,k)
# 35 kth of two sorted
def kth2(a,b,k): return sorted(a+b)[k-1]
ok('q35',[kth2([1,3,8],[2,4,6,9],4),kth2([1,2],[1,2],3),kth2([],[3,5],2),kth2([7],[1,2,3],1),kth2([7],[1,2,3],4)],[4,2,5,1,7])
# 36 max average >=k
def maxavg(nums,k):
    best=-1e18
    for i in range(len(nums)):
        for j in range(i+k,len(nums)+1): best=max(best,sum(nums[i:j])/(j-i))
    return best
for nums,k,e in (([1,12,-5,-6,50,3],4,12.75),([5],1,5.0),([-3,-1,-2],2,-1.5),([0,4,0,3,2],1,4.0)): assert abs(maxavg(nums,k)-e)<1e-9,(nums,k)
def maxavg_bs(nums,k):
    lo,hi=min(nums),max(nums)
    for _ in range(60):
        t=(lo+hi)/2; pre=[0]
        for x in nums: pre.append(pre[-1]+x-t)
        mn=1e18; good=False
        for j in range(k,len(nums)+1):
            mn=min(mn,pre[j-k]); 
            if pre[j]-mn>=0: good=True;break
        if good: lo=t
        else: hi=t
    return lo
for _ in range(300):
    n=random.randint(1,9); nums=[random.randint(-9,9) for _ in range(n)]; k=random.randint(1,n)
    assert abs(maxavg(nums,k)-maxavg_bs(nums,k))<1e-5
# 37 median of matrix
def mmed(M): s=sorted(v for r in M for v in r); return s[len(s)//2]
ok('q37',[mmed([[1,3,5],[2,6,9],[3,6,9]]),mmed([[1]]),mmed([[1,1,1],[2,2,2],[3,3,3]])],[5,1,2])
# 38 kth pair distance
def kpd(nums,k): return sorted(abs(a-b) for a,b in itertools.combinations(nums,2))[k-1]
ok('q38',[kpd([1,3,1],1),kpd([1,1,1],2),kpd([1,6,1],3),kpd([1,3,1],2),kpd([1,3,1],3)],[0,0,5,2,2])
# 39 mult table
def mt(m,n,k): return sorted(i*j for i in range(1,m+1) for j in range(1,n+1))[k-1]
ok('q39',[mt(3,3,5),mt(2,3,6),mt(1,5,4),mt(3,3,9),mt(3,3,1)],[3,6,4,9,1])
for m in range(1,6):
    for n in range(1,6):
        for k in range(1,m*n+1):
            cnt=lambda v:sum(min(n,v//i) for i in range(1,m+1))
            v=next(v for v in range(1,m*n+1) if cnt(v)>=k); assert v==mt(m,n,k)
# 40 gas stations
def gas(st,k):
    gaps=[b-a for a,b in zip(st,st[1:])]; g=len(gaps); best=1e18
    def comps(total,parts):
        if parts==1: yield (total,); return
        for i in range(total+1):
            for r in comps(total-i,parts-1): yield (i,)+r
    for c in comps(k,g): best=min(best,max(gp/(ci+1) for gp,ci in zip(gaps,c)))
    return best
for st,k,e in (([1,2,3,4,5,6,7,8,9,10],9,0.5),([23,24,36,39,46,56,57,65,84,98],1,14.0),([0,10],0,10.0),([0,10],1,5.0)): assert abs(gas(st,k)-e)<1e-9,(st,k,gas(st,k))
# also the predicate-based version agrees on random small
def gas_bs(st,k):
    gaps=[b-a for a,b in zip(st,st[1:])]; lo,hi=0.0,max(gaps)
    for _ in range(100):
        d=(lo+hi)/2
        if sum(math.ceil(g/d)-1 for g in gaps)<=k: hi=d
        else: lo=d
    return hi
for _ in range(100):
    st=sorted(random.sample(range(0,30),random.randint(2,5))); k=random.randint(0,4)
    assert abs(gas(st,k)-gas_bs(st,k))<1e-6
print('ALL EXAMPLES OK')
