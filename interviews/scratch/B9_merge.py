import re,sys,glob
# usage: python3 scratch/B9_merge.py <PartNN e.g. 01> <prefix letter Q|S|P>
N,L=sys.argv[1],sys.argv[2]
P='Book9_SoftSkills/Book9_SoftSkills_Part%s.md'%N
t=open(P,encoding='utf-8',newline='').read()
assert '\r\n' not in t
def blocks(text):
    out={}
    for b in re.split(r'(?m)^(?=### %s\d+ )'%L,text):
        m=re.match(r'### %s(\d+) '%L,b)
        if m: out[int(m.group(1))]=b
    return out
cur=blocks(t)
merged=[];skipped=[]
for f in sorted(glob.glob('scratch/B9P%s_*/answers.md'%N)):
    a=open(f,encoding='utf-8').read().replace('\r\n','\n')
    for n,b in blocks(a).items():
        old=cur[n]
        h_old=old.split('\n')[0]; h_new=b.split('\n')[0]
        ao=[l for l in old.split('\n') if l.startswith('**Asked at:**')]
        an=[l for l in b.split('\n') if l.startswith('**Asked at:**')]
        if h_old!=h_new or ao!=an or 'ANSWER_PENDING' in b:
            skipped.append((n,f)); continue
        t=t.replace(old,b.rstrip('\n')+'\n\n',1); cur=blocks(t); merged.append(n)
open(P,'w',encoding='utf-8',newline='').write(t)
print('merged',sorted(merged)); print('skipped',skipped)
print('pending left',t.count('ANSWER_PENDING'))
