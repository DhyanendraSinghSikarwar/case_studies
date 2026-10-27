# Runs every example printed in the Part 3 prompts against brute-force reference code. Run: python3 -I check_examples.py
import re, itertools, unicodedata, functools, time
from itertools import groupby, permutations
def ok(name, got, exp):
    assert got == exp, (name, got, exp)
# reverse words (manual reference)
def rw(s):
    w=[];cur=''
    for c in s+' ':
        if c==' ':
            if cur: w.append(cur); cur=''
        else: cur+=c
    return ' '.join(w[::-1])
ok('rw',[rw('  the sky  is blue '),rw('a'),rw('   ')],['blue is sky the','a',''])
def lcp(a):
    p=''
    for k in range(min(map(len,a))+1):
        if all(x[:k]==a[0][:k] for x in a): p=a[0][:k]
    return p
ok('lcp',[lcp(['flower','flow','flight']),lcp(['dog','racecar','car']),lcp(['a']),lcp(['','b'])],['fl','','a',''])
def i2r(n):
    t=[(1000,'M'),(900,'CM'),(500,'D'),(400,'CD'),(100,'C'),(90,'XC'),(50,'L'),(40,'XL'),(10,'X'),(9,'IX'),(5,'V'),(4,'IV'),(1,'I')]
    o=''
    for v,s in t:
        while n>=v: o+=s;n-=v
    return o
R2I={i2r(n):n for n in range(1,4000)}
ok('r2i',[R2I[x] for x in ('III','LVIII','MCMXCIV','IX')],[3,58,1994,9])
ok('i2r',[i2r(3749),i2r(58),i2r(1994),i2r(4)],['MMMDCCXLIX','LVIII','MCMXCIV','IV'])
ok('find',[('sadbutsad'.find('sad')),'leetcode'.find('leeto'),'mississippi'.find('issip'),'abc'.find('')],[0,-1,4,0])
def rot(s,g): return any(s[i:]+s[:i]==g for i in range(len(s)))
ok('rot',[rot('abcde','cdeab'),rot('abcde','abced'),rot('aa','a')],[True,False,False])
ok('join',', '.join(['ab','cd','e']),'ab, cd, e'); ok('join2',', '.join([]),''); ok('join3',', '.join(['x']),'x')
def atoi(s):
    m=re.match(r' *([+-]?\d+)',s)
    return max(-2**31,min(2**31-1,int(m.group(1)))) if m else 0
ok('atoi',[atoi(x) for x in ('42','   -042','1337c0d3','words and 987','-91283472332','+-12')],[42,-42,1337,0,-2147483648,0])
def lps(s):
    best=''
    for i in range(len(s)):
        for j in range(i+1,len(s)+1):
            t=s[i:j]
            if t==t[::-1] and len(t)>len(best): best=t
    return best
ok('lps',[lps(x) for x in ('babad','cbbd','a','abacdfgdcaba')],['bab','bb','a','aba'])
def cnt(s): return sum(s[i:j]==s[i:j][::-1] for i in range(len(s)) for j in range(i+1,len(s)+1))
ok('cnt',[cnt('abc'),cnt('aaa'),cnt('abba')],[3,6,6])
def comp(ch):
    o=[]
    for c,g in groupby(ch):
        n=len(list(g)); o.append(c)
        if n>1: o+=list(str(n))
    return o
ok('comp',[comp(list('aabbccc')),comp(['a']),comp(['a']+['b']*12)],[list('a2b2c3'),['a'],['a','b','1','2']])
ok('mul',[str(int(a)*int(b)) for a,b in (('2','3'),('123','456'),('0','9999'),('99','99'))],['6','56088','0','9801'])
def rep(s): return any(s==s[:k]*(len(s)//k) for k in range(1,len(s)) if len(s)%k==0)
ok('rep',[rep('abab'),rep('aba'),rep('abcabcabcabc'),rep('a')],[True,False,True,False])
def calc(e): return eval(e.replace('/','//'))
ok('calc',[calc(x) for x in ('3+2*2',' 3/2 ',' 3+5 / 2 ','14-3/2','10-20/3')],[7,1,5,13,4])
ok('adds',[str(int(a)+int(b)) for a,b in (('11','123'),('456','77'),('0','0'),('999','1'))],['134','533','0','1000'])
ok('addb',[bin(int(a,2)+int(b,2))[2:] for a,b in (('11','1'),('1010','1011'),('0','0'))],['100','10101','0'])
from collections import Counter
def lp(s):
    c=Counter(s); return sum(v//2*2 for v in c.values())+(1 if any(v%2 for v in c.values()) else 0)
ok('lp',[lp(x) for x in ('abccccdd','a','Aa','aaabbb')],[7,1,1,5])
def rv(s):
    v=[c for c in s if c in 'aeiouAEIOU'][::-1]; o=[]
    for c in s: o.append(v.pop(0) if c in 'aeiouAEIOU' else c)
    return ''.join(o)
ok('rv',[rv(x) for x in ('IceCreAm','leetcode','xyz')],['AceCreIm','leotcede','xyz'])
def zig(s,r):
    if r==1: return s
    g=[[] for _ in range(r)];row=0;d=1
    for c in s:
        g[row].append(c)
        if row==0: d=1
        if row==r-1: d=-1
        row+=d
    return ''.join(''.join(x) for x in g)
ok('zig',[zig('PAYPALISHIRING',3),zig('PAYPALISHIRING',4),zig('AB',1)],['PAHNAPLSIIGYIR','PINALSIGYAHRPI','AB'])
def cv(a,b):
    x=list(map(int,a.split('.')));y=list(map(int,b.split('.')));n=max(len(x),len(y))
    x+=[0]*(n-len(x));y+=[0]*(n-len(y)); return (x>y)-(x<y)
ok('cv',[cv('1.2','1.10'),cv('1.01','1.001'),cv('1.0','1.0.0.0'),cv('0.1','1.1'),cv('2.0.1','2')],[-1,0,0,-1,1])
def enc(l): return ''.join(s.replace('/','//').replace('#','/#')+'#' for s in l)
def dec(s):
    o=[];cur=[];i=0
    while i<len(s):
        c=s[i]
        if c=='/': cur.append(s[i+1]); i+=2; continue
        if c=='#': o.append(''.join(cur)); cur=[]
        else: cur.append(c)
        i+=1
    return o
ok('enc',[enc(['a#b','c','']),enc([]),enc([''])],['a/#b#c##','','#'])
ok('dec',dec('a/#b#c##'),['a#b','c',''])
import random
random.seed(1)
for _ in range(500):
    l=[''.join(random.choice('a#/') for _ in range(random.randint(0,4))) for _ in range(random.randint(0,4))]
    assert dec(enc(l))==l
def zf(s): return [len(s) if i==0 else next((k for k in range(len(s)-i+1) if k==len(s)-i or s[k]!=s[i+k]),0) for i in range(len(s))]
ok('z',zf('aabxaab'),[7,1,0,0,3,1,0])
def occ(t,p): return [i for i in range(len(t)-len(p)+1) if t[i:i+len(p)]==p]
ok('occ',occ('abababa','aba'),[0,2,4])
def pi(s): return [max([k for k in range(i+1) if s[:k]==s[i+1-k:i+1]]) for i in range(len(s))]
ok('pi',[pi('abacaba'),pi('aabaaab')],[[0,0,1,0,1,2,3],[0,1,0,1,2,2,3]])
ok('occ2',occ('aaaa','aa'),[0,1,2])
ok('rk',[occ('abracadabra','abra'),occ('aaaaa','aa'),occ('abcabc','cab')],[[0,7],[0,1,2,3],[2]])
def minrot(s):
    best=min(range(len(s)),key=lambda i:(s[i:]+s[:i],i)); return (s[best:]+s[:best],best)
ok('minrot',[minrot(x) for x in ('bca','cba','abab','aaa')],[('abc',2),('acb',2),('abab',0),('aaa',0)])
def hp(s):
    for k in range(len(s)-1,0,-1):
        if s[:k]==s[-k:]: return s[:k]
    return ''
ok('hp',[hp(x) for x in ('level','ababab','abc','a')],['l','abab','',''])
def sp(s):
    for k in range(len(s),-1,-1):
        if s[:k]==s[:k][::-1]: return s[k:][::-1]+s
ok('sp',[sp(x) for x in ('aacecaaa','abcd','','aba')],['aaacecaaa','dcbabcd','','aba'])
VN=re.compile(r'[+-]?(\d+\.?\d*|\.\d+)([eE][+-]?\d+)?')
good=['2','0089','-0.1','+3.14','4.','-.9','2e10','3e+7','53.5e93']; bad=['abc','1a','1e','e3','99e2.5','--6','-+3','95a54e53','.','+.']
ok('vn',[bool(VN.fullmatch(x)) for x in good+bad],[True]*len(good)+[False]*len(bad))
def cts(s): return (len(s),len(s.encode()),len(s.encode('utf-16-le'))//2)
ok('cts',cts('aé\U0001F600'),(3,7,4)); ok('len',(len('é'),len('é'),len('\U0001F600'.encode())),(2,1,4))
def same(a,b,compat=False):
    f='NFKD' if compat else 'NFD'
    n=lambda x: unicodedata.normalize(f,unicodedata.normalize(f,x).casefold())
    return n(a)==n(b)
ok('same',[same('Straße','STRASSE'),same('é','é'),same('①','1'),same('①','1',compat=True)],[True,True,False,True])
ok('lower',('ß'.lower()=='ss','ß'.casefold()=='ss'),(False,True))
def rt(s):
    u=[]
    for c in s:
        if unicodedata.combining(c) and u: u[-1]+=c
        else: u.append(c)
    return ''.join(u[::-1])
ok('rt',(rt('café'),'éx'[::-1]),('éfac','x́e'))
def u8(d):
    try: bytes(d).decode('utf-8'); return True
    except UnicodeDecodeError: return False
ok('u8',[u8(x) for x in ([197,130,1],[235,140,4],[255],[])],[True,False,False,True])
ok('re',(bool(re.fullmatch(r'(a+)+','aaaa')),re.fullmatch(r'(a+)+','aaab')),(True,None))
def wild(s,p):
    @functools.cache
    def f(i,j):
        if j==len(p): return i==len(s)
        if p[j]=='*': return f(i,j+1) or (i<len(s) and f(i+1,j))
        return i<len(s) and (p[j]=='?' or p[j]==s[i]) and f(i+1,j+1)
    return f(0,0)
ok('wild',[wild(*x) for x in (('aa','a'),('aa','*'),('cb','?a'),('adceb','*a*b'),('acdcb','a*c?b'),('','*'))],[False,True,False,True,False,True])
ok('man',(lps('babad'),lps('abacdfgdcaba'),cnt('aaa')),('bab','aba',6))
def one(s,t):
    if abs(len(s)-len(t))>1: return False
    if len(s)==len(t): return sum(a!=b for a,b in zip(s,t))==1
    a,b=(s,t) if len(s)<len(t) else (t,s)
    return any(b[:i]+b[i+1:]==a for i in range(len(b)))
ok('one',[one(*x) for x in (('ab','acb'),('cab','ad'),('1203','1213'),('',''),('a',''),('ab','ab'))],[True,False,True,False,True,False])
def ed(a,b):
    d=[[0]*(len(b)+1) for _ in range(len(a)+1)]
    for i in range(len(a)+1):
        for j in range(len(b)+1):
            d[i][j]=i if j==0 else j if i==0 else min(d[i-1][j]+1,d[i][j-1]+1,d[i-1][j-1]+(a[i-1]!=b[j-1]))
    return d[-1][-1]
def lcs(a,b):
    d=[[0]*(len(b)+1) for _ in range(len(a)+1)]
    for i in range(1,len(a)+1):
        for j in range(1,len(b)+1):
            d[i][j]=d[i-1][j-1]+1 if a[i-1]==b[j-1] else max(d[i-1][j],d[i][j-1])
    return d[-1][-1]
ok('ed',(ed('horse','ros'),ed('intention','execution'),lcs('abcde','ace'),lcs('abc','def'),len('horse')+len('ros')-2*lcs('horse','ros')),(3,5,3,0,4))
ws=['apple','app','apt','bat','bath']
ok('pref',[sum(w.startswith(p) for w in ws) for p in ('ap','bat','c','')],[3,2,0,5])
def ms(s,t): return min(sum(a!=b for a,b in zip(s,p)) for p in set(permutations(t)))
ok('ms',[ms('bab','aba'),ms('leetcode','practice'),ms('anagram','mangaar')],[1,5,0])
def lrs(s):
    best=0
    for L in range(1,len(s)):
        seen=set()
        for i in range(len(s)-L+1):
            t=s[i:i+L]
            if t in seen: best=L;break
            seen.add(t)
    return best
ok('lrs',[lrs(x) for x in ('banana','abcd','aaaaa','abcabcabc')],[3,0,4,6])
print("all examples verified")
