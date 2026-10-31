import re,os
d=os.path.dirname(os.path.abspath(__file__))
P=os.path.join(d,'..','..','Book9_SoftSkills','Book9_SoftSkills_Part01.md')
t=open(P,encoding='utf-8').read()
out=[]
for n in range(21,31):
    m=re.search(r'(?m)^### Q%d .*\n(\*\*Asked at:\*\*.*)\n'%n,t)
    h=re.search(r'(?m)^### Q%d .*$'%n,t).group(0)
    body=open(os.path.join(d,'q%d.md'%n),encoding='utf-8').read().rstrip('\n')
    out.append(h+'\n'+m.group(1)+'\n'+body+'\n')
open(os.path.join(d,'answers.md'),'w',encoding='utf-8').write('\n'.join(out))
