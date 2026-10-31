import re,subprocess,os
d=os.path.dirname(os.path.abspath(__file__))
part=open(d+'/../../Book6_Scenarios/Book6_Scenarios_Part06.md',encoding='utf-8').read()
out=[]
for n in range(37,46):
    m=re.search(r'(?m)^### Q%d .*\n\*\*Asked at:\*\*.*'%n,part)
    head=m.group(0)
    body=open(f'{d}/body{n}.md',encoding='utf-8').read().rstrip('\n')
    code=open(f'{d}/q{n}.py',encoding='utf-8').read()
    r=subprocess.run(['python3','-I',f'{d}/q{n}.py'],capture_output=True,text=True,cwd=d,stdin=subprocess.DEVNULL)
    assert r.returncode==0,(n,r.stderr)
    body=body.replace('{{CODE}}','```python\n'+code.rstrip('\n')+'\n```').replace('{{OUTPUT}}','```text\n'+r.stdout.rstrip('\n')+'\n```')
    out.append(head+'\n'+body+'\n')
open(d+'/answers.md','w',encoding='utf-8').write('\n'.join(out))
