import re, pathlib
R = pathlib.Path("/home/user/case_studies/interviews"); S = R / "scratch/B4P09_Q10-18"
part = (R / "Book4_MLOps/Book4_MLOps_Part09.md").read_text().split("\n")
def head(q):
    for i, l in enumerate(part):
        if l.startswith(f"### Q{q} "):
            asked = next(x for x in part[i+1:i+4] if x.startswith("**Asked at:**"))
            return l, asked
out = ["# Book 4 Part 9, Q10-Q18 answers (Wave B)\n"]
for q in range(10, 19):
    body = (S / f"parts/q{q}.md").read_text()
    body = re.sub(r"\{\{CODE:(.+?)\}\}", lambda m: (S / "code" / m.group(1)).read_text().rstrip(), body)
    body = re.sub(r"\{\{OUT:(.+?)\}\}", lambda m: (S / "code" / m.group(1)).read_text().rstrip(), body)
    h, a = head(q)
    out.append(f"{h}\n{a}\n{body}\n")
(S / "answers.md").write_text("\n".join(out))
