import re,subprocess,os,sys,glob
H=os.path.dirname(os.path.abspath(__file__))
part=open('/home/user/case_studies/interviews/Book6_Scenarios/Book6_Scenarios_Part04.md',encoding='utf-8').read()
out=[];status=[]
for n in range(45,56):
    m=re.search(r'(?m)^(### Q%d .*)\n(\*\*Asked at:\*\*.*)$'%n,part)
    md=f'{H}/q{n}.md'
    if not os.path.exists(md): status.append((n,'missing'));continue
    body=open(md,encoding='utf-8').read()
    code=open(f'{H}/q{n}.py',encoding='utf-8').read()
    r=subprocess.run(['python3','-I',f'{H}/q{n}.py'],capture_output=True,text=True,cwd='/tmp')
    if r.returncode: status.append((n,'FAIL '+r.stderr[-300:]));continue
    body=body.replace('{{CODE}}','```python\n'+code.rstrip()+'\n```').replace('{{OUTPUT}}','```text\n'+r.stdout.rstrip()+'\n```')
    out.append(m.group(1)+'\n'+m.group(2)+'\n'+body.strip()+'\n')
    status.append((n,'ok'))
open(f'{H}/answers.md','w',encoding='utf-8').write('\n'.join(out))
print(status)
for d in glob.glob(H+'/__pycache__'): 
    import shutil;shutil.rmtree(d)
