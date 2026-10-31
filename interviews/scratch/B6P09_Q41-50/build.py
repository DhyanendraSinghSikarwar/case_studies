import os, re, subprocess, sys
os.chdir('/home/user/case_studies/interviews')
D = 'scratch/B6P09_Q41-50'
part = open('Book6_Scenarios/Book6_Scenarios_Part09.md', encoding='utf-8').read()
blocks = {int(m.group(1)): m.group(0) for m in re.finditer(r'(?m)^### Q(\d+) .*\n\*\*Asked at:\*\*.*\n', part)}
out = ''
for n in range(41, 51):
    t = f'{D}/q{n}.md'; c = f'{D}/q{n}.py'
    if not (os.path.exists(t) and os.path.exists(c)):
        print('missing', n); continue
    code = open(c).read()
    r = subprocess.run(['python3', '-I', f'q{n}.py'], cwd=D, capture_output=True, text=True, timeout=120)
    assert r.returncode == 0, (n, r.stderr)
    body = open(t).read().replace('@@CODE@@', '```python\n' + code.rstrip() + '\n```').replace('@@OUTPUT@@', '```text\n' + r.stdout.rstrip() + '\n```')
    out += blocks[n] + body.rstrip() + '\n\n'
open(f'{D}/answers.md', 'w', encoding='utf-8').write(out)
print('built', out.count('### Q'))
