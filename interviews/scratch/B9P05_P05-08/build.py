import re
src=open('/home/user/case_studies/interviews/Book9_SoftSkills/Book9_SoftSkills_Part05.md',encoding='utf-8').read()
blocks=re.split(r'(?m)^(?=### P\d+ )',src)[1:]
out=[]
for n in (5,6,7,8):
    b=[x for x in blocks if x.startswith(f'### P{n} ')][0].split('\n')
    head=b[0]; asked=[l for l in b if l.startswith('**Asked at:**')][0]; scope=[l for l in b if l.startswith('**Scope:**')][0]
    body=open(f'/home/user/case_studies/interviews/scratch/B9P05_P05-08/P{n}.md',encoding='utf-8').read().strip()
    out.append('\n'.join([head,asked,scope,'',body,'']))
open('/home/user/case_studies/interviews/scratch/B9P05_P05-08/answers.md','w',encoding='utf-8').write('\n'.join(out))
