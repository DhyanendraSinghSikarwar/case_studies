import os,re,subprocess,sys
os.chdir(os.path.dirname(os.path.abspath(__file__)))
PART='../../Book6_Scenarios/Book6_Scenarios_Part07.md'
t=open(PART,encoding='utf-8').read()
bl={int(re.match(r'### Q(\d+)',b).group(1)):b for b in re.split(r'(?m)^(?=### Q\d+ )',t)[1:]}
out=''
for n in range(12,23):
    f=f'q{n}.md'
    if not os.path.exists(f): print('missing',f); continue
    head='\n'.join(bl[n].split('\n')[:2])
    body=open(f,encoding='utf-8').read()
    code=open(f'q{n}.py',encoding='utf-8').read().rstrip('\n')
    r=subprocess.run(['python3','-I',f'q{n}.py'],capture_output=True,text=True,timeout=120,stdin=subprocess.DEVNULL)
    assert r.returncode==0,(n,r.stderr)
    body=body.replace('{{CODE}}','```python\n'+code+'\n```').replace('{{OUTPUT}}','```\n'+r.stdout.rstrip('\n')+'\n```')
    q=head+'\n'+body.strip('\n')+'\n\n'
    open(f'Q{n}_final.md','w',encoding='utf-8').write(q)
    out+=q
open('answers.md','w',encoding='utf-8').write(out)
print('built',len(out))
