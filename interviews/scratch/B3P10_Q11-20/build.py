# usage: build.py run   -> writes work/qNN_final.py (markers stripped) and runs them to work/qNN.out
#        build.py md    -> assembles answers.md
import re, sys, subprocess, pathlib
W = pathlib.Path(__file__).parent / "work"
PART = pathlib.Path(__file__).parents[2] / "Book3_SQL/Book3_SQL_Part10.md"
QS = list(range(11, 21))
MARK = re.compile(r"^\s*(#|--)\s*(<<|>>)\s*(\w*)\s*$")
def strip_markers(src):
    return "\n".join(l for l in src.split("\n") if not MARK.match(l))
def snips(src):
    out, cur, buf = {}, None, []
    for l in src.split("\n"):
        m = MARK.match(l)
        if m:
            if m.group(2) == "<<": cur, buf = m.group(3), []
            else: out[cur] = "\n".join(buf); cur = None
        elif cur is not None: buf.append(l)
    return out
def dedent(s):
    import textwrap; return textwrap.dedent(s).strip("\n")
if sys.argv[1] == "run":
    for q in QS:
        src = (W / f"q{q}.py").read_text()
        (W / f"q{q}_final.py").write_text(strip_markers(src))
        r = subprocess.run(["python3", "-I", str(W / f"q{q}_final.py")], capture_output=True, text=True, cwd=str(W))
        (W / f"q{q}.out").write_text(r.stdout + r.stderr)
        print(q, "rc", r.returncode, r.stderr[-300:])
else:
    part = PART.read_text()
    blocks = []
    for q in QS:
        m = re.search(rf"^(### Q{q} .*)\n(\*\*Asked at:\*\*.*)\n", part, re.M)
        head, asked = m.group(1), m.group(2)
        src = (W / f"q{q}.py").read_text()
        final = strip_markers(src).strip("\n")
        sn = {k: dedent(v) for k, v in snips(src).items()}
        out = (W / f"q{q}.out").read_text().rstrip("\n")
        prose = (W / f"q{q}.md").read_text()
        prose = re.sub(r"\{\{SNIP:(\w+)\}\}", lambda mm: sn[mm.group(1)], prose)
        prose = prose.replace("{{CODE}}", final).replace("{{OUT}}", out)
        blocks.append(head + "\n" + asked + "\n" + prose.strip("\n") + "\n")
    (pathlib.Path(__file__).parent / "answers.md").write_text("\n".join(blocks))
    print("written")
