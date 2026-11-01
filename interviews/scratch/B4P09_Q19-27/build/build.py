import re
P='/home/user/case_studies/interviews/'; S=P+'scratch/B4P09_Q19-27/'
lines=open(P+'Book4_MLOps/Book4_MLOps_Part09.md').read().split('\n')
head={}
for i,l in enumerate(lines):
    m=re.match(r'### (Q\d+) ',l)
    if m: head[m.group(1)]=(l,lines[i+1]); assert lines[i+1].startswith('**Asked at:**')
body=open(S+'build/body.md').read()
parts=re.split(r'^@@(Q\d+)\n',body,flags=re.M)
def code(m):
    fs=m.group(1).split(','); txt=''
    for f in fs:
        c=open(S+'code/'+f).read().rstrip('\n')
        txt+=(f'# ---- file: {f} ----\n' if len(fs)>1 else '')+c+'\n\n'
    return '```python\n'+txt.rstrip('\n')+'\n```'
def out(m):
    fs=m.group(1).split(','); txt=''
    for f in fs:
        o=open(S+'out/'+f).read().rstrip('\n')
        txt+=(f'# ---- {f} ----\n' if len(fs)>1 else '')+o+'\n\n'
    return '```\n'+txt.rstrip('\n')+'\n```'
res=['# Book 4 Part 9, Q19-Q27 answers (Wave B)\n']
for q,b in zip(parts[1::2],parts[2::2]):
    b=re.sub(r'\{\{CODE:([^}]+)\}\}',code,b); b=re.sub(r'\{\{OUT:([^}]+)\}\}',out,b)
    res.append(head[q][0]+'\n'+head[q][1]+'\n'+b.strip()+'\n')
open(S+'answers.md','w').write('\n'.join(res))
