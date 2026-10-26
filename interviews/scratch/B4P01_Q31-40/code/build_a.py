import re, pathlib
HERE = pathlib.Path(__file__).parent
PART = pathlib.Path("/home/user/case_studies/interviews/Book4_MLOps/Book4_MLOps_Part01.md").read_text().splitlines()

def head(n):
    for i, l in enumerate(PART):
        if l.startswith(f"### Q{n} "):
            assert PART[i+1].startswith("**Asked at:**"), n
            return l + "\n" + PART[i+1]
    raise KeyError(n)

def rd(p):
    t = (HERE / p).read_text().rstrip("\n")
    return t.replace(str(HERE), "<scratch>/code")

def block(lang, *files):
    parts = []
    for f in files:
        body = rd(f)
        parts.append(f"# ---- {f} ----\n{body}" if len(files) > 1 else body)
    return f"```{lang}\n" + "\n\n".join(parts) + "\n```"

def out(*files):
    return "```text\n" + "\n".join(rd(f) for f in files) + "\n```"

ENV = "Python 3.13.17, git 2.43.0, git-filter-repo 2.47.0, scikit-learn 1.9.1, numpy 2.5.3, pytest 9.1.1, hatchling 1.32.4, build 1.6.1"
A = {}
