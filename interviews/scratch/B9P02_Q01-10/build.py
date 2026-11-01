import re,os
d=os.path.dirname(os.path.abspath(__file__))
part=open(os.path.join(d,'..','..','Book9_SoftSkills','Book9_SoftSkills_Part02.md'),encoding='utf-8').read()
out=[]
for n in range(1,11):
    m=re.search(r'(?m)^### Q%d .*\n(\*\*Asked at:\*\*.*\n)?'%n,part)
    head=m.group(0).rstrip('\n')
    body=open(os.path.join(d,'q%02d.md'%n),encoding='utf-8').read().rstrip('\n')
    out.append(head+'\n'+body+'\n')
open(os.path.join(d,'answers.md'),'w',encoding='utf-8').write('\n'.join(out))
