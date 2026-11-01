import re, importlib.util, sys
PART = "/home/user/case_studies/interviews/Book3_SQL/Book3_SQL_Part08.md"
part = open(PART).read()
P = {}
for f in ("prose_a", "prose_b", "prose_c"):
    spec = importlib.util.spec_from_file_location(f, f + ".py"); m = importlib.util.module_from_spec(spec)
    spec.loader.exec_module(m); P.update(m.P)

def head(n):
    mm = re.search(r"^(### Q%d .*)\n(\*\*Asked at:\*\*.*)\n" % n, part, re.M)
    return mm.group(1), mm.group(2)

def const(code, name):
    mm = re.search(r'^%s = """(.*?)"""' % name, code, re.S | re.M)
    assert mm, name
    return mm.group(1).strip("\n")

blocks = []
for n in range(23, 34):
    p = P[n]
    h, a = head(n)
    code = open("q%d.py" % n).read()
    out = open("out%d.txt" % n).read().rstrip("\n")
    assert "```" not in code and "```" not in out
    if p["schema"]:
        schema = const(code, "SCHEMA")
    else:
        schema = re.search(r'executescript\("""(.*?)"""\)', code, re.S).group(1).strip("\n")
    s = [h, a, "**Say this first (1 line):** " + p["say"], ""]
    s += ["**Schema and sample data:** " + p["schema_note"], "```sql", schema, "```", ""]
    s += ["**SQL answer:** " + p["sqlnote"]]
    for name in p["sqls"]:
        s += ["```sql", const(code, name), "```"]
    if p["sqlafter"]:
        s += [p["sqlafter"]]
    s += [""]
    pdm = re.search(r"# pd:main\n(.*?)# pd:end", code, re.S)
    if pdm:
        s += ["**pandas answer:** " + p["pdnote"], "```py", pdm.group(1).rstrip("\n"), "```", ""]
    else:
        s += ["**pandas answer:** " + p["pdnote"], ""]
    s += ["**Example:** walk through the sample data by hand.", p["example"], ""]
    s += ["**Code:** run with `python3 -I`. The SQL and pandas results are asserted equal after ordering as noted in the comment above each assert; everything printed below comes from the run.",
          "```python", code.rstrip("\n"), "```", ""]
    s += ["**Output (my run):**", "```text", out, "```", ""]
    s += ["**Edge cases:**", p["edge"], ""]
    s += ["**Then explain:**", p["explain"], ""]
    s += ["**Follow-ups:**", p["fu"], ""]
    s += ["**Common mistakes:**", p["mist"], "", ""]
    blocks.append("\n".join(s))
open("../answers.md", "w").write("\n".join(blocks).rstrip("\n") + "\n")
print("built", len(blocks))
