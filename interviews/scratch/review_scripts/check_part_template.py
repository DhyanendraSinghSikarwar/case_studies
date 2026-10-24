import re,sys,subprocess,os
p='Book2_GenAI/Book2_GenAI_Part10.md'
t=open(p,encoding='utf-8').read()
qs=re.split(r'(?m)^(?=### Q\d+ )',t)[1:]
print('questions',len(qs))
need=['Say this first','Then explain','Follow-ups','Common mistakes']
nums=[int(re.match(r'### Q(\d+)',q).group(1)) for q in qs]
print('continuous',nums==list(range(1,len(qs)+1)))
stars=[len(re.match(r'### Q\d+ ((?:⭐)+)',q).group(1)) for q in qs]
print('star order ok',stars==sorted(stars,reverse=True),'counts',[stars.count(i) for i in (3,2,1)])
for q in qs:
    n=re.match(r'### Q(\d+)',q).group(1)
    miss=[k for k in need if k not in q]
    if 'Example' not in q: miss.append('Example')
    if miss: print('Q'+n,'missing',miss)
blocks=[]
for q in qs:
    n=re.match(r'### Q(\d+)',q).group(1)
    lines=q.split('\n'); inb=False; i=0
    for l in lines:
        if not inb and l.startswith('```python'): inb=True; cur=[]; continue
        if inb and l.startswith('```'): blocks.append((n,i,'\n'.join(cur)+'\n')); i+=1; inb=False; continue
        if inb: cur.append(l)
print('python blocks',len(blocks))
fails=[]
for n,i,b in blocks:
    f=f'/tmp/claude-0/rev_b2p8/q{n}_{i}.py'; open(f,'w').write(b)
    r=subprocess.run(['python3','-I',f],capture_output=True,text=True,timeout=300,cwd='/tmp/claude-0/rev_b2p8')
    nx='not executed' in b
    print(f'Q{n}#{i}','rc',r.returncode,'NOTEXEC' if nx else '', (r.stderr.strip().splitlines() or [''])[-1][:100] if r.returncode else '')
    if r.returncode and not nx: fails.append((n,i))
print('FAILS',fails)
