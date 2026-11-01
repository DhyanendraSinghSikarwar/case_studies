import re,subprocess,os,sys
D=os.path.dirname(os.path.abspath(__file__))
P=os.path.join(D,'..','..','Book6_Scenarios','Book6_Scenarios_Part04.md')
t=open(P,encoding='utf-8').read()
out=[]
for n in range(12,23):
    if not os.path.exists(f"{D}/q{n}.md"): continue
    m=re.search(r'(?m)^### Q%d .*\n\*\*Asked at:\*\*.*$'%n,t)
    head=m.group(0)
    body=open(f'{D}/q{n}.md',encoding='utf-8').read().strip('\n')
    code=open(f'{D}/q{n}.py',encoding='utf-8').read().rstrip('\n')
    r=subprocess.run(['python3','-I',f'{D}/q{n}.py'],capture_output=True,text=True,cwd='/tmp',timeout=300)
    assert r.returncode==0,(n,r.stderr)
    open(f'{D}/q{n}.out','w').write(r.stdout)
    body=body.replace('{{CODE}}','```python\n'+code+'\n```').replace('{{OUTPUT}}','```text\n'+r.stdout.rstrip('\n')+'\n```')
    out.append(head+'\n'+body+'\n')
open(f'{D}/answers.md','w',encoding='utf-8').write('\n'.join(out))
print('built',len(out))
