import re,os
H=os.path.dirname(os.path.abspath(__file__))
part=open(os.path.join(H,'../../Book9_SoftSkills/Book9_SoftSkills_Part05.md'),encoding='utf-8').read()
out=[]
for n in range(1,5):
    m=re.search(r'(?m)^(### P%d .*)\n(\*\*Asked at:\*\*.*)\n(\*\*Scope:\*\*.*)\n'%n,part)
    out.append('\n'.join(m.groups())+'\n'+open(os.path.join(H,'items','P%d.md'%n),encoding='utf-8').read().strip()+'\n')
open(os.path.join(H,'answers.md'),'w',encoding='utf-8').write('\n'.join(out))
print(len(out))
