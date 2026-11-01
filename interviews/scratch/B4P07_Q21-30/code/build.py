import re, sys
from pathlib import Path
HERE = Path(__file__).resolve().parent
PART = Path("/home/user/case_studies/interviews/Book4_MLOps/Book4_MLOps_Part07.md").read_text().splitlines()
out = ["# Book 4 Part 7, Q21-Q30 answers (Wave B)", ""]
for n in range(21, 31):
    i = next(k for k, l in enumerate(PART) if l.startswith(f"### Q{n} "))
    assert PART[i + 1].startswith("**Asked at:**")
    out += [PART[i], PART[i + 1]]
    for line in (HERE / "_tmpl" / f"q{n}.md").read_text().splitlines():
        if line.startswith("@@CODE"):
            _, lang, pref, *files = line.split()
            out.append(f"```{lang}")
            for f in files:
                out.append(f"{pref} --- {f} ---")
                out += (HERE / f).read_text().rstrip("\n").splitlines()
                out.append("")
            if out[-1] == "": out.pop()
            out.append("```")
        elif line.startswith("@@OUT"):
            out += ["```text"] + (HERE / line.split()[1]).read_text().rstrip("\n").splitlines() + ["```"]
        else:
            out.append(line)
    out.append("")
(HERE.parent / "answers.md").write_text("\n".join(out))
