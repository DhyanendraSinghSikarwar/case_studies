import ast, re, subprocess, sys
base = "/home/user/case_studies/interviews/"
part = open(base + "Book3_SQL/Book3_SQL_Part10.md", encoding="utf-8").read().split("\n")
heads = {}
for i, l in enumerate(part):
    m = re.match(r"### Q(\d+) ", l)
    if m and 1 <= int(m.group(1)) <= 10:
        assert part[i + 1].startswith("**Asked at:**")
        heads[int(m.group(1))] = l + "\n" + part[i + 1]
here = base + "scratch/B3P10_Q01-10/"
out = []
for n in range(1, 11):
    tag = f"{n:02d}"
    code = open(here + f"code/q{tag}.py", encoding="utf-8").read().rstrip("\n")
    res = subprocess.run(["python3", "-I", here + f"code/q{tag}.py"], capture_output=True, text=True, cwd="/tmp")
    assert res.returncode == 0, (n, res.stderr)
    output = res.stdout.rstrip("\n")
    assert "```" not in code and "```" not in output
    consts = {}
    for node in ast.walk(ast.parse(code)):
        if isinstance(node, ast.Assign) and len(node.targets) == 1 and isinstance(node.targets[0], ast.Name):
            try:
                v = ast.literal_eval(node.value)
            except Exception:
                continue
            if isinstance(v, str):
                consts[node.targets[0].id] = v.strip("\n")
    t = open(here + f"prose/p{tag}.md", encoding="utf-8").read().rstrip("\n")
    t = t.replace("{{HEAD}}", heads[n])
    t = re.sub(r"\{\{(?:SQL|EXPR):(\w+)\}\}", lambda m: consts[m.group(1)], t)
    t = t.replace("{{CODE}}", "```python\n" + code + "\n```").replace("{{OUT}}", output)
    # verify prose sql/py fences against the code (line by line, comments stripped)
    norm = lambda s: re.sub(r"\s+", " ", s)
    ncode = norm(code)
    for m in re.finditer(r"```(sql|py)\n(.*?)\n```", t, re.S):
        for line in m.group(2).split("\n"):
            line = re.sub(r"\s+--.*$", "", line).strip()
            line = re.sub(r"\s+#.*$", "", line).strip()
            if line and norm(line) not in ncode:
                print("Q%d fence line not in code:" % n, line)
    assert t.count("ANSWER_PENDING") == 0
    out.append(t)
open(here + "answers.md", "w", encoding="utf-8").write("\n\n".join(out) + "\n")
