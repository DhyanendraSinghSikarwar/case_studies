# Runs every example printed in the Part 6 prompts against node-based reference solutions AND independent brute-force code on Python lists,
# plus exhaustive / randomised checks of the claims made in the prompts. Run: python3 -I check_examples.py
import heapq, itertools, random, sys, math
from collections import OrderedDict
random.seed(6)
def ok(name, got, exp): assert got == exp, (name, got, exp)

class ListNode:
    __slots__=('val','next')
    def __init__(s,val=0,next=None): s.val=val; s.next=next
def build(arr,pos=-1):
    d=ListNode(); t=d; nodes=[]
    for v in arr:
        t.next=ListNode(v); t=t.next; nodes.append(t)
    if pos!=-1: t.next=nodes[pos]
    return d.next,nodes
def H(arr): return build(arr)[0]
def arr(h,cap=10**6):
    out=[]
    while h is not None:
        out.append(h.val); h=h.next
        assert len(out)<=cap,'cycle'
    return out
def ids(h):
    out=[]
    while h is not None: out.append(id(h)); h=h.next; assert len(out)<10**6
    return out
def acyclic(h):
    s=f=h
    while f and f.next:
        s=s.next; f=f.next.next
        if s is f: return False
    return True
def inplace(fn,a,*args,exp=None):
    """run fn on fresh list; result must hold exactly the same node objects (as a subset when stated) and match exp values"""
    h,nodes=build(a); before=set(id(n) for n in nodes)
    r=fn(h,*args); assert acyclic(r)
    got=arr(r)
    if exp is not None: assert got==exp,(fn.__name__,a,args,got,exp)
    assert set(ids(r))<=before and len(set(ids(r)))==len(ids(r))
    return got

# ---------------- reference node-based solvers ----------------
def rev_it(h):
    p=None
    while h: n=h.next; h.next=p; p=h; h=n
    return p
def rev_rec(h):
    if not h or not h.next: return h
    r=rev_rec(h.next); h.next.next=h; h.next=None; return r
def mid(h):
    s=f=h
    while f and f.next: s=s.next; f=f.next.next
    return s
def merge2(a,b):
    d=t=ListNode()
    while a and b:
        if b.val<a.val: t.next=b; b=b.next
        else: t.next=a; a=a.next
        t=t.next
    t.next=a or b; return d.next
def has_cycle(h):
    s=f=h
    while f and f.next:
        s=s.next; f=f.next.next
        if s is f: return True
    return False
def has_cycle_set(h):
    seen=set()
    while h:
        if h in seen: return True
        seen.add(h); h=h.next
    return False
def remove_nth(h,n):
    d=ListNode(0,h); f=s=d
    for _ in range(n): f=f.next
    while f.next: f=f.next; s=s.next
    s.next=s.next.next; return d.next
def cycle_start(h):
    s=f=h
    while f and f.next:
        s=s.next; f=f.next.next
        if s is f:
            p=h
            while p is not s: p=p.next; s=s.next
            return p
    return None
def pal(h):
    if not h: return True
    m=mid(h); r=rev_it(m); a,b=h,r; res=True
    while b:
        if a.val!=b.val: res=False
        a=a.next; b=b.next
    rev_it(r)  # restore
    # restore link: first half tail still points at m? after reverse+restore the second half is back in order
    return res
def add_rev(a,b):
    d=t=ListNode(); c=0
    while a or b or c:
        s=c+(a.val if a else 0)+(b.val if b else 0); c,dg=divmod(s,10)
        t.next=ListNode(dg); t=t.next; a=a.next if a else None; b=b.next if b else None
    return d.next
def reorder(h):
    if not h or not h.next: return h
    s=f=h
    while f.next and f.next.next: s=s.next; f=f.next.next
    second=rev_it(s.next); s.next=None; a=h
    while second:
        an,bn=a.next,second.next; a.next=second; second.next=an; a=an; second=bn
    return h
def inter(a,b):
    p,q=a,b
    while p is not q:
        p=p.next if p else b; q=q.next if q else a
    return p
class RN:
    __slots__=('val','next','random')
    def __init__(s,v): s.val=v; s.next=None; s.random=None
def build_r(spec):
    ns=[RN(v) for v,_ in spec]
    for i,(v,r) in enumerate(spec):
        if i+1<len(ns): ns[i].next=ns[i+1]
        if r is not None: ns[i].random=ns[r]
    return (ns[0] if ns else None), ns
def spec_of(h):
    ns=[];p=h
    while p: ns.append(p); p=p.next
    ix={id(n):i for i,n in enumerate(ns)}
    return [[n.val, None if n.random is None else ix[id(n.random)]] for n in ns]
def copy_map(h):
    m={None:None}; p=h
    while p: m[p]=RN(p.val); p=p.next
    p=h
    while p: m[p].next=m[p.next]; m[p].random=m[p.random]; p=p.next
    return m[h]
def copy_o1(h):
    if not h: return None
    p=h
    while p: c=RN(p.val); c.next=p.next; p.next=c; p=c.next
    p=h
    while p: p.next.random=p.random.next if p.random else None; p=p.next.next
    p=h; ch=h.next
    while p:
        c=p.next; p.next=c.next; c.next=c.next.next if c.next else None; p=p.next
    return ch
def merge_k_heap(ls):
    hp=[(l.val,i,l) for i,l in enumerate(ls) if l]; heapq.heapify(hp); d=t=ListNode()
    while hp:
        _,i,n=heapq.heappop(hp); t.next=n; t=n
        if n.next: heapq.heappush(hp,(n.next.val,i,n.next))
    t.next=None
    return d.next
def merge_k_dc(ls):
    if not ls: return None
    while len(ls)>1: ls=[merge2(ls[i],ls[i+1]) if i+1<len(ls) else ls[i] for i in range(0,len(ls),2)]
    return ls[0]
def rev_k(h,k):
    d=ListNode(0,h); gp=d
    while True:
        e=gp
        for _ in range(k):
            e=e.next
            if not e: return d.next
        nxt=e.next; prev=nxt; cur=gp.next
        for _ in range(k): n=cur.next; cur.next=prev; prev=cur; cur=n
        first=gp.next; gp.next=prev; gp=first
def del_node(node): node.val=node.next.val; node.next=node.next.next
def dedup_sorted(h):
    c=h
    while c and c.next:
        if c.val==c.next.val: c.next=c.next.next
        else: c=c.next
    return h
def remove_val(h,v):
    d=ListNode(0,h); p=d
    while p.next:
        if p.next.val==v: p.next=p.next.next
        else: p=p.next
    return d.next
def rev_between(h,l,r):
    d=ListNode(0,h); p=d
    for _ in range(l-1): p=p.next
    cur=p.next
    for _ in range(r-l): n=cur.next; cur.next=n.next; n.next=p.next; p.next=n
    return d.next
def swap_pairs(h):
    d=ListNode(0,h); p=d
    while p.next and p.next.next:
        a=p.next; b=a.next; a.next=b.next; b.next=a; p.next=b; p=a
    return d.next
def odd_even(h):
    if not h: return h
    o=h; e=h.next; eh=e
    while e and e.next: o.next=e.next; o=o.next; e.next=o.next; e=e.next
    o.next=eh; return h
def partition(h,x):
    a=ListNode(); b=ListNode(); ta,tb=a,b
    while h:
        if h.val<x: ta.next=h; ta=h
        else: tb.next=h; tb=h
        h=h.next
    tb.next=None; ta.next=b.next; return a.next
def rotate(h,k):
    if not h or not h.next: return h
    n=1; t=h
    while t.next: t=t.next; n+=1
    k%=n
    if k==0: return h
    p=h
    for _ in range(n-k-1): p=p.next
    nh=p.next; p.next=None; t.next=h; return nh
def add_fwd(a,b):
    sa=[];sb=[]
    while a: sa.append(a.val); a=a.next
    while b: sb.append(b.val); b=b.next
    head=None; c=0
    while sa or sb or c:
        s=c+(sa.pop() if sa else 0)+(sb.pop() if sb else 0); c,dg=divmod(s,10)
        head=ListNode(dg,head)
    return head
def dedup_all(h):
    d=ListNode(0,h); p=d
    while p.next:
        c=p.next
        if c.next and c.next.val==c.val:
            while c.next and c.next.val==c.val: c=c.next
            p.next=c.next
        else: p=p.next
    return d.next
def sort_bu(h):
    n=0;p=h
    while p: n+=1; p=p.next
    d=ListNode(0,h); size=1
    def split(h,s):
        for _ in range(s-1):
            if not h: break
            h=h.next
        if not h: return None
        r=h.next; h.next=None; return r
    def merge(a,b):
        t0=t=ListNode()
        while a and b:
            if b.val<a.val: t.next=b; b=b.next
            else: t.next=a; a=a.next
            t=t.next
        t.next=a or b
        while t.next: t=t.next
        return t0.next,t
    while size<n:
        cur=d.next; tail=d
        while cur:
            l=cur; r=split(l,size); cur=split(r,size)
            m,t=merge(l,r); tail.next=m; tail=t
        size*=2
    return d.next
def sort_td(h):
    if not h or not h.next: return h
    m=mid(h); s=h
    while s.next is not m: s=s.next   # node before second middle
    s.next=None
    return merge2(sort_td(h),sort_td(m))
def dedup_unsorted(h):
    seen=set(); d=ListNode(0,h); p=d
    while p.next:
        if p.next.val in seen: p.next=p.next.next
        else: seen.add(p.next.val); p=p.next
    return d.next
def insertion_sort(h):
    d=ListNode()
    while h:
        n=h.next; p=d
        while p.next and p.next.val<=h.val: p=p.next
        h.next=p.next; p.next=h; h=n
    return d.next
def cyc_mu_lam(h):
    s=f=h
    if not h: return (0,0)
    while f and f.next:
        s=s.next; f=f.next.next
        if s is f: break
    else:
        n=0
        while h: n+=1; h=h.next
        return (n,0)
    lam=1; p=s.next
    while p is not s: p=p.next; lam+=1
    mu=0; a=h; b=s
    while a is not b: a=a.next; b=b.next; mu+=1
    return (mu,lam)
def break_cycle(h):
    st=cycle_start(h)
    if st is None: return None
    p=st
    while p.next is not st: p=p.next
    p.next=None; return p

# ---------------- brute force on python lists ----------------
def nodes_of(h): 
    out=[]
    while h: out.append(h); h=h.next
    return out

# ===== Q1 reverse =====
for f in (rev_it,rev_rec):
    for a,e in (([1,2,3,4,5],[5,4,3,2,1]),([1,2],[2,1]),([7],[7]),([],[])): inplace(f,a,exp=e)
# ===== Q2 middle
for a,e in (([1,2,3,4,5],[3,4,5]),([1,2,3,4,5,6],[4,5,6]),([1],[1]),([1,2],[2])):
    h,ns=build(a); m=mid(h); assert m is ns[len(a)//2]; ok('mid',arr(m),e)
# ===== Q3 merge (stable, identity)
for a,b,e in (([1,2,4],[1,3,4],[1,1,2,3,4,4]),([],[],[]),([],[0],[0]),([2,5],[1],[1,2,5])):
    ha,na=build(a); hb,nb=build(b); r=merge2(ha,hb); ok('merge',arr(r),e)
    assert set(ids(r))==set(map(id,na+nb))
ha,na=build([1,2,4]); hb,nb=build([1,3,4]); r=merge2(ha,hb); assert ids(r)[:2]==[id(na[0]),id(nb[0])]
# ===== Q4 cycle detect
for a,pos,e in (([3,2,0,-4],1,True),([1,2],0,True),([1],-1,False),([1,1,1],-1,False),([],-1,False)):
    h,_=build(a,pos); ok('cyc',has_cycle(h),e); ok('cycset',has_cycle_set(h),e)
# value-set would be wrong with repeated values:
h,_=build([1,1,1]); assert len({n.val for n in nodes_of(h)})<3
# ===== Q5 remove nth
for a,n,e in (([1,2,3,4,5],2,[1,2,3,5]),([1],1,[]),([1,2],1,[1]),([1,2],2,[2])):
    ok('rmn',inplace(remove_nth,a,n),e)
    ok('rmn-brute',a[:len(a)-n]+a[len(a)-n+1:],e)
# ===== Q6 cycle start + proof claim (exhaustive)
for a,pos in (([3,2,0,-4],1),([1,2],0),([1],0),([1,2,3],-1)):
    h,ns=build(a,pos); r=cycle_start(h); assert r is (ns[pos] if pos>=0 else None)
steps_ok=0
for mu in range(0,16):
    for lam in range(1,16):
        a=list(range(mu+lam)); h,ns=build(a,mu)
        s=f=h; t=0
        while True:
            s=s.next; f=f.next.next; t+=1
            if s is f: break
        t_exp=next(x for x in range(1,10**4) if x%lam==0 and x>=mu)
        assert t==t_exp,(mu,lam,t,t_exp)
        k=(t-mu)%lam; assert (mu+k)%lam==0 and s is ns[mu+k if mu+k<mu+lam else mu+k-lam]
        assert cycle_start(h) is ns[mu]; steps_ok+=1
# when mu=0 the smallest multiple >=mu with t>=1: prompt says smallest multiple of lambda with t>=mu; mu=0 gives t=lambda (since t>=1) -- covered by test above using range from 1
# ===== Q7 palindrome
for a,e in (([1,2,2,1],True),([1,2,3,2,1],True),([1,2],False),([1],True),([1,0,0],False)):
    h,ns=build(a); before=ids(h); ok('pal',pal(h),e); assert ids(h)==before and arr(h)==a
    ok('pal-b',a==a[::-1],e)
# ===== Q8 add reverse
for a,b,e in (([2,4,3],[5,6,4],[7,0,8]),([0],[0],[0]),([9,9,9,9],[1],[0,0,0,0,1]),([5],[5],[0,1])):
    ok('addrev',arr(add_rev(H(a),H(b))),e)
assert 342+465==807
# ===== Q9 reorder
def reorder_brute(a):
    out=[];i,j=0,len(a)-1
    while i<=j:
        out.append(a[i]); i+=1
        if i<=j: out.append(a[j]); j-=1
    return out
for a,e in (([1,2,3,4],[1,4,2,3]),([1,2,3,4,5],[1,5,2,4,3]),([1],[1]),([1,2],[1,2])):
    ok('reo',inplace(reorder,a,exp=e),e); ok('reo-b',reorder_brute(a),e)
# ===== Q10 intersection
def mk_inter(pa,pb,sh):
    s,sn=build(sh); 
    def pre(p):
        d=t=ListNode()
        for v in p: t.next=ListNode(v); t=t.next
        t.next=s; return d.next
    return pre(pa),pre(pb),s
for pa,pb,sh,e in (([4,1],[5,6,1],[8,4,5],8),([1,9,1],[3],[2,4],2),([2,6,4],[1,5],[],None),([],[],[7],7)):
    a,b,s=mk_inter(pa,pb,sh); r=inter(a,b); assert r is s; ok('inter',None if r is None else r.val,e)
# differing-length, equal-value no-intersection: val compare would be wrong
a=H([1,2]); b=H([1,2]); assert inter(a,b) is None
# ===== Q11 copy random (hash map)
for spec in ([[7,None],[13,0],[11,4],[10,2],[1,0]],[[1,1],[2,1]],[]):
    h,ns=build_r(spec); c=copy_map(h); ok('cp',spec_of(c),spec)
    orig={id(n) for n in ns}; assert all(id(n) not in orig for n in nodes_of(c))
    h2,ns2=build_r(spec); c2=copy_o1(h2); ok('cp2',spec_of(c2),spec); ok('cp2-input',spec_of(h2),spec)
    assert {id(n) for n in nodes_of(h2)}=={id(n) for n in ns2} and not ({id(n) for n in nodes_of(c2)}&{id(n) for n in ns2})
h,ns=build_r([[5,0]]); c=copy_o1(h); assert c.random is c and c is not h and h.random is h and h.next is None and c.next is None
# ===== Q12 merge k
for lists,e in (([[1,4,5],[1,3,4],[2,6]],[1,1,2,3,4,4,5,6]),([],[]),([[]],[]),([[],[2],[]],[2])):
    for f in (merge_k_heap,merge_k_dc):
        hs=[build(l) for l in lists]; ns=[n for _,n in hs]; r=f([h for h,_ in hs]); ok('mk',arr(r),e)
        assert sorted(ids(r))==sorted(id(x) for n in ns for x in n)
# stability: ties keep lower list index
for f in (merge_k_heap,merge_k_dc):
    hs=[build([1,1]),build([1])]; r=f([h for h,_ in hs]); assert ids(r)[:2]==[id(hs[0][1][0]),id(hs[0][1][1])] or ids(r)[0]==id(hs[0][1][0])
    # exact stable expectation: all list0 ones first? merge by (val, list idx): 1(l0),1(l0 second),1(l1) -> heap yields l0[0], then l0[1] (idx0) before l1[0]
    assert ids(r)==[id(hs[0][1][0]),id(hs[0][1][1]),id(hs[1][1][0])],f.__name__
# ListNode not orderable
try: ListNode(1)<ListNode(2); assert False
except TypeError: pass
# ===== Q13 reverse k group
def revk_brute(a,k):
    out=[]
    for i in range(0,len(a),k):
        g=a[i:i+k]; out+= g[::-1] if len(g)==k else g
    return out
for a,k,e in (([1,2,3,4,5],2,[2,1,4,3,5]),([1,2,3,4,5],3,[3,2,1,4,5]),([1,2,3],1,[1,2,3]),([1,2,3,4],4,[4,3,2,1])):
    ok('rk',inplace(rev_k,a,k),e); ok('rkb',revk_brute(a,k),e)
# ===== Q14 delete node
for a,v,e in (([4,5,1,9],5,[4,1,9]),([4,5,1,9],1,[4,5,9]),([1,2],1,[2]),([0,1,2,3],0,[1,2,3])):
    h,ns=build(a); n=next(x for x in ns if x.val==v); del_node(n); ok('del',arr(h),e)
# ===== Q15 dedup sorted
for a,e in (([1,1,2],[1,2]),([1,1,2,3,3],[1,2,3]),([5,5,5],[5]),([],[]),([1,2,3],[1,2,3])):
    ok('dd',inplace(dedup_sorted,a,exp=e),e); ok('ddb',sorted(set(a)),e)
# ===== Q16 remove val
for a,v,e in (([1,2,6,3,4,5,6],6,[1,2,3,4,5]),([],1,[]),([7,7,7],7,[]),([1,2],3,[1,2]),([6,1],6,[1])):
    ok('rv',inplace(remove_val,a,v),e); ok('rvb',[x for x in a if x!=v],e)
# ===== Q17 python specifics
def from_array(a): return build(a)[0]
def to_array(h): return arr(h)
def show(h):
    if h is None: return 'None'
    idx={};parts=[];p=h;i=0
    while p is not None:
        if id(p) in idx: return ' -> '.join(parts)+f' -> (cycle to index {idx[id(p)]})'
        idx[id(p)]=i; parts.append(str(p.val)); p=p.next; i+=1
    return ' -> '.join(parts)+' -> None'
ok('show1',show(H([1,2,3])),'1 -> 2 -> 3 -> None'); ok('show2',show(None),'None')
ok('show3',show(build([1,2,3],1)[0]),'1 -> 2 -> 3 -> (cycle to index 1)'); ok('show4',to_array(from_array([4,5])),[4,5])
x,y=ListNode(1),ListNode(1); assert (x==y) is False and (x is y) is False and (x==x)
assert not hasattr(x,'__dict__')
try: x.extra=1; assert False
except AttributeError: pass
class Plain:
    def __init__(s): s.val=1; s.next=None
assert hasattr(Plain(),'__dict__')
# a naive `while node:` print on a cycle never ends: demonstrated by step cap
def naive(h,cap=1000):
    c=0
    while h: h=h.next; c+=1
    # unreachable on cycle
    return c
h,_=build([1,2,3],1); p=h; c=0
while p and c<10**4: p=p.next; c+=1
assert c==10**4  # still going after 10^4 steps
# ===== Q18 reverse between
for a,l,r,e in (([1,2,3,4,5],2,4,[1,4,3,2,5]),([5],1,1,[5]),([3,5],1,2,[5,3]),([1,2,3],1,3,[3,2,1]),([1,2,3],2,2,[1,2,3])):
    ok('rb',inplace(rev_between,a,l,r),e); ok('rbb',a[:l-1]+a[l-1:r][::-1]+a[r:],e)
# ===== Q19 swap pairs
def swp(a): 
    o=a[:]
    for i in range(0,len(o)-1,2): o[i],o[i+1]=o[i+1],o[i]
    return o
for a,e in (([1,2,3,4],[2,1,4,3]),([1,2,3],[2,1,3]),([1],[1]),([],[]),([1,2],[2,1])):
    ok('sp',inplace(swap_pairs,a,exp=e),e); ok('spb',swp(a),e)
# ===== Q20 odd-even
for a,e in (([1,2,3,4,5],[1,3,5,2,4]),([2,1,3,5,6,4,7],[2,3,6,7,1,5,4]),([1],[1]),([1,2],[1,2]),([],[])):
    ok('oe',inplace(odd_even,a,exp=e),e); ok('oeb',a[0::2]+a[1::2],e)
# ===== Q21 partition
for a,x,e in (([1,4,3,2,5,2],3,[1,2,2,4,3,5]),([2,1],2,[1,2]),([],0,[]),([3,3],3,[3,3]),([1,2,3],4,[1,2,3])):
    ok('pt',inplace(partition,a,x),e); ok('ptb',[v for v in a if v<x]+[v for v in a if v>=x],e)
# ===== Q22 rotate
for a,k,e in (([1,2,3,4,5],2,[4,5,1,2,3]),([0,1,2],4,[2,0,1]),([1],99,[1]),([1,2],2,[1,2]),([],3,[]),([1,2,3],2000000000,[2,3,1])):
    ok('rot',inplace(rotate,a,k),e)
    n=len(a); kk=k%n if n else 0; ok('rotb',a[n-kk:]+a[:n-kk] if n else [],e)
# ===== Q23 add fwd
for a,b,e in (([7,2,4,3],[5,6,4],[7,8,0,7]),([2,4,3],[5,6,4],[8,0,7]),([0],[0],[0]),([9,9],[1],[1,0,0])):
    ha,_=build(a); hb,_=build(b); r=add_fwd(ha,hb); ok('af',arr(r),e)
    assert arr(ha)==a and arr(hb)==b
    ok('afb',[int(c) for c in str(int(''.join(map(str,a)))+int(''.join(map(str,b))))],e)
assert 7243+564==7807
# ===== Q24 dedup all
def dall(a):
    from collections import Counter
    c=Counter(a); return [v for v in a if c[v]==1]
for a,e in (([1,2,3,3,4,4,5],[1,2,5]),([1,1,1,2,3],[2,3]),([1,1],[]),([1,2,3],[1,2,3]),([],[])):
    ok('da',inplace(dedup_all,a,exp=e),e); ok('dab',dall(a),e)
# ===== Q25 sort
for f in (sort_bu,sort_td):
    for a,e in (([4,2,1,3],[1,2,3,4]),([-1,5,3,4,0],[-1,0,3,4,5]),([],[]),([2,2,1,1],[1,1,2,2]),([1],[1])):
        ok('sort',inplace(f,a,exp=e),e)
# stability by identity
for f in (sort_bu,sort_td):
    for _ in range(300):
        n=random.randint(0,40); a=[random.randint(0,5) for _ in range(n)]
        h,ns=build(a); order=sorted(range(n),key=lambda i:a[i]); r=f(h); assert ids(r)==[id(ns[i]) for i in order]
# ===== Q26 recursion
import sys as _s
assert _s.getrecursionlimit()==1000
r=rev_rec(H(list(range(100)))); ok('rec100',arr(r),list(range(99,-1,-1)))
try: rev_rec(H(list(range(2000)))); assert False
except RecursionError: pass
ok('it2000',arr(rev_it(H(list(range(2000))))),list(range(1999,-1,-1)))
big=H(list(range(10**5))); ok('it1e5',arr(rev_it(big))[:3],[99999,99998,99997])
ok('rec5',arr(rev_rec(H([1,2,3,4,5]))),[5,4,3,2,1])
# ===== Q27 dedup unsorted
def dun(a):
    seen=set();o=[]
    for v in a:
        if v not in seen: seen.add(v); o.append(v)
    return o
for a,e in (([1,2,1,3,2,4],[1,2,3,4]),([5,5,5],[5]),([],[]),([3,1,2],[3,1,2]),([2,1,2,1],[2,1])):
    ok('du',inplace(dedup_unsorted,a,exp=e),e); ok('dub',dun(a),e)
# ===== Q28 insertion sort
for a,e in (([4,2,1,3],[1,2,3,4]),([-1,5,3,4,0],[-1,0,3,4,5]),([],[]),([2,2,1],[1,2,2]),([1,2,3],[1,2,3])):
    ok('is',inplace(insertion_sort,a,exp=e),e)
for _ in range(300):
    n=random.randint(0,30); a=[random.randint(0,4) for _ in range(n)]; h,ns=build(a); order=sorted(range(n),key=lambda i:a[i]); assert ids(insertion_sort(h))==[id(ns[i]) for i in order]
# ===== Q29 doubly linked list with sentinels
class DN:
    __slots__=('val','prev','next')
    def __init__(s,v=None): s.val=v; s.prev=s.next=None
class DLL:
    def __init__(s): s.head=DN(); s.tail=DN(); s.head.next=s.tail; s.tail.prev=s.head
    def _ins(s,a,v): n=DN(v); b=a.next; n.prev=a; n.next=b; a.next=n; b.prev=n; return n
    def add_first(s,v): return s._ins(s.head,v)
    def add_last(s,v): return s._ins(s.tail.prev,v)
    def remove(s,n): n.prev.next=n.next; n.next.prev=n.prev; return n.val
    def pop_first(s): return None if s.head.next is s.tail else s.remove(s.head.next)
    def pop_last(s): return None if s.tail.prev is s.head else s.remove(s.tail.prev)
    def to_array(s):
        o=[];p=s.head.next
        while p is not s.tail: o.append(p.val); p=p.next
        b=[];p=s.tail.prev
        while p is not s.head: b.append(p.val); p=p.prev
        assert b==o[::-1]; return o
d=DLL(); d.add_last(1); d.add_last(2); d.add_first(0); ok('dll1',d.to_array(),[0,1,2])
ok('dll2',d.pop_last(),2); ok('dll3',d.to_array(),[0,1]); ok('dll4',d.pop_first(),0); ok('dll5',d.to_array(),[1])
d.pop_first(); ok('dll6',d.to_array(),[]); assert d.pop_first() is None and d.pop_last() is None
for _ in range(300):  # random cross-check with a list
    d=DLL(); L=[]
    for _ in range(40):
        op=random.randint(0,3); v=random.randint(0,9)
        if op==0: d.add_first(v); L.insert(0,v)
        elif op==1: d.add_last(v); L.append(v)
        elif op==2: ok('pf',d.pop_first(),L.pop(0) if L else None)
        else: ok('pl',d.pop_last(),L.pop() if L else None)
        ok('mirror',d.to_array(),L)
# ===== Q30 LRU concept (OrderedDict reference; and a dict + DLL implementation checked against it)
class LRU:
    def __init__(s,c): s.c=c; s.m={}; s.h=DN(); s.t=DN(); s.h.next=s.t; s.t.prev=s.h
    def _rm(s,n): n.prev.next=n.next; n.next.prev=n.prev
    def _front(s,n): n.next=s.h.next; n.prev=s.h; s.h.next.prev=n; s.h.next=n
    def get(s,k):
        if k not in s.m: return -1
        n=s.m[k]; s._rm(n); s._front(n); return n.val[1]
    def put(s,k,v):
        if k in s.m: n=s.m[k]; n.val=(k,v); s._rm(n); s._front(n); return
        if len(s.m)==s.c: n=s.t.prev; s._rm(n); del s.m[n.val[0]]
        n=DN((k,v)); s.m[k]=n; s._front(n)
class LRUref:
    def __init__(s,c): s.c=c; s.d=OrderedDict()
    def get(s,k):
        if k not in s.d: return -1
        s.d.move_to_end(k); return s.d[k]
    def put(s,k,v):
        if k in s.d: s.d.move_to_end(k)
        s.d[k]=v
        if len(s.d)>s.c: s.d.popitem(last=False)
for C in (LRU,LRUref):
    c=C(2); c.put(1,1); c.put(2,2); ok('l1',c.get(1),1); c.put(3,3); ok('l2',c.get(2),-1); c.put(4,4); ok('l3',c.get(1),-1); ok('l4',c.get(3),3); ok('l5',c.get(4),4)
for _ in range(300):
    cap=random.randint(1,4); a,b=LRU(cap),LRUref(cap)
    for _ in range(60):
        k=random.randint(0,6)
        if random.random()<.5: v=random.randint(0,99); a.put(k,v); b.put(k,v)
        else: ok('lru',a.get(k),b.get(k))
# ===== Q31 flatten multilevel
class MN:
    __slots__=('val','prev','next','child')
    def __init__(s,v): s.val=v; s.prev=s.next=s.child=None
def build_ml(spec):
    head=None; prev=None
    for it in spec:
        if isinstance(it,list):
            ch=build_ml(it); prev.child=ch
        else:
            n=MN(it); n.prev=prev
            if prev: prev.next=n
            else: head=n
            prev=n
    return head
def flatten(h):
    p=h
    while p:
        if p.child:
            c=p.child; t=c
            while t.next: t=t.next
            t.next=p.next
            if p.next: p.next.prev=t
            p.next=c; c.prev=p; p.child=None
        p=p.next
    return h
def flat_ref(spec):
    out=[]
    for it in spec:
        if isinstance(it,list): out+=flat_ref(it)
        else: out.append(it)
    return out
for spec,e in (([1,2,3,[7,8,[11,12],9],4],[1,2,3,7,8,11,12,9,4]),([1,[2],3],[1,2,3]),([],[]),([1,[2,[3]]],[1,2,3]),([1,2],[1,2])):
    h=build_ml(spec); r=flatten(h); o=[];p=r;last=None
    while p: assert p.child is None and p.prev is last; o.append(p.val); last=p; p=p.next
    ok('fl',o,e); ok('flr',flat_ref(spec),e)
# ===== Q32 mu lambda
for a,pos,e in (([3,2,0,-4],1,(1,3)),([1,2],0,(0,2)),([1],-1,(1,0)),([1,2,3],2,(2,1)),([],-1,(0,0))):
    h,_=build(a,pos); ok('ml',cyc_mu_lam(h),e)
# move-count bound: slow steps t, then lambda, then mu; verify t <= mu+lambda and total exactly formula; fast moves 2t
for mu in range(0,20):
    for lam in range(1,20):
        h,ns=build(list(range(mu+lam)),mu); ok('ml2',cyc_mu_lam(h),(mu,lam))
        t=next(x for x in range(1,10**4) if x%lam==0 and x>=mu); assert t<=mu+lam-1 or mu==0 or True
        assert t< mu+lam or (mu==0 and t==lam)   # t < mu + lambda  (t is the first multiple of lam that is >= mu, so t < mu+lam), t=lam when mu=0
# ===== Q33 break cycle
for a,pos,cut,e in (([3,2,0,-4],1,3,[3,2,0,-4]),([1,2],0,1,[1,2]),([1,2,3],2,2,[1,2,3]),([1],-1,None,[1])):
    h,ns=build(a,pos); b=set(map(id,ns)); r=break_cycle(h)
    ok('bc',None if r is None else ns.index(r),cut); assert acyclic(h); ok('bca',arr(h),e); assert set(ids(h))==b
# ===== Q34 copy O(1) covered above
# ===== Q35 harness claims
def inplace_check(fn,a):
    h,ns=build(a); before={id(n) for n in ns}; r=fn(h); return {id(n) for n in nodes_of(r)}==before
def rev_new(h):
    a=arr(h); d=None
    for v in a: d=ListNode(v,d)
    return d
assert inplace_check(rev_it,[1,2,3]) and not inplace_check(rev_new,[1,2,3]); ok('rn',arr(rev_new(H([1,2,3]))),[3,2,1])
def bad_rev(h):
    r=rev_it(h); t=r
    while t.next: t=t.next
    t.next=r; return r
r=bad_rev(H([1,2,3])); assert not acyclic(r)
# randomized node-vs-list cross-check of main solvers
for _ in range(500):
    n=random.randint(0,12); a=[random.randint(0,6) for _ in range(n)]
    ok('x1',inplace(rev_it,a),a[::-1]); ok('x2',inplace(rev_rec,a),a[::-1])
    k=random.randint(1,max(1,n)); ok('x3',inplace(rev_k,a,k),revk_brute(a,k))
    if n:
        m=random.randint(1,n); ok('x4',inplace(remove_nth,a,m),a[:n-m]+a[n-m+1:])
        l=random.randint(1,n); r2=random.randint(l,n); ok('x5',inplace(rev_between,a,l,r2),a[:l-1]+a[l-1:r2][::-1]+a[r2:])
    x=random.randint(0,7); ok('x6',inplace(partition,a,x),[v for v in a if v<x]+[v for v in a if v>=x])
    kk=random.randint(0,30); nn=len(a); ok('x7',inplace(rotate,a,kk),(a[nn-kk%nn:]+a[:nn-kk%nn]) if nn else [])
    ok('x8',inplace(odd_even,a),a[0::2]+a[1::2]); ok('x9',inplace(swap_pairs,a),swp(a)); ok('x10',inplace(reorder,a),reorder_brute(a))
    s=sorted(a); ok('x11',arr(dedup_sorted(H(s))),sorted(set(a))); ok('x12',arr(dedup_all(H(s))),dall(s)); ok('x13',inplace(dedup_unsorted,a),dun(a))
    ok('x14',inplace(sort_bu,a),s); ok('x15',inplace(sort_td,a),s); ok('x16',inplace(insertion_sort,a),s)
    A=sorted(random.randint(0,6) for _ in range(random.randint(0,8))); B=sorted(random.randint(0,6) for _ in range(random.randint(0,8)))
    ok('x17',arr(merge2(H(A),H(B))),sorted(A+B))
    pos=random.randint(-1,n-1) if n else -1; hh,ns=build(a,pos); ok('x19',has_cycle(hh),pos!=-1 and n>0); ok('x19b',has_cycle_set(hh),pos!=-1 and n>0)
    ok('x20',cycle_start(hh) is (ns[pos] if pos!=-1 else None),True)
    ok('x21',pal(H(a)),a==a[::-1])
    lists=[sorted(random.randint(0,9) for _ in range(random.randint(0,5))) for _ in range(random.randint(0,5))]
    for f in (merge_k_heap,merge_k_dc): ok('x22',arr(f([H(l) for l in lists])),sorted(sum(lists,[])))
    d1=[random.randint(0,9) for _ in range(random.randint(1,6))]; d2=[random.randint(0,9) for _ in range(random.randint(1,6))]
    sv=lambda x:int(''.join(map(str,x)))
    ok('x23',sv(arr(add_fwd(H(d1),H(d2)))),sv(d1)+sv(d2))
    ok('x24',sv(arr(add_rev(H(d1),H(d2)))[::-1]),sv(d1[::-1])+sv(d2[::-1]))
    spec=[[random.randint(0,9),random.choice([None]+list(range(n)))] for _ in range(n)]
    h,nsr=build_r(spec); ok('x25',spec_of(copy_map(h)),spec); h,nsr=build_r(spec); ok('x26',spec_of(copy_o1(h)),spec); ok('x27',spec_of(h),spec)
    pa=[random.randint(0,3) for _ in range(random.randint(0,4))]; pb=[random.randint(0,3) for _ in range(random.randint(0,4))]; sh=[random.randint(0,3) for _ in range(random.randint(0,4))]
    A_,B_,S_=mk_inter(pa,pb,sh); assert inter(A_,B_) is S_
print('ALL OK; floyd exhaustive pairs:',steps_ok)
