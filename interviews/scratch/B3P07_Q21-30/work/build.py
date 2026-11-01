import re, subprocess, textwrap, pathlib
W = pathlib.Path(__file__).parent
PART = pathlib.Path("/home/user/case_studies/interviews/Book3_SQL/Book3_SQL_Part07.md").read_text().split("\n")
OUTFILE = W.parent / "answers.md"

def head(n):
    for i, l in enumerate(PART):
        if l.startswith(f"### Q{n} "):
            assert PART[i+1].startswith("**Asked at:**")
            return l + "\n" + PART[i+1]
    raise KeyError(n)

def parts(n):
    src = (W / f"q{n}.py").read_text()
    ns = {}
    exec(src.split("con = sqlite3.connect")[0], ns)
    m = re.search(r"# pd:main\n(.*?)# pd:end", src, re.S)
    pd_txt = textwrap.dedent(m.group(1)).rstrip() if m else ""
    return src, ns, pd_txt

def run(n):
    r = subprocess.run(["python3", "-I", str(W / f"q{n}.py")], capture_output=True, text=True, cwd=str(W))
    assert r.returncode == 0, r.stderr
    return r.stdout.rstrip()

T = {}
exec((W / "templates.py").read_text())

blocks = []
for n in range(21, 31):
    src, ns, pd_txt = parts(n)
    sqlkey = {25: "SQL_A"}.get(n, "SQL_MAIN")
    body = T[n]
    sqltxt = ns[sqlkey].strip("\n")
    body = body.replace("@@SCHEMA@@", "```sql\n" + ns["SCHEMA"].strip("\n") + "\n```")
    body = body.replace("@@SQL@@", "```sql\n" + sqltxt + "\n```")
    body = body.replace("@@PD@@", "```py\n" + pd_txt + "\n```")
    body = body.replace("@@CODE@@", "```python\n" + src.rstrip() + "\n```")
    body = body.replace("@@OUT@@", "```text\n" + run(n) + "\n```")
    blocks.append(head(n) + "\n" + body.strip("\n") + "\n")
OUTFILE.write_text("\n".join(blocks))
print("written", OUTFILE)
