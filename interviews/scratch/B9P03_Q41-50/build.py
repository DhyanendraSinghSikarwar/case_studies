import re
t=open('../../Book9_SoftSkills/Book9_SoftSkills_Part03.md',encoding='utf-8').read()
out=[]
for n in range(41,51):
    m=re.search(r'(?ms)^(### Q%d .*?)\n(\*\*Asked at:\*\*.*?)\n<!-- ANSWER_PENDING -->'%n,t)
    try: body=open('item_%d.md'%n,encoding='utf-8').read().strip()
    except FileNotFoundError: continue
    out.append(m.group(1)+'\n'+m.group(2)+'\n'+body+'\n')
open('answers.md','w',encoding='utf-8').write('\n'.join(out))
print(len(out))
