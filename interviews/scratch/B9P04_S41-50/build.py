import re,os
base='/home/user/case_studies/interviews/'
t=open(base+'Book9_SoftSkills/Book9_SoftSkills_Part04.md',encoding='utf-8').read()
out=[]
for n in range(41,51):
    m=re.search(r'(?m)^### S%d .*\n(?:\*\*Asked at:\*\*.*\n)?\*\*Situation:\*\*.*\n'%n,t)
    head=m.group(0)
    body=open(base+'scratch/B9P04_S41-50/items/S%d.md'%n,encoding='utf-8').read().strip()
    out.append(head+'\n'+body+'\n')
open(base+'scratch/B9P04_S41-50/answers.md','w',encoding='utf-8').write('\n'.join(out))
