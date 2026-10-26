import re, subprocess, shutil, tempfile, os, sys
sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
from content import C, OUT
base = os.path.dirname(os.path.abspath(__file__))
part = open("/home/user/case_studies/interviews/Book4_MLOps/Book4_MLOps_Part03.md", encoding="utf-8").read().split("\n")
def heading(n):
    i = next(k for k, l in enumerate(part) if l.startswith(f"### Q{n} "))
    assert part[i+1].startswith("**Asked at:**")
    return part[i], part[i+1]
LANG = {"yaml": "yaml", "python": "python", "json": "text", "text": "text"}
out = []
for n in range(1, 11):
    c, o = C[n], OUT[n]
    qd = os.path.join(base, "code", f"q{n:02d}")
    h, a = heading(n)
    out += [h, a, f"**Say this first (1 line):** {c['say']}", "", "**Then explain:**", c["explain"], "", f"**Example:** {c['example']}", ""]
    out.append("**Code:**")
    for lang in ("yaml", "json", "text", "python"):
        files = o.get(lang)
        if not files: continue
        body = []
        for f in files:
            cm = "#" if lang in ("yaml", "python", "text") else None
            txt = open(os.path.join(qd, f)).read().rstrip("\n")
            if lang == "json": body.append(f"// ---- {f} ----\n{txt}" if False else txt)
            else: body.append(f"# ---- {f} ----\n{txt}")
        out += [f"```{LANG[lang]}", "\n\n".join(body), "```"]
    sh = ["# these ran (from the code/ folder of this answer):"] + o["cmds"] + ["", "# NOT EXECUTED here (no cluster, no kubectl):"] + ["# " + x for x in o["cluster"]]
    if c.get("code_note"): sh += ["# " + c["code_note"]]
    out += ["```bash", "\n".join(sh), "```", ""]
    # run
    tmp = tempfile.mkdtemp()
    shutil.copytree(qd, tmp, dirs_exist_ok=True)
    res = []
    for cmd in o["cmds"]:
        p = subprocess.run(cmd, shell=True, cwd=tmp, capture_output=True, text=True)
        assert p.returncode == 0, (n, cmd, p.stdout, p.stderr)
        res.append(f"$ {cmd}\n{(p.stdout + p.stderr).rstrip()}")
    shutil.rmtree(tmp)
    out += ["**Output (my run):**", "```text", "\n\n".join(res), "```", c["notexec"], ""]
    out.append("**Follow-ups:**")
    out += [f"- **{q}** {a_}" for q, a_ in c["follow"]]
    out += ["", "**Common mistakes:**", c["mistakes"], "", "---", ""]
open(os.path.join(base, "answers.md"), "w", encoding="utf-8").write("\n".join(out))
print("ok")
