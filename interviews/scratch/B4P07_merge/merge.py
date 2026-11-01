import re,sys,glob
P='Book4_MLOps/Book4_MLOps_Part07.md'
t=open(P,encoding='utf-8',newline='').read()
assert '\r\n' not in t
def blocks(text):
    parts=re.split(r'(?m)^(?=### Q\d+ )',text)
    out={}
    for b in parts:
        m=re.match(r'### Q(\d+) ',b)
        if m: out[int(m.group(1))]=b
    return out
cur=blocks(t)
merged=[];skipped=[]
for f in sorted(glob.glob('scratch/B4P07_Q*/answers.md')):
    a=open(f,encoding='utf-8').read().replace('\r\n','\n')
    for n,b in blocks(a).items():
        old=cur[n]
        h_old=old.split('\n')[0]; h_new=b.split('\n')[0]
        ask_old=[l for l in old.split('\n') if l.startswith('**Asked at:**')][0]
        ask_new=[l for l in b.split('\n') if l.startswith('**Asked at:**')]
        if h_old!=h_new or not ask_new or ask_new[0]!=ask_old or 'ANSWER_PENDING' in b:
            skipped.append((n,f)); continue
        nb=b.rstrip('\n')+'\n\n'
        t=t.replace(old,nb,1); cur=blocks(t); merged.append(n)
open(P,'w',encoding='utf-8',newline='').write(t)
print('merged',sorted(merged)); print('skipped',skipped)
print('pending left',t.count('ANSWER_PENDING'))
