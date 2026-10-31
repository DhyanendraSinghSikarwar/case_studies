import re,glob,os
base='/home/user/case_studies/interviews'
t=open(base+'/Book9_SoftSkills/Book9_SoftSkills_Part03.md',encoding='utf-8').read()
out=[]
for n in range(21,31):
    m=re.search(r'(?m)^### Q%d .*\n(\*\*Asked at:\*\*.*)\n'%n,t)
    head=m.group(0).rstrip('\n')
    f=base+'/scratch/B9P03_Q21-30/items/q%d.md'%n
    if os.path.exists(f): out.append(head+'\n'+open(f,encoding='utf-8').read().strip()+'\n')
open(base+'/scratch/B9P03_Q21-30/answers.md','w',encoding='utf-8').write('\n'.join(out))
