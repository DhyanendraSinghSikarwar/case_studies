import re
P='/home/user/case_studies/interviews/'
t=open(P+'Book9_SoftSkills/Book9_SoftSkills_Part05.md',encoding='utf-8').read()
out=[]
for n in (9,10,11,12):
    m=re.search(r'(?m)^### P%d .*\n\*\*Asked at:\*\*.*\n\*\*Scope:\*\*.*$'%n,t)
    out.append(m.group(0)+'\n\n'+open(P+'scratch/B9P05_P09-12/p%02d.md'%n,encoding='utf-8').read().strip()+'\n')
open(P+'scratch/B9P05_P09-12/answers.md','w',encoding='utf-8').write('\n'.join(out))
