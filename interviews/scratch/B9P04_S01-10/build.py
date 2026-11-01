import re,os
d=os.path.dirname(os.path.abspath(__file__))
t=open(d+'/../../Book9_SoftSkills/Book9_SoftSkills_Part04.md',encoding='utf-8').read()
out=[]
for b in re.split(r'(?m)^(?=### S\d+ )',t)[1:]:
    n=int(re.match(r'### S(\d+) ',b).group(1))
    if n>10: continue
    L=b.split('\n')
    head=L[0]; asked=[l for l in L if l.startswith('**Asked at:**')]; sit=[l for l in L if l.startswith('**Situation:**')][0]
    body=open(f'{d}/s{n:02d}.md',encoding='utf-8').read().strip()
    out.append('\n'.join([head]+asked+[sit,body])+'\n')
open(d+'/answers.md','w',encoding='utf-8').write('\n'.join(out))
