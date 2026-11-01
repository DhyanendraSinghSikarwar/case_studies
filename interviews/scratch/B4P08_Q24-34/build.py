import pathlib
ROOT = pathlib.Path(__file__).parent
CODE = ROOT / "code"
PART = pathlib.Path("/home/user/case_studies/interviews/Book4_MLOps/Book4_MLOps_Part08.md").read_text().splitlines()

def head(n):
    for i, l in enumerate(PART):
        if l.startswith("### Q%d " % n):
            assert PART[i+1].startswith("**Asked at:**")
            return l + "\n" + PART[i+1]
    raise KeyError(n)

def block(lang, d, files):
    parts = []
    for f in files:
        txt = (CODE / d / f).read_text().rstrip("\n")
        assert "```" not in txt
        parts.append(txt if len(files) == 1 else f"# ===== {f} =====\n{txt}")
    return "```%s\n%s\n```" % (lang, "\n\n".join(parts))

exec((ROOT / "prose.py").read_text())
LABEL = {"python": "Python (python3 -I in a venv with numpy, scipy, pandas, scikit-learn, PyYAML as needed)", "yaml": "YAML",
         "markdown": "Post-mortem template"}
out = []
for n in range(24, 35):
    p = Q[n]; d = "q%02d" % n
    code = [LABEL[lang] + ":\n" + block(lang, d, files) for lang, files in p["code"]]
    o = (ROOT / "out" / (d + ".txt")).read_text().rstrip("\n")
    assert "```" not in o
    out.append(head(n) + "\n"
        + "**Say this first (1 line):** " + p["say"] + "\n\n"
        + "**Then explain:**\n" + p["explain"].strip("\n") + "\n\n"
        + "**Example:** " + p["example"].strip("\n") + "\n\n"
        + "**Code:**\n" + "\n\n".join(code) + "\n\n"
        + "**Output (my run):** " + p["outnote"] + "\n```text\n" + o + "\n```\n\n"
        + "**Follow-ups:**\n" + p["follow"].strip("\n") + "\n\n"
        + "**Common mistakes:**\n" + p["mistakes"].strip("\n") + "\n")
(ROOT / "answers.md").write_text("\n".join(out))
print("wrote", len(out))
