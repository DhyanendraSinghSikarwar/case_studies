import re,os
base=os.path.dirname(os.path.abspath(__file__))
src=open('/home/user/case_studies/interviews/Book9_SoftSkills/Book9_SoftSkills_Part03.md',encoding='utf-8').read()
out=[]
for n in range(1,11):
    m=re.search(r'(?m)^### Q%d .*\n(\*\*Asked at:\*\*.*)\n'%n,src)
    h=re.search(r'(?m)^### Q%d .*$'%n,src).group(0)
    body=open(os.path.join(base,'items','%02d.md'%n),encoding='utf-8').read().rstrip()
    out.append(h+'\n'+m.group(1)+'\n'+body+'\n')
open(os.path.join(base,'answers.md'),'w',encoding='utf-8').write('\n'.join(out))
