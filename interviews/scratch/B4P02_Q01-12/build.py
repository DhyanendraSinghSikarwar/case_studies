import re, subprocess, os
ROOT = "/home/user/case_studies/interviews"
OUT = f"{ROOT}/scratch/B4P02_Q01-12"
CODE = f"{OUT}/code"
part = open(f"{ROOT}/Book4_MLOps/Book4_MLOps_Part02.md").read().splitlines()

def head(n):
    for i, l in enumerate(part):
        if l.startswith(f"### Q{n} "):
            assert part[i+1].startswith("**Asked at:**")
            return l, part[i+1]
    raise KeyError(n)

COMMENT = "#"
def code_block(lang, files, d):
    parts = []
    for f in files:
        txt = open(f"{CODE}/{d}/{f}").read().rstrip("\n")
        parts.append(f"{COMMENT} ---- {f} ----\n{txt}")
    return f"```{lang}\n" + "\n\n".join(parts) + "\n```"

def run(d, cmd):
    r = subprocess.run(["bash", "-c", cmd + " 2>&1"], cwd=f"{CODE}/{d}", capture_output=True, text=True)
    out = re.sub(r"\x1b\[[0-9;]*m", "", r.stdout).rstrip("\n")
    return f"$ {cmd}\n{out}"

def output_block(d, cmds):
    return "```text\n" + "\n\n".join(run(d, c) for c in cmds) + "\n```"

def render(n, d, say, explain, example, code, cmds, notrun, followups, mistakes):
    h, a = head(n)
    code_txt = "\n\n".join(code_block(l, fs, d) for l, fs in code)
    out = [h, a, f"**Say this first (1 line):** {say}", "", "**Then explain:**", explain.strip(), "",
           "**Example:** " + example.strip(), "", "**Code:**", code_txt, "",
           "**Output (my run):**", notrun.strip(), "", output_block(d, cmds), "",
           "**Follow-ups:**", followups.strip(), "", "**Common mistakes:**", mistakes.strip(), ""]
    return "\n".join(out)

HC = "hadolint {f}; echo \"hadolint exit code: $?\""
answers = []
exec(open(f"{OUT}/content.py").read())
open(f"{OUT}/answers.md", "w").write("\n".join(answers))
print("written", len(answers))
