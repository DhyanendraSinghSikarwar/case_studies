import pathlib, subprocess, re
ROOT = pathlib.Path(__file__).parent
CODE = ROOT / "code"
PART = pathlib.Path("/home/user/case_studies/interviews/Book4_MLOps/Book4_MLOps_Part07.md").read_text().splitlines()

def head(n):
    for i, l in enumerate(PART):
        if l.startswith("### Q%d " % n):
            assert PART[i+1].startswith("**Asked at:**")
            return l + "\n" + PART[i+1]
    raise KeyError(n)

def block(lang, d, files, cmt="#"):
    parts = []
    for f in files:
        txt = (CODE / d / f).read_text().rstrip("\n")
        assert "```" not in txt
        parts.append(txt if len(files) == 1 else f"{cmt} ===== {f} =====\n{txt}")
    return "```%s\n%s\n```" % (lang, "\n\n".join(parts))

exec((ROOT / "prose.py").read_text())

out = []
for n in range(1, 11):
    p = Q[n]; d = "q%02d" % n
    code = []
    for lang, files in p["code"]:
        label = {"yaml": "Workflow YAML", "python": "Python", "shell": "Shell (venv with actionlint-py, check-jsonschema, pytest, PyYAML on PATH)",
                 "json": "JSON", "ini": "pytest.ini"}[lang]
        code.append(label + ":\n" + block(lang, d, files))
    o = (ROOT / "out" / (d + ".txt")).read_text().rstrip("\n")
    assert "```" not in o
    text = (head(n) + "\n"
        + "**Say this first (1 line):** " + p["say"] + "\n\n"
        + "**Then explain:**\n" + p["explain"].strip("\n") + "\n\n"
        + "**Example:** " + p["example"].strip("\n") + "\n\n"
        + "**Code:**\n" + "\n\n".join(code) + "\n\n"
        + "**Output (my run):** " + p["outnote"] + "\n```text\n" + o + "\n```\n\n"
        + "**Follow-ups:**\n" + p["follow"].strip("\n") + "\n\n"
        + "**Common mistakes:**\n" + p["mistakes"].strip("\n") + "\n")
    out.append(text)
(ROOT / "answers.md").write_text("\n".join(out))
print("built", len(out))
