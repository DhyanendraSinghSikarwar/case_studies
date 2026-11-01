import re,subprocess,os,sys
D=os.path.dirname(os.path.abspath(__file__))
part=open(D+'/../../Book6_Scenarios/Book6_Scenarios_Part07.md',encoding='utf-8').read()
out=[]
for n in range(45,56):
    m=re.search(r'(?m)^(### Q%d .*)\n(\*\*Asked at:\*\*.*)$'%n,part)
    head,asked=m.group(1),m.group(2)
    tf=D+'/q%02d.txt'%n; cf=D+'/q%02d.py'%n
    if not os.path.exists(tf) or not os.path.exists(cf): continue
    body=open(tf,encoding='utf-8').read().rstrip()+'\n'
    code=open(cf,encoding='utf-8').read().rstrip()+'\n'
    r=subprocess.run(['python3','-I',cf],cwd='/tmp',capture_output=True,text=True,timeout=120,stdin=subprocess.DEVNULL)
    if r.returncode: print('FAIL Q',n,r.stderr[-400:]); sys.exit(1)
    body=body.replace('{CODE}','```python\n'+code+'```').replace('{OUTPUT}','```\n'+r.stdout.rstrip()+'\n```')
    out.append(head+'\n'+asked+'\n\n'+body)
open(D+'/answers.md','w',encoding='utf-8').write('\n'.join(out))
print('built',len(out))
