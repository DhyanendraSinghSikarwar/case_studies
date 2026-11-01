import re,os
R='/home/user/case_studies/interviews'
part=open(R+'/Book9_SoftSkills/Book9_SoftSkills_Part01.md',encoding='utf-8').read()
d=os.path.dirname(os.path.abspath(__file__))
out=[]
for n in range(41,51):
    m=re.search(r'(?m)^(### Q%d .*)\n(\*\*Asked at:\*\*.*)\n'%n,part)
    body=open(f'{d}/q{n}.md',encoding='utf-8').read().rstrip()
    out.append(m.group(1)+'\n'+m.group(2)+'\n'+body+'\n')
open(d+'/answers.md','w',encoding='utf-8').write('\n'.join(out))
