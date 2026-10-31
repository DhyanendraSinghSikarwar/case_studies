import re,os
d=os.path.dirname(os.path.abspath(__file__))
part=open(os.path.join(d,'../../Book9_SoftSkills/Book9_SoftSkills_Part04.md'),encoding='utf-8').read()
out=[]
for n in range(31,41):
    m=re.search(r'(?ms)^(### S%d .*?)\n(\*\*Asked at:\*\*.*?)\n(\*\*Situation:\*\*.*?)\n'%n,part)
    body=open(os.path.join(d,'S%d.md'%n),encoding='utf-8').read().strip()
    out.append('\n'.join([m.group(1),m.group(2),m.group(3),body])+'\n')
open(os.path.join(d,'answers.md'),'w',encoding='utf-8').write('\n'.join(out))
