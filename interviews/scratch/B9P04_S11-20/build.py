import re,os
d=os.path.dirname(os.path.abspath(__file__))
src=open(os.path.join(d,'../../Book9_SoftSkills/Book9_SoftSkills_Part04.md'),encoding='utf-8').read()
out=[]
for n in range(11,21):
    p=os.path.join(d,f's{n}.md')
    if not os.path.exists(p): continue
    m=re.search(r'(?m)^### S%d .*\n\*\*Asked at:\*\*.*\n\*\*Situation:\*\*.*\n'%n,src)
    out.append(m.group(0)+open(p,encoding='utf-8').read().rstrip()+'\n')
open(os.path.join(d,'answers.md'),'w',encoding='utf-8').write('\n'.join(out))
