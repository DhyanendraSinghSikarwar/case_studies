# Runs every example printed in the Part 4 prompts against brute-force / independent reference code. Run: python3 -I check_examples.py
import sys, re, itertools, random, collections, queue
def ok(name, got, exp):
    assert got == exp, (name, got, exp)
# 1 valid parentheses: repeated removal reference
def vp(s):
    p=None
    while p!=s:
        p=s; s=s.replace('()','').replace('[]','').replace('{}','')
    return s==''
ok('vp',[vp(x) for x in ('()[]{}','(]','([{}])','((',']','([)]')],[True,False,True,False,False,False])
# 2 min stack: list scan reference
st=[];
def mn(): return min(st)
st+= [-2,0,-3]; r1=mn(); st.pop(); r2=st[-1]; r3=mn(); st+=[-2,-2]; st.pop(); r4=mn()
ok('minstack',[r1,r2,r3,r4],[-3,0,-2,-2])
# 3 queue via two stacks: reference deque
d=collections.deque(); d.append(1); d.append(2); a=d[0]; b=d.popleft(); c=not d; e=d.popleft(); f=not d
ok('q2s',[a,b,c,e,f],[1,1,False,2,True])
# 4 list vs deque
cmds=['push 1','push 2','pop','push 3','pop','pop']
def run(q,pop):
    out=[]
    for c in cmds:
        if c=='pop': out.append(pop(q))
        else: q.append(int(c.split()[1]))
    return out
ok('listdq',[run([],lambda q:q.pop(0)),run(collections.deque(),lambda q:q.popleft())],[[1,2,3]]*2)
# 5 NGE subset
def nge1(n1,n2): return [next((y for y in n2[n2.index(x)+1:] if y>x),-1) for x in n1]
ok('nge1',[nge1([4,1,2],[1,3,4,2]),nge1([2,4],[1,2,3,4])],[[-1,3,-1],[3,-1]])
# 6 RPN: Fraction-free recursive reference with truncation
def rpn(t):
    s=[]
    for x in t:
        if x in '+-*/' and len(x)==1:
            b=s.pop();a=s.pop()
            s.append(a+b if x=='+' else a-b if x=='-' else a*b if x=='*' else (abs(a)//abs(b))*(1 if (a<0)==(b<0) else -1))
        else: s.append(int(x))
    return s[0]
ok('rpn',[rpn(x) for x in (['2','1','+','3','*'],['4','13','5','/','+'],['10','6','9','3','+','-11','*','/','*','17','+','5','+'],['7','-2','/'])],[9,6,22,-3])
assert 7//-2==-4  # floor trap claimed in prompt
# 7 daily temperatures brute force
def dt(t): return [next((j-i for j in range(i+1,len(t)) if t[j]>t[i]),0) for i in range(len(t))]
ok('dt',[dt([73,74,75,71,69,72,76,73]),dt([30,40,50,60]),dt([30,60,90])],[[1,1,4,2,1,1,0,0],[1,1,1,0],[1,1,0]])
# 8 decode string: regex innermost expansion reference
def dec(s):
    while True:
        n=re.sub(r'(\d+)\[([a-z]*)\]',lambda m:m.group(2)*int(m.group(1)),s)
        if n==s: return s
        s=n
ok('dec',[dec('3[a]2[bc]'),dec('3[a2[c]]'),dec('2[abc]3[cd]ef'),dec('ab10[c]')],['aaabcbc','accaccacc','abcabccdcdcdef','ab'+'c'*10])
# 9 simplify path: posixpath.normpath-free reference via repeated rewrite
import posixpath
def sp(p):
    parts=[]
    for x in p.split('/'):
        if x in ('','.'): continue
        if x=='..':
            if parts: parts.pop()
        else: parts.append(x)
    return '/'+'/'.join(parts)
ok('sp',[sp(x) for x in ('/home/','/home//foo/','/a/./b/../../c/','/../','/.../a/../b/c/../d/./')],['/home','/home/foo','/c','/','/.../b/d'])
ok('sp-posix',[posixpath.normpath(x) for x in ('/home//foo/','/a/./b/../../c/','/../')],['/home/foo','/c','/'])
# 10 NGE circular brute force
def ngec(a):
    n=len(a); return [next((a[(i+k)%n] for k in range(1,n) if a[(i+k)%n]>a[i]),-1) for i in range(n)]
ok('ngec',[ngec([1,2,1]),ngec([1,2,3,4,3]),ngec([5,5])],[[2,-1,2],[2,3,4,-1,4],[-1,-1]])
# 11 calculator with parentheses: eval reference (python ints; only + - and parens, unary minus)
def ev(s): return eval(s)
ok('calc1',[ev('1 + 1'),ev(' 2-1 + 2 '),ev('(1+(4+5+2)-3)+(6+8)'),ev('-(2+3)'),ev('2-(5-6)')],[2,3,23,-5,3])
# 12 histogram brute force
def hist(h): return max([min(h[i:j+1])*(j-i+1) for i in range(len(h)) for j in range(i,len(h))])
ok('hist',[hist([2,1,5,6,2,3]),hist([2,4]),hist([1,1,1,1]),hist([0]),hist([6,2,5,4,5,1,6])],[10,4,4,0,12])
# 13 rain water: column formula
def rain(h): return sum(max(0,min(max(h[:i+1]),max(h[i:]))-h[i]) for i in range(len(h)))
ok('rain',[rain([0,1,0,2,1,0,1,3,2,1,2,1]),rain([4,2,0,3,2,5]),rain([3,0,2]),rain([1,2,3])],[6,9,2,0])
# 14 stack via queues: reference list
l=[1,2]; t1=l[-1]; p1=l.pop(); e1=not l; p2=l.pop(); e2=not l
ok('sq',[t1,p1,e1,p2,e2],[2,2,False,1,True])
# 15 backspace compare
def bs(s):
    o=''
    for c in s: o=o[:-1] if c=='#' else o+c
    return o
ok('bsc',[bs(a)==bs(b) for a,b in (('ab#c','ad#c'),('ab##','c#d#'),('a#c','b'),('a##c','#a#c'))],[True,True,False,True])
# 16 adjacent duplicates: regex / repeated scan reference
def rd(s):
    p=None
    while p!=s:
        p=s; s=re.sub(r'(.)\1','',s,count=1)
    return s
def rdk(s,k):
    p=None
    while p!=s:
        p=s; s=re.sub(r'(.)\1{%d}'%(k-1),'',s,count=1)
    return s
ok('rd',[rd('abbaca'),rd('azxxzy'),rdk('deeedbbcccbdaa',3),rdk('pbbcggttciiippooaais',2)],['ca','ay','aa','ps'])
# 17 min remove parens (index-matching reference using counters from both sides)
def mr(s):
    drop=set(); bal=0
    for i,c in enumerate(s):
        if c=='(': bal+=1
        elif c==')':
            if bal==0: drop.add(i)
            else: bal-=1
    # unmatched openers: the last `bal` unmatched '(' found by right-to-left scan
    need=bal
    for i in range(len(s)-1,-1,-1):
        if need and s[i]=='(' and i not in drop:
            # only unmatched ones: recompute using stack matching
            pass
    st=[];dr=set()
    for i,c in enumerate(s):
        if c=='(': st.append(i)
        elif c==')':
            if st: st.pop()
            else: dr.add(i)
    dr|=set(st)
    return ''.join(c for i,c in enumerate(s) if i not in dr)
def valid(s):
    b=0
    for c in s:
        b+= c=='('; b-= c==')'
        if b<0: return False
    return b==0
def mr_min(s):  # brute: max-length valid subsequence by deletion of parens only
    idx=[i for i,c in enumerate(s) if c in '()']
    for r in range(len(idx)+1):
        res=set()
        for dele in itertools.combinations(idx,r):
            t=''.join(c for i,c in enumerate(s) if i not in dele)
            if valid(t): res.add(t)
        if res: return r,res
for s,e in (('lee(t(c)o)de)','lee(t(c)o)de'),('a)b(c)d','ab(c)d'),('))((',''),('(a(b(c)d)','a(b(c)d)')):
    ok('mr',mr(s),e); r,res=mr_min(s); assert mr(s) in res and len(s)-len(e)==r,(s,res)
# 18 stock span brute force
def span(p): return [next((i-j for j in range(i,-1,-1) if p[j]>p[i]),i+1) for i in range(len(p))]
ok('span',[span([100,80,60,70,60,75,85]),span([7,7,7])],[[1,1,1,2,1,4,6],[1,2,3]])
# 19 prev/next smaller
def pn(a):
    n=len(a)
    return ([next((j for j in range(i-1,-1,-1) if a[j]<a[i]),-1) for i in range(n)],[next((j for j in range(i+1,n) if a[j]<a[i]),n) for i in range(n)])
ok('pn',[pn([4,5,2,10,8]),pn([3,3,3])],[([-1,0,-1,2,2],[2,2,5,4,5]),([-1,-1,-1],[3,3,3])])
# 20 remove k digits brute force
def rk(s,k):
    best=None
    for dele in itertools.combinations(range(len(s)),k):
        t=''.join(c for i,c in enumerate(s) if i not in dele)
        v=int(t) if t else 0
        best=v if best is None or v<best else best
    return str(best)
ok('rk',[rk('1432219',3),rk('10200',1),rk('10',2),rk('9',1),rk('112',1)],['1219','200','0','0','11'])
# 21 car fleet simulation (event based, exact fractions)
from fractions import Fraction
def fleets(target,pos,spd):
    cars=sorted(zip(pos,spd),reverse=True)
    # simulate: a car's effective arrival = max(own, arrival of car ahead)
    arr=[];ahead=Fraction(0);cnt=0
    for p,s in cars:
        t=Fraction(target-p,s)
        if t>ahead: cnt+=1; ahead=t
    return cnt
def fleets_sim(target,pos,spd):
    # time-stepped simulation (dt=1/1000, exact Fractions): a car never passes the one ahead; fleet = cars arriving together
    n=len(pos); order=sorted(range(n),key=lambda i:-pos[i])
    x={i:Fraction(pos[i]) for i in order}; arrive={}
    dt=Fraction(1,1000); t=Fraction(0)
    while len(arrive)<n:
        t+=dt
        for k,i in enumerate(order):
            if i in arrive: continue
            nx=x[i]+spd[i]*dt
            if k>0: nx=min(nx,x[order[k-1]])
            x[i]=nx
            if x[i]>=target: arrive[i]=t; x[i]=Fraction(target)
    return len({round(float(v),2) for v in arrive.values()})
ok('fleet',[fleets(12,[10,8,0,5,3],[2,4,1,1,3]),fleets(10,[3],[3]),fleets(100,[0,2,4],[4,2,1])],[3,1,1])
ok('fleet-sim',[fleets_sim(12,[10,8,0,5,3],[2,4,1,1,3]),fleets_sim(10,[3],[3]),fleets_sim(100,[0,2,4],[4,2,1])],[3,1,1])
# 22 circular queue: reference deque with capacity
class CQ:
    def __init__(s,k): s.k=k; s.d=collections.deque()
    def en(s,x):
        if len(s.d)==s.k: return False
        s.d.append(x); return True
    def de(s):
        if not s.d: return False
        s.d.popleft(); return True
    def front(s): return s.d[0] if s.d else -1
    def rear(s): return s.d[-1] if s.d else -1
q=CQ(3); r=[q.en(1),q.en(2),q.en(3),q.en(4),q.rear(),len(q.d)==q.k,q.de(),q.en(4),q.rear(),q.front()]
ok('cq',r,[True,True,True,False,3,True,True,True,4,2])
# 23 monotonic queue: reference list
buf=[]
buf+=[3,1]; a1=max(buf); buf+=[2]; buf.remove(3) if False else buf.pop(0); a2=max(buf); buf.pop(0); a3=max(buf); buf.append(5); a4=max(buf)
ok('mq',[a1,a2,a3,a4],[3,2,2,5])
b=[2,2]; b.pop(0); ok('mq-dup',max(b),2)
# 24 remove duplicate letters brute force
def rdl(s):
    k=len(set(s)); best=None
    for c in itertools.combinations(range(len(s)),k):
        t=''.join(s[i] for i in c)
        if len(set(t))==k and (best is None or t<best): best=t
    return best
ok('rdl',[rdl('bcabc'),rdl('cbacdcbc'),rdl('abacb'),rdl('a')],['abc','acdb','abc','a'])
# 25 longest valid parentheses brute force
def lvp(s):
    return max([j-i for i in range(len(s)) for j in range(i,len(s)+1) if valid(s[i:j])] or [0])
ok('lvp',[lvp('(()'),lvp(')()())'),lvp(''),lvp('()(())'),lvp('()(()')],[2,4,0,6,2])
# 26 maximal rectangle brute force
def mrect(m):
    R=len(m);C=len(m[0]);best=0
    for r1 in range(R):
        for r2 in range(r1,R):
            for c1 in range(C):
                for c2 in range(c1,C):
                    if all(m[r][c]=='1' for r in range(r1,r2+1) for c in range(c1,c2+1)):
                        best=max(best,(r2-r1+1)*(c2-c1+1))
    return best
ok('mrect',[mrect(['10100','10111','11111','10010']),mrect(['0']),mrect(['1']),mrect(['11','11'])],[6,0,1,4])
# 27 sum of subarray minimums brute force
def ssm(a): return sum(min(a[i:j+1]) for i in range(len(a)) for j in range(i,len(a)))%(10**9+7)
ok('ssm',[ssm([3,1,2,4]),ssm([11,81,94,43,3]),ssm([2,2,2])],[17,444,12])
# 28 recursion limit
def dsum(x,d=1): return sum(dsum(y,d+1) if isinstance(y,list) else y*d for y in x)
ok('dsum',[dsum([1,[4,[6]]]),dsum([[1,1],2,[1,1]])],[27,10])
chain=[7]
for _ in range(4999): chain=[chain]
assert sys.getrecursionlimit()==1000, sys.getrecursionlimit()
try: dsum(chain); raise SystemExit('expected RecursionError')
except RecursionError: pass
def dsum_it(x):
    tot=0; st=[(x,1)]
    while st:
        l,d=st.pop()
        for y in l:
            if isinstance(y,list): st.append((y,d+1))
            else: tot+=y*d
    return tot
ok('dsum-it',[dsum_it([1,[4,[6]]]),dsum_it([[1,1],2,[1,1]]),dsum_it(chain)],[27,10,35000])
# 29 BFS levels
g={'A':['B','C'],'B':['D'],'C':['D','E'],'D':['F'],'E':['F'],'F':[]}
dist={'A':0}; dq=collections.deque(['A']); lv=[]
while dq:
    lv.append([]) 
    for _ in range(len(dq)):
        u=dq.popleft(); lv[-1].append(u)
        for w in g[u]:
            if w not in dist: dist[w]=dist[u]+1; dq.append(w)
ok('bfs',(lv,dist['F']),([['A'],['B','C'],['D','E'],['F']],3))
#
log=[];res=[]
for t in (1,100,3001,3002):
    log.append(t); res.append(sum(1 for x in log if t-3000<=x<=t))
ok('recent',res,[1,2,3,3])
# 31 queue.Queue vs deque
qq=queue.Queue(maxsize=2); qq.put(1); qq.put(2)
try: qq.put_nowait(3); raise SystemExit('no Full')
except queue.Full: pass
ok('qget',qq.get(),1)
dd=collections.deque(maxlen=2)
for i in (1,2,3): dd.append(i)
ok('maxlen',list(dd),[2,3])
# 32 undo/redo and browser
def editor(cmds):
    txt=[];red=[];out=[]
    for c in cmds:
        if c.startswith('type'): txt.append(c.split()[1]); red.clear()
        elif c=='undo':
            if txt: red.append(txt.pop())
        elif c=='redo':
            if red: txt.append(red.pop())
        out.append(''.join(txt))
    return out
ok('editor',editor(['type a','type b','type c','undo','undo','redo','type d','redo','undo']),['a','ab','abc','ab','a','ab','abd','abd','ab'])
def browser(cmds):
    hist=[];i=-1;out=[]
    for c in cmds:
        if c.startswith('visit'): hist=hist[:i+1]+[c.split()[1]]; i+=1
        elif c=='back': i=max(0,i-1)
        elif c=='forward': i=min(len(hist)-1,i+1)
        out.append(hist[i])
    return out,hist[i]
ok('browser',browser(['visit x','visit y','visit z','back','back','forward','visit w','forward']),(['x','y','z','y','x','y','w','w'],'w'))
# 33 validate stack sequences brute force over all interleavings
def vss(pu,po):
    seen=set()
    def go(i,st,j):
        if (i,st,j) in seen: return False
        seen.add((i,st,j))
        if j==len(po): return True
        if st and st[-1]==po[j] and go(i,st[:-1],j+1): return True
        if i<len(pu) and go(i+1,st+(pu[i],),j): return True
        return False
    return go(0,(),0)
ok('vss',[vss([1,2,3,4,5],[4,5,3,2,1]),vss([1,2,3,4,5],[4,3,5,1,2])],[True,False])
# 34 exclusive time per time unit
def excl(n,logs):
    ans=[0]*n; stack=[]; 
    ev=[]
    for l in logs:
        i,k,t=l.split(':'); ev.append((int(i),k,int(t)))
    T=max(t for _,_,t in ev)+1
    # build per-unit running function
    start=[0]*(T+2); 
    cur=[]; idx=0
    for u in range(T):
        while idx<len(ev) and ev[idx][2]==u and ev[idx][1]=='start':
            cur.append(ev[idx][0]); idx+=1
        if cur: ans[cur[-1]]+=1
        while idx<len(ev) and ev[idx][2]==u and ev[idx][1]=='end':
            cur.pop(); idx+=1
    return ans
ok('excl',[excl(2,['0:start:0','1:start:2','1:end:5','0:end:6']),excl(1,['0:start:0','0:start:2','0:end:5','0:start:6','0:end:6','0:end:7'])],[[3,4],[8]])
# 35 jump game VI O(nk) DP
def jg(a,k):
    n=len(a); dp=[None]*n; dp[0]=a[0]
    for i in range(1,n): dp[i]=a[i]+max(dp[max(0,i-k):i])
    return dp[-1]
ok('jg',[jg([1,-1,-2,4,-7,3],2),jg([10,-5,-2,4,0,3],3),jg([1,-5,-20,4,-1,3,-6,-3],2)],[7,17,0])
# 36 circular deque: reference deque
class CD(CQ):
    def il(s,x):
        if len(s.d)==s.k: return False
        s.d.append(x); return True
    def ifr(s,x):
        if len(s.d)==s.k: return False
        s.d.appendleft(x); return True
    def dl(s):
        if not s.d: return False
        s.d.pop(); return True
q=CD(3); r=[q.il(1),q.il(2),q.ifr(3),q.ifr(4),q.rear(),len(q.d)==3,q.dl(),q.ifr(4),q.front()]
ok('cd',r,[True,True,True,False,2,True,True,True,4])
# 37 calculator III: eval with truncating division
def tdiv(a,b): return int(a/b) if abs(a)<2**52 else None
def ev3(s):
    s=re.sub(r'(\d+)',r'I(\1)',s)
    class I(int):
        def __truediv__(a,b): return I(int(a)//int(b)) if (int(a)>=0)==(int(b)>0) else I(-(abs(int(a))//abs(int(b))))
    return int(eval(s,{'I':I}))
ok('calc3',[ev3('1+1'),ev3('6-4/2'),ev3('2*(5+5*2)/3+(6/2+8)'),ev3('(2+6*3+5-(3*14/7+2)*5)+3')],[2,4,21,-12])
# 38 max stack reference
ms=[5,1,5]; t1=ms[-1]
m=max(ms); i=len(ms)-1-ms[::-1].index(m); pm=ms.pop(i); t2=ms[-1]; pk=max(ms); p=ms.pop(); t3=ms[-1]
ok('maxstack',[t1,pm,t2,pk,p,t3],[5,5,1,5,1,5])
# 39 visible people brute force
def vis(h):
    n=len(h);out=[]
    for i in range(n):
        c=0
        for j in range(i+1,n):
            if all(h[k]<min(h[i],h[j]) for k in range(i+1,j)): c+=1
        out.append(c)
    return out
ok('vis',[vis([10,6,8,5,11,9]),vis([5,1,2,3,10])],[[3,1,2,1,1,0],[4,1,1,1,0]])
# 40 132 pattern brute force
def p132(a): return any(a[i]<a[k]<a[j] for i in range(len(a)) for j in range(i+1,len(a)) for k in range(j+1,len(a)))
ok('132',[p132([1,2,3,4]),p132([3,1,4,2]),p132([-1,3,2,0])],[False,True,True])
# asteroid brute force: repeated leftmost-collision simulation
def ast(a):
    a=list(a)
    while True:
        for i in range(len(a)-1):
            if a[i]>0 and a[i+1]<0:
                x,y=a[i],-a[i+1]
                a[i:i+2]=[] if x==y else [a[i]] if x>y else [a[i+1]]
                break
        else: return a
ok('ast',[ast(x) for x in ([5,10,-5],[8,-8],[10,2,-5],[-2,-1,1,2],[3,5,-6,2,-1,4])],[[5,10],[],[10],[-2,-1,1,2],[-6,2,4]])
print('all examples OK')
