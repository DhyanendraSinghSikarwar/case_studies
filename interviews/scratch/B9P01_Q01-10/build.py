import re,os
H=os.path.dirname(os.path.abspath(__file__))
part=open(os.path.join(H,'../../Book9_SoftSkills/Book9_SoftSkills_Part01.md'),encoding='utf-8').read()
out=[]
for n in range(1,11):
    m=re.search(r'(?m)^(### Q%d .*)\n(\*\*Asked at:\*\*.*)\n'%n,part)
    p=os.path.join(H,'items','Q%02d.md'%n)
    if not os.path.exists(p): continue
    out.append(m.group(1)+'\n'+m.group(2)+'\n'+open(p,encoding='utf-8').read().strip()+'\n')
open(os.path.join(H,'answers.md'),'w',encoding='utf-8').write('\n'.join(out))
print(len(out),'items')
