import re, subprocess, os, glob, sys
os.chdir('/home/user/case_studies/interviews')
D = 'scratch/B6P09_Q21-30'
part = open('Book6_Scenarios/Book6_Scenarios_Part09.md', encoding='utf-8').read()
blocks = {int(re.match(r'### Q(\d+)', b).group(1)): b for b in re.split(r'(?m)^(?=### Q\d+ )', part)[1:]}
out = ''
for n in range(21, 31):
    f = f'{D}/q{n}.md'
    if not os.path.exists(f):
        continue
    lines = blocks[n].split('\n')
    head = lines[0] + '\n' + lines[1] + '\n'
    body = open(f, encoding='utf-8').read()
    code = open(f'{D}/q{n}.py', encoding='utf-8').read()
    r = subprocess.run(['python3', '-I', f'{D}/q{n}.py'], capture_output=True, text=True)
    assert r.returncode == 0, (n, r.stderr)
    body = body.replace('{{CODE}}', '```python\n' + code.rstrip() + '\n```').replace('{{OUTPUT}}', '```text\n' + r.stdout.rstrip() + '\n```')
    out += head + body.rstrip() + '\n\n'
open(f'{D}/answers.md', 'w', encoding='utf-8').write(out)
subprocess.run('find scratch/B6P09_Q21-30 -name __pycache__ -exec rm -rf {} +', shell=True)
print('built', len(out))
