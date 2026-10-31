import os, re, subprocess, tempfile
os.chdir('/home/user/case_studies/interviews')
D = 'scratch/B6P08_Q10-18'
part = open('Book6_Scenarios/Book6_Scenarios_Part08.md', encoding='utf-8').read()
out = ''
for n in range(10, 19):
    m = re.search(r'(?m)^(### Q%d .*)\n(\*\*Asked at:\*\*.*)\n' % n, part)
    body_f = f'{D}/q{n}_body.md'
    if not os.path.exists(body_f):
        continue
    body = open(body_f, encoding='utf-8').read().rstrip('\n')
    code = open(f'{D}/q{n}_code.py', encoding='utf-8').read().rstrip('\n')
    d = tempfile.mkdtemp(); open(d + '/x.py', 'w').write(code + '\n')
    r = subprocess.run(['python3', '-I', 'x.py'], cwd=d, capture_output=True, text=True)
    assert r.returncode == 0, (n, r.stderr)
    body = body.replace('{{CODE}}', '```python\n' + code + '\n```').replace('{{OUTPUT}}', '```\n' + r.stdout.rstrip('\n') + '\n```')
    out += m.group(1) + '\n' + m.group(2) + '\n' + body + '\n\n'
open(f'{D}/answers.md', 'w', encoding='utf-8').write(out)
print('built', out.count('### Q'))
