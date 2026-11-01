import re, subprocess, sys
base = "/home/user/case_studies/interviews/"
part = open(base + "Book3_SQL/Book3_SQL_Part12.md", encoding="utf-8").read().split("\n")
out = []
for n in range(11, 21):
    i = next(k for k, l in enumerate(part) if l.startswith("### Q%d " % n))
    out.append(part[i]); out.append(part[i + 1]); assert part[i + 1].startswith("**Asked at:**")
    prose = open(base + "scratch/B3P12_Q11-20/prose/p%d.txt" % n, encoding="utf-8").read().rstrip("\n")
    codep = base + "scratch/B3P12_Q11-20/code/q%d.py" % n
    code = open(codep, encoding="utf-8").read().rstrip("\n")
    res = subprocess.run(["python3", "-I", codep], capture_output=True, text=True)
    assert res.returncode == 0, res.stderr
    assert "```" not in code and "```" not in res.stdout
    m = re.search(r'executescript\("""(.*?)"""\)', code, re.S)
    schema = "```sql\n" + m.group(1).strip() + "\n```" if m else ""
    prose = prose.replace("@@SCHEMA@@", schema)
    prose = prose.replace("@@CODE@@", "```python\n" + code + "\n```")
    prose = prose.replace("@@OUTPUT@@", "```text\n" + res.stdout.rstrip("\n") + "\n```")
    out.append(prose); out.append("")
open(base + "scratch/B3P12_Q11-20/answers.md", "w", encoding="utf-8").write("\n".join(out))
