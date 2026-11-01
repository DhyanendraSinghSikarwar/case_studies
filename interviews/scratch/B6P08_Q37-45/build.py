import re, subprocess, os, sys
D = os.path.dirname(os.path.abspath(__file__))
PART = os.path.join(D, '../../Book6_Scenarios/Book6_Scenarios_Part08.md')
t = open(PART, encoding='utf-8').read()
blocks = re.split(r'(?m)^(?=### Q\d+ )', t)[1:]
heads = {}
for b in blocks:
    ls = b.split('\n')
    n = int(re.match(r'### Q(\d+)', ls[0]).group(1))
    assert ls[1].startswith('**Asked at:**')
    heads[n] = ls[0] + '\n' + ls[1] + '\n'
out = ''
done = []
for n in range(37, 46):
    bp = os.path.join(D, f'q{n}.body.md'); cp = os.path.join(D, f'q{n}.py')
    if not (os.path.exists(bp) and os.path.exists(cp)):
        continue
    r = subprocess.run(['python3', '-I', cp], capture_output=True, text=True, cwd='/tmp')
    assert r.returncode == 0, (n, r.stderr)
    code = open(cp, encoding='utf-8').read().rstrip('\n')
    body = open(bp, encoding='utf-8').read()
    body = body.replace('{{CODE}}', code).replace('{{OUT}}', r.stdout.rstrip('\n'))
    q = heads[n] + body.rstrip('\n') + '\n'
    open(os.path.join(D, f'q{n}.md'), 'w', encoding='utf-8').write(q)
    out += q + '\n'
    done.append(n)
open(os.path.join(D, 'answers.md'), 'w', encoding='utf-8').write(out.rstrip('\n') + '\n')
print('built', done)
