import os, re, subprocess, sys
HERE = os.path.dirname(os.path.abspath(__file__))
PART = '/home/user/case_studies/interviews/Book6_Scenarios/Book6_Scenarios_Part05.md'
txt = open(PART, encoding='utf-8').read()
blocks = {int(re.match(r'### Q(\d+) ', b).group(1)): b for b in re.split(r'(?m)^(?=### Q\d+ )', txt)[1:]}
out = []
for n in range(23, 34):
    b = blocks[n].split('\n')
    if not os.path.exists(f'{HERE}/q{n}.md'): continue
    head, asked = b[0], b[1]
    assert asked.startswith('**Asked at:**')
    body = open(f'{HERE}/q{n}.md', encoding='utf-8').read().strip('\n')
    code = open(f'{HERE}/q{n}.py', encoding='utf-8').read().rstrip('\n')
    r = subprocess.run(['python3', '-I', f'q{n}.py'], cwd=HERE, capture_output=True, text=True, timeout=300, stdin=subprocess.DEVNULL)
    assert r.returncode == 0, (n, r.stderr[-400:])
    body = body.replace('{{CODE}}', code).replace('{{OUTPUT}}', r.stdout.rstrip('\n'))
    out.append(f'{head}\n{asked}\n{body}\n')
open(f'{HERE}/answers.md', 'w', encoding='utf-8').write('\n'.join(out))
subprocess.run('rm -rf __pycache__', shell=True, cwd=HERE)
print('built', len(out))
