import re, subprocess, sys, os
HERE=os.path.dirname(os.path.abspath(__file__))
PART="/home/user/case_studies/interviews/Book3_SQL/Book3_SQL_Part07.md"
OUT=os.path.join(HERE,"..","answers.md")
lines=open(PART,encoding="utf-8").read().split("\n")
def head(n):
    for i,l in enumerate(lines):
        if l.startswith(f"### Q{n} "):
            assert lines[i+1].startswith("**Asked at:**")
            return l, lines[i+1]
    raise KeyError(n)
def strval(py,name):
    m=re.search(r'^'+name+r' = """(.*?)"""',py,re.S|re.M)
    assert m,name
    return m.group(1).strip("\n")
def run(n):
    p=subprocess.run([sys.executable,"-I",os.path.join(HERE,f"q{n}.py")],capture_output=True,text=True,cwd=HERE)
    if p.returncode: print(p.stderr); raise SystemExit(f"q{n} failed")
    return p.stdout.rstrip("\n")
blocks=[]
qs=[int(a) for a in sys.argv[1:]] or list(range(1,11))
for n in qs:
    py=open(os.path.join(HERE,f"q{n}.py"),encoding="utf-8").read().rstrip("\n")
    md=open(os.path.join(HERE,f"q{n}.md"),encoding="utf-8").read().strip("\n")
    out=run(n)
    md=md.replace("{{CODE}}","```python\n"+py+"\n```")
    md=md.replace("{{OUTPUT}}","```text\n"+out+"\n```")
    md=re.sub(r"\{\{SQL:(\w+)\}\}",lambda m:"```sql\n"+strval(py,m.group(1))+"\n```",md)
    def pd_(m):
        mm=re.search(r"# pd:main\n(.*?)# pd:end",py,re.S); assert mm
        return "```py\n"+mm.group(1).rstrip("\n")+"\n```"
    md=md.replace("{{PD}}",pd_(None))
    h,a=head(n)
    blocks.append(h+"\n"+a+"\n"+md)
open(OUT,"w",encoding="utf-8").write("\n\n".join(blocks)+"\n")
print("wrote",len(blocks))
