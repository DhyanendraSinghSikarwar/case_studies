import re, subprocess, pathlib
root=pathlib.Path(__file__).parent
part=open(root/'../../Book4_MLOps/Book4_MLOps_Part12.md').read()
qs={int(m.group(1)):m.group(0) for m in re.finditer(r'(?m)^### Q(\d+) .*\n\*\*Asked at:\*\*.*',part)}
PY={3:'/tmp/claude-0/b10p10/v/bin/python'}
def run(n):
    f=f"code/q{n:02d}.py"
    cmd=[PY.get(n,'python3'),'-I',f]
    if n==7: cmd=[PY[3],'-I',f]
    r=subprocess.run(cmd,cwd=root,capture_output=True,text=True)
    return (r.stdout+r.stderr).strip()
A={}
exec(open(root/'texts.py').read())
out=[]
for n in range(1,12):
    t=A[n]
    code=open(root/f"code/q{n:02d}.py").read().strip()
    o=run(n)
    t=t.replace('@@CODE@@',"```python\n"+code+"\n```").replace('@@OUT@@',"```text\n"+o+"\n```")
    out.append(qs[n]+"\n"+t.strip()+"\n")
open(root/'answers.md','w').write("\n".join(out))
