import ast, re, sys
ROOT = "/home/user/case_studies/interviews"
part = open(ROOT + "/Book3_SQL/Book3_SQL_Part11.md", encoding="utf-8").read().split("\n")
def head(n):
    i = next(k for k, l in enumerate(part) if l.startswith("### Q%d " % n))
    assert part[i + 1].startswith("**Asked at:**")
    return part[i], part[i + 1]

def sqlconst(code, names):
    tree = ast.parse(code); out = []
    for nm in names:
        for node in tree.body:
            if isinstance(node, ast.Assign) and isinstance(node.targets[0], ast.Name) and node.targets[0].id == nm:
                out.append(node.value.value.strip("\n"))
    assert len(out) == len(names), names
    return "\n\n".join(out)

def func(code, name):
    tree = ast.parse(code); lines = code.split("\n")
    for node in tree.body:
        if isinstance(node, ast.FunctionDef) and node.name == name:
            return "\n".join(lines[node.lineno - 1:node.end_lineno])
    raise KeyError(name)

def block(lang, txt):
    assert "```" not in txt
    return "```%s\n%s\n```" % (lang, txt.rstrip("\n"))

def make(n, Q):
    h, a = head(n)
    code = open("code/q%d.py" % n, encoding="utf-8").read()
    out = open("code/q%d.out" % n, encoding="utf-8").read()
    if Q.get("sql_text"):
        for ln in Q["sql_text"].split("\n"):
            if ln.strip():
                assert ln.strip() in code, (n, ln)
    s = [h, a, "**Say this first (1 line):** " + Q["say"], "",
         "**Schema and sample data:**", block("sql", Q["schema"]), "",
         "**SQL answer:** " + Q["sql_intro"], block("sql", sqlconst(code, Q["sql"]) if Q.get("sql") else Q["sql_text"]), "",
         "**pandas answer:** " + Q["pd_intro"]]
    pd_txt = Q["pd"] if isinstance(Q["pd"], str) else func(code, Q["pd"][0])
    if isinstance(Q["pd"], str):
        assert pd_txt in code, (n, "pandas snippet not in code")
    s += [block("py", pd_txt), "", "**Example:** " + Q["example"], "",
          "**Code:** run with `python3 -I`.", block("python", code), "",
          "**Output (my run):**", block("text", out), "",
          "**Edge cases:**"] + ["- " + x for x in Q["edge"]] + ["", "**Then explain:**"] + ["- " + x for x in Q["explain"]] + \
         ["", "**Follow-ups:**"] + ["- " + x for x in Q["follow"]] + ["", "**Common mistakes:**"] + ["- " + x for x in Q["mist"]] + [""]
    return "\n".join(s)

sys.path.insert(0, "."); import prose
body = "\n".join(make(n, prose.Q[n]) for n in range(19, 28))
open("answers.md", "w", encoding="utf-8").write(body)
print("written", len(body))
