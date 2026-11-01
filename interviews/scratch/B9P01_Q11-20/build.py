import re,os
d=os.path.dirname(os.path.abspath(__file__))
part=open(os.path.join(d,'../../Book9_SoftSkills/Book9_SoftSkills_Part01.md'),encoding='utf-8').read()
out=[]
for n in range(11,21):
    f=os.path.join(d,'item_%02d.md'%n)
    if not os.path.exists(f): continue
    m=re.search(r'(?m)^(### Q%d .*)\n(\*\*Asked at:\*\*.*)\n'%n,part)
    out.append(m.group(1)+'\n'+m.group(2)+'\n'+open(f,encoding='utf-8').read().strip()+'\n')
open(os.path.join(d,'answers.md'),'w',encoding='utf-8').write('\n'.join(out))
print(len(out),'items')
