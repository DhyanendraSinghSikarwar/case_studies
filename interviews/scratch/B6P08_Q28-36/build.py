import re, subprocess, os, sys
D = os.path.dirname(os.path.abspath(__file__))
PART = '/home/user/case_studies/interviews/Book6_Scenarios/Book6_Scenarios_Part08.md'
t = open(PART, encoding='utf-8').read()
blocks = {int(m.group(1)): b for b in re.split(r'(?m)^(?=### Q\d+ )', t)[1:] if (m := re.match(r'### Q(\d+) ', b))}
out = []
for n in range(28, 37):
    tf = f'{D}/q{n}.md'; pf = f'{D}/q{n}.py'
    if not (os.path.exists(tf) and os.path.exists(pf)):
        print('skip', n); continue
    lines = blocks[n].split('\n')
    head, asked = lines[0], lines[1]
    assert head.startswith(f'### Q{n} ') and asked.startswith('**Asked at:**')
    code = open(pf).read()
    r = subprocess.run(['python3', '-I', pf], capture_output=True, text=True, cwd=D, timeout=300)
    assert r.returncode == 0, (n, r.stderr)
    body = open(tf, encoding='utf-8').read().strip('\n')
    assert '<<CODE>>' in body and '<<OUTPUT>>' in body
    body = body.replace('<<CODE>>', '```python\n' + code.strip('\n') + '\n```').replace('<<OUTPUT>>', '```text\n' + r.stdout.strip('\n') + '\n```')
    out.append(head + '\n' + asked + '\n' + body + '\n')
    open(f'{D}/out_q{n}.txt', 'w').write(r.stdout)
open(f'{D}/answers.md', 'w', encoding='utf-8').write('\n'.join(out))
print('built', len(out))
