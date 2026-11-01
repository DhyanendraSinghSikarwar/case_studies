import re,subprocess,os
here=os.path.dirname(os.path.abspath(__file__))
part=os.path.join(here,'..','..','Book6_Scenarios','Book6_Scenarios_Part05.md')
t=open(part,encoding='utf-8').read()
blocks={int(re.match(r'### Q(\d+) ',b).group(1)):b for b in re.split(r'(?m)^(?=### Q\d+ )',t)[1:]}
out=[]
for q in range(34,45):
    lines=blocks[q].split('\n')
    head,asked=lines[0],lines[1]
    assert asked.startswith('**Asked at:**')
    code=open(f'{here}/q{q}.py').read()
    r=subprocess.run(['python3','-I',f'q{q}.py'],cwd=here,capture_output=True,text=True,check=True)
    body=open(f'{here}/q{q}.md').read().replace('@@CODE@@',code).replace('@@OUT@@',r.stdout)
    out.append(head+'\n'+asked+'\n'+body.rstrip()+'\n')
open(f'{here}/answers.md','w',encoding='utf-8').write('\n'.join(out))
