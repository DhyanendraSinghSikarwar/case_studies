import re,subprocess,tempfile,os,shutil
here=os.path.dirname(os.path.abspath(__file__))
part=os.path.join(here,'..','..','Book6_Scenarios','Book6_Scenarios_Part06.md')
t=open(part,encoding='utf-8').read()
blocks={}
for b in re.split(r'(?m)^(?=### Q\d+ )',t)[1:]:
    n=int(re.match(r'### Q(\d+)',b).group(1)); L=b.split('\n'); blocks[n]=(L[0],L[1])
out=[]
for n in range(10,19):
    bf=os.path.join(here,f'q{n}.md')
    if not os.path.exists(bf): continue
    body=open(bf,encoding='utf-8').read().strip('\n')
    cf=os.path.join(here,f'q{n}.py')
    code=open(cf,encoding='utf-8').read().rstrip('\n')
    d=tempfile.mkdtemp(); open(d+'/x.py','w').write(code+'\n')
    r=subprocess.run(['python3','-I','x.py'],cwd=d,capture_output=True,text=True,timeout=300,stdin=subprocess.DEVNULL)
    assert r.returncode==0,(n,r.stderr)
    body=body.replace('{{CODE}}','```python\n'+code+'\n```').replace('{{OUTPUT}}','```text\n'+r.stdout.rstrip('\n')+'\n```')
    out.append(blocks[n][0]+'\n'+blocks[n][1]+'\n'+body+'\n')
open(os.path.join(here,'answers.md'),'w',encoding='utf-8').write('\n'.join(out))
for r,ds,fs in os.walk(here):
    for d in ds:
        if d=='__pycache__': shutil.rmtree(os.path.join(r,d))
print('built',len(out))
