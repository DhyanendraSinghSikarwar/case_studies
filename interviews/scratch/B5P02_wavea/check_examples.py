# Runs every example printed in the Part 2 prompts against brute-force reference code. Run: python3 -I check_examples.py
from itertools import combinations
from collections import Counter
def ok(name, got, exp):
    assert got == exp, (name, got, exp)
def subs(n):
    for i in range(n):
        for j in range(i+1, n+1): yield i, j
def pal(s):
    t=[c.lower() for c in s if c.isalnum()]; return t==t[::-1]
ok('pal',[pal(x) for x in ("A man, a plan, a canal: Panama","race a car"," ","0P")],[True,False,True,False])
def ts2(a,t):
    return [(i,j) for i,j in combinations(range(len(a)),2) if a[i]+a[j]==t][0]
ok('ts2',ts2([2,7,11,15],9),(0,1)); ok('ts2b',ts2([2,3,4],6),(0,2)); ok('ts2c',ts2([-1,0],-1),(0,1))
def maxavg(a,k): return max(sum(a[i:i+k]) for i in range(len(a)-k+1))/k
ok('avg',maxavg([1,12,-5,-6,50,3],4),12.75); ok('avg2',maxavg([5],1),5.0)
def stock(p): return max([0]+[p[j]-p[i] for i,j in combinations(range(len(p)),2)])
ok('stock',stock([7,1,5,3,6,4]),5); ok('stock2',stock([7,6,4,3,1]),0)
ok('sq',sorted(x*x for x in [-4,-1,0,3,10]),[0,1,9,16,100]); ok('sq2',sorted(x*x for x in [-7,-3,2,3,11]),[4,9,9,49,121])
def lsr(s): return max([0]+[j-i for i,j in subs(len(s)) if len(set(s[i:j]))==j-i])
ok('lsr',[lsr(x) for x in ("abcabcbb","bbbbb","pwwkew","","abba")],[3,1,3,0,2])
def cont(h): return max(min(h[i],h[j])*(j-i) for i,j in combinations(range(len(h)),2))
ok('cont',cont([1,8,6,2,5,4,8,3,7]),49); ok('cont2',cont([1,1]),1)
def t3(a): return sorted(set(tuple(sorted(c)) for c in combinations(a,3) if sum(c)==0))
ok('3s',[list(x) for x in t3([-1,0,1,2,-1,-4])],[[-1,-1,2],[-1,0,1]]); ok('3s2',t3([0,0,0]),[(0,0,0)]); ok('3s3',t3([1,2,3]),[])
def perm(a,b): return any(Counter(b[i:i+len(a)])==Counter(a) for i in range(len(b)-len(a)+1))
ok('perm',perm("ab","eidbaooo"),True); ok('perm2',perm("ab","eidboaoo"),False)
def anag(s,p): return [i for i in range(len(s)-len(p)+1) if Counter(s[i:i+len(p)])==Counter(p)]
ok('an',anag("cbaebabacd","abc"),[0,6]); ok('an2',anag("abab","ab"),[0,1,2])
def crr(s,k): return max(j-i for i,j in subs(len(s)) if (j-i)-max(Counter(s[i:j]).values())<=k)
ok('crr',crr("AABABBA",1),4); ok('crr2',crr("ABAB",2),4)
def mss(t,a): return min([j-i for i,j in subs(len(a)) if sum(a[i:j])>=t] or [0])
ok('mss',[mss(7,[2,3,1,2,4,3]),mss(4,[1,4,4]),mss(11,[1]*8)],[2,1,0])
def trap(h): return sum(min(max(h[:i+1]),max(h[i:]))-h[i] for i in range(len(h)))
ok('trap',[trap([0,1,0,2,1,0,1,3,2,1,2,1]),trap([4,2,0,3,2,5])],[6,9])
def minw(s,t):
    best=""
    for i,j in subs(len(s)):
        if not Counter(t)-Counter(s[i:j]) and (best=="" or j-i<len(best)): best=s[i:j]
    return best
ok('minw',[minw("ADOBECODEBANC","ABC"),minw("a","aa"),minw("a","a")],["BANC","","a"])
def swm(a,k): return [max(a[i:i+k]) for i in range(len(a)-k+1)]
ok('swm',swm([1,3,-1,-3,5,3,6,7],3),[3,3,5,5,6,7]); ok('swm2',swm([1],1),[1])
def issub(s,t):
    it=iter(t); return all(c in it for c in s)
ok('issub',[issub("ace","abcde"),issub("aec","abcde"),issub("","x")],[True,False,True])
ok('inter',[2,2,4],[x for x in [2,2,4]]) 
def inter(a,b): return sorted((Counter(a)&Counter(b)).elements())
ok('inter',inter([1,2,2,3,4],[2,2,2,4,5]),[2,2,4]); ok('inter2',inter([1,3],[2,4]),[])
def pal2(s): return any(s[:i]+s[i+1:]==(s[:i]+s[i+1:])[::-1] for i in range(len(s))) or s==s[::-1]
ok('pal2',[pal2("aba"),pal2("abca"),pal2("abc")],[True,True,False])
def rd2(a):
    out=[]
    for x in a:
        if out.count(x)<2: out.append(x)
    return out
ok('rd2',rd2([1,1,1,2,2,3]),[1,1,2,2,3]); ok('rd2b',(len(rd2([0,0,1,1,1,1,2,3,3])),rd2([0,0,1,1,1,1,2,3,3])),(7,[0,0,1,1,2,3,3]))
def bs(s):
    o=[]
    for c in s:
        if c=='#': o and o.pop()
        else: o.append(c)
    return o
ok('bs',[bs("ab#c")==bs("ad#c"),bs("a#c")==bs("b"),bs("a##c")==bs("#a#c")],[True,False,True])
def ones3(a,k): return max(j-i for i,j in subs(len(a)) if a[i:j].count(0)<=k)
ok('o3',[ones3([1,1,1,0,0,0,1,1,1,1,0],2),ones3([0,0,1,1,0,0,1,1,1,0,1,1,0,0,0,1,1,1,1],3)],[6,10])
def fruit(a): return max(j-i for i,j in subs(len(a)) if len(set(a[i:j]))<=2)
ok('fr',[fruit([1,2,1]),fruit([0,1,2,2]),fruit([1,2,3,2,2])],[3,3,4])
def kd(s,k): return max([0]+[j-i for i,j in subs(len(s)) if len(set(s[i:j]))<=k])
ok('kd',[kd("eceba",2),kd("aa",1),kd("abc",0)],[3,2,0])
def prod(a,k):
    c=0
    for i,j in subs(len(a)):
        p=1
        for x in a[i:j]: p*=x
        c+= p<k
    return c
ok('prod',[prod([10,5,2,6],100),prod([1,2,3],0)],[8,0])
def c3(a,t): return min((sum(c) for c in combinations(a,3)),key=lambda s:abs(s-t))
ok('c3',[c3([-1,2,1,-4],1),c3([0,0,0],1)],[2,0])
def cards(a,k): return max(sum(a[:i])+sum(a[len(a)-(k-i):]) for i in range(k+1))
ok('cards',[cards([1,2,3,4,5,6,1],3),cards([2,2,2],2),cards([9,7,7,9,7,7,9],7)],[12,4,55])
def del1(a):
    return max(j-i-1 for i,j in subs(len(a)) if a[i:j].count(0)<=1 and j-i>=1) if len(a)>0 else 0
def del1(a):
    best=0
    for i in range(len(a)):
        b=a[:i]+a[i+1:]; cur=0
        for x in b:
            cur=cur+1 if x else 0; best=max(best,cur)
    return best
ok('del1',[del1([1,1,0,1]),del1([0,1,1,1,0,1,1,0,1]),del1([1,1,1])],[3,5,2])
def nice(a,k): return sum(1 for i,j in subs(len(a)) if sum(x%2 for x in a[i:j])==k)
ok('nice',[nice([1,1,2,1,1],3),nice([2,4,6],1),nice([2,2,2,1,2,2,1,2,2,2],2)],[2,0,16])
def f4(a,t): return sorted(set(tuple(sorted(c)) for c in combinations(a,4) if sum(c)==t))
ok('4s',f4([1,0,-1,0,-2,2],0),[(-2,-1,1,2),(-2,0,0,2),(-1,0,0,1)]); ok('4s2',f4([2]*5,8),[(2,2,2,2)])
def kdi(a,k): return sum(1 for i,j in subs(len(a)) if len(set(a[i:j]))==k)
ok('kdi',[kdi([1,2,1,2,3],2),kdi([1,2,1,3,4],3)],[7,3])
def abc(s): return sum(1 for i,j in subs(len(s)) if set("abc")<=set(s[i:j]))
ok('abc',[abc("abcabc"),abc("aaacb"),abc("abc")],[10,3,1])
def exactk(a,k): return max([0]+[j-i for i,j in subs(len(a)) if sum(a[i:j])==k])
ok('neg',[exactk([1,-1,5,-2,3],3),exactk([-2,-1,2,1],1)],[4,2])
def le_k_naive(a,k):
    l=0;s=0;best=0
    for r,x in enumerate(a):
        s+=x
        while s>k and l<=r: s-=a[l]; l+=1
        best=max(best,r-l+1)
    return best
def le_k(a,k): return max([0]+[j-i for i,j in subs(len(a)) if sum(a[i:j])<=k])
ok('when',(le_k([4,-3,1],2),le_k_naive([4,-3,1],2)),(3,2))
ok('when2',(le_k([1,2,3],3),le_k_naive([1,2,3],3)),(2,2))
w=[1,3,2,6,-1,4,1,8,2]
sums=[sum(w[i:i+5]) for i in range(len(w)-5+1)]
ok('win',sums,[11,14,12,18,14])
def boats(p,L):
    from itertools import permutations
    best=len(p)
    # brute: partition into groups of <=2 with sum<=L
    def go(rem):
        if not rem: return 0
        a=rem[0]; r=rem[1:]; m=1+go(r)
        for i,b in enumerate(r):
            if a+b<=L: m=min(m,1+go(r[:i]+r[i+1:]))
        return m
    return go(list(p))
ok('boats',[boats([3,2,2,1],3),boats([3,5,3,4],5),boats([1,2],3)],[3,4,1])
def mount(a):
    best=0
    for i,j in subs(len(a)):
        b=a[i:j]
        if len(b)>=3:
            p=b.index(max(b))
            if 0<p<len(b)-1 and all(b[x]<b[x+1] for x in range(p)) and all(b[x]>b[x+1] for x in range(p,len(b)-1)): best=max(best,len(b))
    return best
ok('mt',[mount([2,1,4,7,3,2,5]),mount([2,2,2])],[5,0])
def rx(a,x):
    best=-1
    for i in range(len(a)+1):
        for j in range(i,len(a)+1):
            if sum(a[:i])+sum(a[j:])==x: best=max(best,i+len(a)-j) if False else (i+len(a)-j if best==-1 else min(best,i+len(a)-j))
    return best
ok('rx',[rx([1,1,4,2,3],5),rx([5,6,7,8,9],4),rx([3,2,20,1,1,3],10)],[2,-1,5])
def kth(a,b,k): return sorted(a+b)[k-1]
ok('kth',[kth([1,3,5,7],[2,4,6],5),kth([1,1,2],[1,2,2],4)],[5,2])
def cw(s,words):
    L=len(words[0]);n=len(words);out=[]
    for i in range(len(s)-L*n+1):
        ch=[s[i+x*L:i+x*L+L] for x in range(n)]
        if sorted(ch)==sorted(words): out.append(i)
    return out
ok('cw',[cw("barfoothefoobarman",["foo","bar"]),cw("wordgoodgoodgoodbestword",["word","good","best","word"]),cw("barfoofoobarthefoobarman",["bar","foo","the"])],[[0,9],[],[6,9,12]])
def mws(s,t):
    best=""
    for i,j in subs(len(s)):
        it=iter(s[i:j])
        if all(c in it for c in t) and (best=="" or j-i<len(best)): best=s[i:j]
    return best
ok('mws',[mws("abcdebdde","bde"),mws("jmeqksfrsdcmsiwvaovztaqenprpvnbstl","u")],["bcde",""])
def ssk(a,k): return min([j-i for i,j in subs(len(a)) if sum(a[i:j])>=k] or [-1])
ok('ssk',[ssk([1],1),ssk([1,2],4),ssk([2,-1,2],3)],[1,-1,3])
def cal(a):
    n=len(a)
    for s in range(n):
        seen=[];i=s
        while i not in seen:
            seen.append(i); i=(i+a[i])%n
        cyc=seen[seen.index(i):]
        if len(cyc)>1 and (all(a[x]>0 for x in cyc) or all(a[x]<0 for x in cyc)): return True
    return False
ok('cal',[cal([2,-1,1,2,2]),cal([-1,-2,-3,-4,-5,6]),cal([1,-1,5,1,4])],[True,False,True])
def lim(a,l): return max(j-i for i,j in subs(len(a)) if max(a[i:j])-min(a[i:j])<=l)
ok('lim',[lim([8,2,4,7],4),lim([10,1,2,4,7,2],5),lim([4,2,2,2,4,4,2,2],0)],[2,4,3])
print("all examples verified")
