import re, subprocess, textwrap, pathlib
ROOT = pathlib.Path(__file__).parent
PART = pathlib.Path("/home/user/case_studies/interviews/Book3_SQL/Book3_SQL_Part12.md").read_text().splitlines()

def head(n):
    for i, l in enumerate(PART):
        if l.startswith("### Q%d " % n):
            assert PART[i+1].startswith("**Asked at:**")
            return l + "\n" + PART[i+1]
    raise KeyError(n)

def schema(code):
    m = re.search(r'executescript\("""(.*?)"""\)', code, re.S)
    return textwrap.dedent(m.group(1)).strip("\n")

def sqlvar(code, name):
    m = re.search(r'^%s = """(.*?)"""' % name, code, re.S | re.M)
    return textwrap.dedent(m.group(1)).strip("\n")

def between(code, a, b):
    i = code.index(a); j = code.index(b, i)
    return code[i:j].rstrip("\n")

def scoring(pts, setname, q, full, partial):
    f = lambda x: ("%g" % round(pts * x, 2))
    return ("- **Scoring note (Set %s, %s, %d pts, by the part header rubric):** %s points for a correct query on the seed data (%s), "
            "%s for naming and handling the seeded edge case, %s for the pandas version, %s for stating the assumption before coding, "
            "%s for a one-line check. Partial credit: %s") % (setname, q, pts, f(.4), full, f(.2), f(.2), f(.1), f(.1), partial)

def run(n):
    r = subprocess.run(["python3", "-I", str(ROOT / "code" / ("q%02d.py" % n))], capture_output=True, text=True, cwd="/tmp")
    assert r.returncode == 0, r.stderr
    return r.stdout.rstrip("\n")

Q = {}
exec(open(ROOT / "prose.py").read())

out = []
for n in range(1, 11):
    code = (ROOT / "code" / ("q%02d.py" % n)).read_text().rstrip("\n")
    assert "```" not in code
    ns = dict(code=code, run_out=run(n))
    p = Q[n]
    txt = p["body"]
    for key, fn in p.get("subs", {}).items():
        txt = txt.replace("<<%s>>" % key, fn(code))
    txt = txt.replace("<<CODE>>", code).replace("<<OUTPUT>>", ns["run_out"])
    assert "<<" not in txt, (n, re.findall(r"<<[^>]*>>", txt))
    out.append(head(n) + "\n" + txt.strip("\n") + "\n")
(ROOT / "answers.md").write_text("\n".join(out))
print("built", len(out))
