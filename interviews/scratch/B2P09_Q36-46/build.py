import re, subprocess, os
base = "/home/user/case_studies/interviews"
part = open(f"{base}/Book2_GenAI/Book2_GenAI_Part09.md").read().split("\n")
sec = open(f"{base}/scratch/B2P09_Q36-46/body.txt").read()
out = []
for chunk in sec.split("=====")[1:]:
    qn, body = chunk.split("\n", 1); n = int(qn[1:])
    i = next(k for k, l in enumerate(part) if l.startswith(f"### Q{n} "))
    code = open(f"{base}/scratch/B2P09_Q36-46/code/q{n}.py").read().rstrip("\n")
    res = subprocess.run(["python3", "-I", f"{base}/scratch/B2P09_Q36-46/code/q{n}.py"], capture_output=True, text=True, check=True).stdout.rstrip("\n")
    blk = "```python\n" + code + "\n```\n**Output (my run):**\n```\n" + res + "\n```"
    body = body.replace("@@CODE@@", blk).rstrip("\n")
    out.append(part[i] + "\n" + part[i + 1] + "\n" + body + "\n")
open(f"{base}/scratch/B2P09_Q36-46/answers.md", "w").write("\n".join(out))
