import re,os
d=os.path.dirname(os.path.abspath(__file__))
t=open(os.path.join(d,'../../Book9_SoftSkills/Book9_SoftSkills_Part02.md'),encoding='utf-8').read()
out=[]
for n in range(31,41):
    f=os.path.join(d,'q%d.md'%n)
    if not os.path.exists(f): continue
    h=re.search(r'(?m)^### Q%d .*$'%n,t).group(0)
    a=re.search(r'(?m)^### Q%d .*\n(\*\*Asked at:\*\*.*)$'%n,t).group(1)
    out.append(h+'\n'+a+'\n'+open(f,encoding='utf-8').read().strip()+'\n')
open(os.path.join(d,'answers.md'),'w',encoding='utf-8').write('\n'.join(out))
print(len(out),'items')
