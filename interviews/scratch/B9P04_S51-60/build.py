import re,os
p='Book9_SoftSkills/Book9_SoftSkills_Part04.md'
t=open(p,encoding='utf-8').read()
out=[]
for n in range(51,61):
    m=re.search(r'(?ms)^(### S%d .*?)\n(\*\*Asked at:\*\*.*?)\n(\*\*Situation:\*\*.*?)\n'%n,t)
    out.append('\n'.join(m.groups())+'\n'+open('scratch/B9P04_S51-60/S%d.txt'%n,encoding='utf-8').read().rstrip()+'\n')
open('scratch/B9P04_S51-60/answers.md','w',encoding='utf-8').write('\n'.join(out))
