import re, subprocess, sys
base="/home/user/case_studies/interviews/"
part=open(base+"Book3_SQL/Book3_SQL_Part02.md").read()
tmpl=open(base+"scratch/B3P02_Q35-45/template.md").read()
src=base+"scratch/B3P02_Q35-45/src/"
blocks=re.split(r"^@@(Q\d+)\n",tmpl,flags=re.M)
out=[]; problems=[]
runs={}
def run(q):
    if q not in runs:
        r=subprocess.run(["python3","-I",src+q+".py"],capture_output=True,text=True,cwd="/tmp")
        if r.returncode: problems.append(f"{q} failed: {r.stderr[-400:]}")
        if r.stderr.strip(): problems.append(f"{q} stderr: {r.stderr[:200]}")
        runs[q]=r.stdout.rstrip("\n")
    return runs[q]
for i in range(1,len(blocks),2):
    qn=blocks[i]; body=blocks[i+1].strip("\n")
    m=re.search(rf"^(### {qn} .*)\n(\*\*Asked at:\*\*.*)$",part,flags=re.M)
    head=m.group(1)+"\n"+m.group(2)+"\n"
    q=qn.lower()
    code=open(src+q+".py").read().rstrip("\n")
    assert "```" not in code
    def sub(mm):
        kind=mm.group(1)
        if kind=="CODE": return "```python\n"+code+"\n```"
        if kind=="OUT": return "```text\n"+run(q)+"\n```"
    body=re.sub(r"\{\{(CODE|OUT):"+q+r"\}\}",sub,body)
    def var(mm):
        name=mm.group(2); c=open(src+mm.group(1)+".py").read()
        v=re.search(name+r' = """(.*?)"""',c,re.S) or re.search(name+r' = f?"""(.*?)"""',c,re.S)
        return v.group(1).strip("\n")
    body=re.sub(r"\{\{VAR:(q\d+):(\w+)\}\}",var,body)
    assert "{{" not in body, qn
    # fence checks: sql/py/text-free prose fences must be lines contained in code
    code_lines={l.strip() for l in code.splitlines()}
    code_flat=" ".join(l.strip() for l in code.splitlines())
    for fm in re.finditer(r"^```(sql|py)\n(.*?)^```",body,flags=re.M|re.S):
        for l in fm.group(2).splitlines():
            if l.strip() and l.strip() not in code_lines and l.strip() not in code_flat:
                problems.append(f"{qn} prose line not in code: {l.strip()[:80]}")
    out.append(head+body+"\n")
open(base+"scratch/B3P02_Q35-45/answers.md","w").write("\n".join(out))
print("\n".join(problems) or "no problems")
