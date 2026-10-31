import re, subprocess, pathlib
base = pathlib.Path("/home/user/case_studies/interviews/scratch/B3P01_Q13-23")
part = pathlib.Path("/home/user/case_studies/interviews/Book3_SQL/Book3_SQL_Part01.md").read_text().split("\n")
heads = {}
for i, l in enumerate(part):
    m = re.match(r"### Q(\d+) ", l)
    if m and 13 <= int(m.group(1)) <= 23:
        assert part[i + 1].startswith("**Asked at:**")
        heads[int(m.group(1))] = (l, part[i + 1])
tpl = (base / "template.txt").read_text()
blocks = re.split(r"^@@Q(\d+)\n", tpl, flags=re.M)
out = []
for k in range(1, len(blocks), 2):
    n = int(blocks[k]); body = blocks[k + 1].rstrip() + "\n"
    code = (base / "code" / f"q{n}.py").read_text().rstrip("\n")
    res = subprocess.run(["python3", "-I", str(base / "code" / f"q{n}.py")], capture_output=True, text=True, check=True).stdout.rstrip("\n")
    m = re.search(r'"""(.*?)"""', code, re.S)
    sch = m.group(1).strip("\n") if m else ""
    body = body.replace("{{SCHEMA:q%d}}" % n, "```sql\n" + sch + "\n```")
    body = body.replace("{{CODE:q%d}}" % n, "```python\n" + code + "\n```")
    body = body.replace("{{OUT:q%d}}" % n, "```text\n" + res + "\n```")
    out.append(heads[n][0] + "\n" + heads[n][1] + "\n" + body)
(base / "answers.md").write_text("\n".join(out))
