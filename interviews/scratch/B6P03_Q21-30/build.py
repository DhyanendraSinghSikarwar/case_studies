import re, subprocess, os, sys
here = os.path.dirname(os.path.abspath(__file__))
part = open(os.path.join(here, '../../Book6_Scenarios/Book6_Scenarios_Part03.md'), encoding='utf-8').read()
blocks = re.split(r'(?m)^(?=### Q\d+ )', part)[1:]
head = {}
for b in blocks:
    n = int(re.match(r'### Q(\d+) ', b).group(1))
    lines = b.split('\n')
    head[n] = (lines[0], lines[1])
out = []; missing = []
for n in range(21, 31):
    bp = os.path.join(here, f'q{n}.md'); cp = os.path.join(here, f'q{n}.py')
    if not (os.path.exists(bp) and os.path.exists(cp)): missing.append(n); continue
    body = open(bp, encoding='utf-8').read().strip('\n')
    code = open(cp, encoding='utf-8').read().rstrip('\n')
    r = subprocess.run(['python3', '-I', cp], capture_output=True, text=True, cwd='/tmp')
    if r.returncode: print('FAIL', n, r.stderr[-300:]); sys.exit(1)
    body = body.replace('{{CODE}}', '```python\n' + code + '\n```').replace('{{OUTPUT}}', '```text\n' + r.stdout.rstrip('\n') + '\n```')
    out.append(head[n][0] + '\n' + head[n][1] + '\n' + body + '\n')
open(os.path.join(here, 'answers.md'), 'w', encoding='utf-8').write('\n'.join(out))
print('built', len(out), 'missing', missing)
