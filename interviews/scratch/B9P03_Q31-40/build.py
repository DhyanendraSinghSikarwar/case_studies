import re,os
base='/home/user/case_studies/interviews'
part=open(base+'/Book9_SoftSkills/Book9_SoftSkills_Part03.md',encoding='utf-8').read()
out=[]
for n in range(31,41):
    m=re.search(r'(### Q%d .*\n\*\*Asked at:\*\*.*\n)'%n,part)
    out.append(m.group(1)+open(os.path.join(base,'scratch/B9P03_Q31-40/items/Q%d.md'%n),encoding='utf-8').read().rstrip()+'\n')
open(base+'/scratch/B9P03_Q31-40/answers.md','w',encoding='utf-8').write('\n'.join(out))
