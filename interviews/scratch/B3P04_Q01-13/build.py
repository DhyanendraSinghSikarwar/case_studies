import re, subprocess, sys, os
sys.dont_write_bytecode=True
H='/home/user/case_studies/interviews/scratch/B3P04_Q01-13/'
sys.path.insert(0,H)
from prose1 import P
from prose2 import P2
P.update(P2)
part=open('/home/user/case_studies/interviews/Book3_SQL/Book3_SQL_Part04.md',encoding='utf-8').read()
heads={}
for m in re.finditer(r'^(### Q(\d+) .*)\n(\*\*Asked at:\*\*.*)$',part,re.M):
    heads[int(m.group(2))]=(m.group(1),m.group(3))
out=[]
for n in range(1,14):
    code=open(H+'code/q%02d.py'%n).read().rstrip('\n')
    assert '```' not in code
    run=subprocess.run(['python3','-I',H+'code/q%02d.py'%n],capture_output=True,text=True,cwd='/tmp')
    assert run.returncode==0,(n,run.stderr)
    o=run.stdout.rstrip('\n')
    t=P[n]
    def sch(m):
        sc=re.search(r'^SCHEMA = """\n(.*?)"""',code,re.S|re.M).group(1).strip('\n')
        return '```sql\n'+sc+'\n```'
    t=t.replace('{{SCHEMA}}','\x00S')
    if '\x00S' in t: t=t.replace('\x00S',sch(None))
    def sq(m):
        b=re.search(r'^%s = """\n(.*?)"""'%m.group(1),code,re.S|re.M).group(1).rstrip('\n')
        return '```sql\n'+b+'\n```'
    t=re.sub(r'\{\{SQL:(\w+)\}\}',sq,t)
    def pd_(m):
        b=re.search(r'# pd:%s\n(.*?)# pd:end'%m.group(1),code,re.S).group(1).rstrip('\n')
        return '```py\n'+b+'\n```'
    t=re.sub(r'\{\{PD:(\w+)\}\}',pd_,t)
    t=t.replace('{{CODE}}','```python\n'+code+'\n```').replace('{{OUT}}','```text\n'+o+'\n```')
    assert '{{' not in t,n
    h,a=heads[n]
    out.append(h+'\n'+a+'\n'+t.rstrip('\n')+'\n')
open(H+'answers.md','w',encoding='utf-8').write('\n'.join(out))
print('built')
