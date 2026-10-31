import re,os
base=os.path.dirname(os.path.abspath(__file__))
src=open('/home/user/case_studies/interviews/Book9_SoftSkills/Book9_SoftSkills_Part04.md',encoding='utf-8').read()
out=[]
for n in range(21,31):
    h=re.search(r'(?m)^### S%d .*$'%n,src).group(0)
    a=re.search(r'(?m)^### S%d .*\n(\*\*Asked at:\*\*.*)\n(\*\*Situation:\*\*.*)\n'%n,src)
    body=open(os.path.join(base,'items','%02d.md'%n),encoding='utf-8').read().rstrip()
    out.append(h+'\n'+a.group(1)+'\n'+a.group(2)+'\n'+body+'\n')
open(os.path.join(base,'answers.md'),'w',encoding='utf-8').write('\n'.join(out))
