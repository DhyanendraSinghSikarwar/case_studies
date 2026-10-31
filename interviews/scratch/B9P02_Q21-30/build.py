import re,os
base=os.path.dirname(os.path.abspath(__file__))
part=open(os.path.join(base,'../../Book9_SoftSkills/Book9_SoftSkills_Part02.md'),encoding='utf-8').read()
out=[]
for n in range(21,31):
    p=os.path.join(base,'items','q%d.md'%n)
    if not os.path.exists(p): continue
    m=re.search(r'(?m)^### Q%d .*\n(\*\*Asked at:\*\*.*)\n'%n,part)
    h=re.search(r'(?m)^### Q%d .*$'%n,part).group(0)
    out.append(h+'\n'+m.group(1)+'\n'+open(p,encoding='utf-8').read().strip()+'\n')
open(os.path.join(base,'answers.md'),'w',encoding='utf-8').write('\n'.join(out))
