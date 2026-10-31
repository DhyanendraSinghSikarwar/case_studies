import re,glob,os
base=os.path.dirname(os.path.abspath(__file__))
part=open(os.path.join(base,'../../Book9_SoftSkills/Book9_SoftSkills_Part01.md'),encoding='utf-8').read()
out=[]
for n in range(31,41):
    m=re.search(r'(### Q%d .*\n\*\*Asked at:\*\*.*\n)'%n,part)
    f=os.path.join(base,'Q%d.md'%n)
    if not os.path.exists(f): continue
    out.append(m.group(1)+open(f,encoding='utf-8').read().strip('\n')+'\n')
open(os.path.join(base,'answers.md'),'w',encoding='utf-8').write('\n'.join(out))
