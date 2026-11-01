# Assemble answers.md: run each qNN.py with python3 -I, paste real output into qNN.md placeholders, copy headings verbatim.
import re, subprocess, os, sys
D = os.path.dirname(os.path.abspath(__file__))
part = open(os.path.join(D, '../../Book6_Scenarios/Book6_Scenarios_Part09.md'), encoding='utf-8').read()
blocks = re.split(r'(?m)^(?=### Q\d+ )', part)[1:]
head = {}
for b in blocks:
    n = int(re.match(r'### Q(\d+)', b).group(1))
    lines = b.split('\n')
    asked = [l for l in lines if l.startswith('**Asked at:**')][0]
    head[n] = lines[0] + '\n' + asked
out = []
for n in range(1, 11):
    mdp = os.path.join(D, 'q%02d.md' % n); pyp = os.path.join(D, 'q%02d.py' % n)
    if not (os.path.exists(mdp) and os.path.exists(pyp)): continue
    code = open(pyp).read()
    r = subprocess.run(['python3', '-I', pyp], capture_output=True, text=True, cwd=D, timeout=300, stdin=subprocess.DEVNULL)
    assert r.returncode == 0, (n, r.stderr)
    body = open(mdp, encoding='utf-8').read()
    body = body.replace('@@CODE@@', '```python\n' + code.rstrip() + '\n```').replace('@@OUT@@', '```text\n' + r.stdout.rstrip() + '\n```')
    out.append(head[n] + '\n' + body.strip() + '\n')
open(os.path.join(D, 'answers.md'), 'w', encoding='utf-8').write('\n'.join(out))
print('built', len(out))
