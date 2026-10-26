import re, sys, pathlib
sys.path.insert(0, str(pathlib.Path(__file__).parent))
from bodies1 import B as B1
from bodies2 import B as B2
B = {**B1, **B2}
part = pathlib.Path("/home/user/case_studies/interviews/Book4_MLOps/Book4_MLOps_Part01.md").read_text().split("\n")
out = ["# Book 4 Part 1, Q11-Q20 answers (Wave B)", ""]
for n in range(11, 21):
    i = next(k for k, l in enumerate(part) if l.startswith(f"### Q{n} "))
    assert part[i + 1].startswith("**Asked at:**")
    out += [part[i], part[i + 1], B[n].strip("\n"), "", "---", ""]
pathlib.Path(__file__).with_name("answers.md").write_text("\n".join(out))
