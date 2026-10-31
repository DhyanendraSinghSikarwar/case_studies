import re, pathlib
root = pathlib.Path(__file__).parent
part = open("/home/user/case_studies/interviews/Book4_MLOps/Book4_MLOps_Part04.md", encoding="utf-8").read().split("\n")
HINT = ("To track the changes with git", "git add dvc.lock", "To enable auto staging", "dvc config core.autostage", "Use `dvc push`")
def head(n):
    i = next(k for k, l in enumerate(part) if l.startswith(f"### Q{n} "))
    assert part[i + 1].startswith("**Asked at:**")
    return part[i], part[i + 1]
def code(m):
    spec = m.group(1)
    if spec.startswith("yaml:"):
        return "\n\n".join((root / "code" / p).read_text().rstrip() for p in spec[5:].split("|"))
    return (root / "code" / spec).read_text().rstrip()
def out(m):
    t = (root / "code" / m.group(1)).read_text().rstrip()
    if m.group(1) in ("q3.out", "q4.out", "q5.out"):
        lines = [l for l in t.split("\n") if not l.strip().startswith(HINT) and not l.strip().startswith("git add ")]
        t = re.sub(r"\n{3,}", "\n\n", "\n".join(lines))
    return t
res = ["# Book 4 Part 4, Q1-Q10 answers (Wave B)\n"]
for n in range(1, 11):
    h, a = head(n)
    b = (root / "bodies" / f"q{n}.md").read_text()
    b = re.sub(r"@@CODE:(.+?)@@", code, b)
    b = re.sub(r"@@OUT:(.+?)@@", out, b)
    b = re.sub(r"\n(\*\*(Then explain|Example|Code|Output \(my run\)|Follow-ups|Common mistakes):\*\*)", r"\n\n\1", b)
    b = re.sub(r"\n{3,}", "\n\n", b)
    res += [h, a, b.strip(), "\n"]
(root / "answers.md").write_text("\n".join(res), encoding="utf-8")
