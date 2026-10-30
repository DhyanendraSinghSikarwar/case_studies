import glob
T = "\n**Code:**\n```python\n{{CODE}}\n```\n\n**Output (my run):**\n```text\n{{OUTPUT}}\n```\n"
for f in glob.glob("body/q*.md"):
    s = open(f).read()
    if "{{TAIL}}" in s: open(f, "w").write(s.replace("{{TAIL}}", T))
