# builds ../answers.md: copies Q heading + Asked at verbatim from the part file, embeds each script and its real output.
import os, re, subprocess, sys
HERE = os.path.dirname(os.path.abspath(__file__))
PART = "/home/user/case_studies/interviews/Book4_MLOps/Book4_MLOps_Part10.md"
PY = "/tmp/claude-0/b10p10/v/bin/python"
lines = open(PART, encoding="utf-8").read().split("\n")
head = {}
for i, l in enumerate(lines):
    m = re.match(r"### Q(\d+) ", l)
    if m and 31 <= int(m.group(1)) <= 40:
        assert lines[i + 1].startswith("**Asked at:**"); head[int(m.group(1))] = (l, lines[i + 1])
sys.path.insert(0, HERE)
from texts import A
out = []
for n in range(31, 41):
    h, asked = head[n]; t = A[n]
    code = open(os.path.join(HERE, f"q{n}.py"), encoding="utf-8").read().rstrip()
    res = subprocess.run([PY, "-I", os.path.join(HERE, f"q{n}.py")], capture_output=True, text=True, cwd="/tmp/claude-0/b10_q31_40")
    assert res.returncode == 0, (n, res.stderr[-500:])
    output = re.sub(r"[0-9a-f]{8}-[0-9a-f]{4}-[0-9a-f]{4}-[0-9a-f]{4}-[0-9a-f]{12}", "<uuid>", res.stdout.rstrip()) if n == 38 else res.stdout.rstrip()
    if n == 38: output = re.sub(r"'KeyId': '[^']*'", "'KeyId': '<id>'", output); output = re.sub(r"'DeletionDate': '[^']*'", "'DeletionDate': '<date>'", output)
    out.append("\n".join([h, asked, "**Say this first (1 line):** " + t["say"], "", "**Then explain:**", *["- " + b for b in t["explain"]], "",
        "**Example:** " + t["example"], "", "**Code:** " + t["codenote"] + " Run with `python3 -I` from the venv (boto3 1.43.118, moto 5.2.4); fake keys only.",
        "```python", code, "```", "", "**Output (my run):** " + t["outnote"], "```text", output, "```", "",
        "**Follow-ups:**", *["- " + b for b in t["follow"]], "", "**Common mistakes:**", *["- " + b for b in t["mistakes"]], "", ""]))
open(os.path.join(HERE, "..", "answers.md"), "w", encoding="utf-8").write("\n".join(out))
print("wrote", len(out), "answers")
