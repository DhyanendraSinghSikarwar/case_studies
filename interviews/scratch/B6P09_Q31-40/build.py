import os, re, subprocess, sys
D = os.path.dirname(os.path.abspath(__file__))
os.chdir(D)
part = open('../../Book6_Scenarios/Book6_Scenarios_Part09.md', encoding='utf-8').read()
blocks = {int(re.match(r'### Q(\d+)', b).group(1)): b for b in re.split(r'(?m)^(?=### Q\d+ )', part)[1:]}
out = []
for n in range(31, 41):
    head = blocks[n].split('\n')
    assert head[0].startswith(f'### Q{n} ') and head[1].startswith('**Asked at:**')
    body = open(f'q{n}_body.md', encoding='utf-8').read().rstrip('\n')
    code = open(f'q{n}_code.py', encoding='utf-8').read().rstrip('\n')
    r = subprocess.run(['python3', '-I', f'q{n}_code.py'], capture_output=True, text=True, timeout=300, cwd=D)
    assert r.returncode == 0, (n, r.stderr)
    body = body.replace('<<CODE>>', '**Code:**\n```python\n' + code + '\n```')
    body = body.replace('<<OUTPUT>>', '**Output (my run):**\n```\n' + r.stdout.rstrip('\n') + '\n```')
    out.append('\n'.join(head[:2]) + '\n' + body + '\n')
open('answers.md', 'w', encoding='utf-8').write('\n'.join(out))
print('built', len(out))
