import re, subprocess, sys, os
BASE = os.path.dirname(os.path.abspath(__file__))
ROOT = os.path.abspath(os.path.join(BASE, '..', '..'))
PART = os.path.join(ROOT, 'Book6_Scenarios', 'Book6_Scenarios_Part04.md')
text = open(PART, encoding='utf-8').read()
blocks = {}
for b in re.split(r'(?m)^(?=### Q\d+ )', text):
    m = re.match(r'### Q(\d+) ', b)
    if m: blocks[int(m.group(1))] = b
out = []
for n in range(34, 45):
    body_f = os.path.join(BASE, 'body', f'q{n}.md')
    code_f = os.path.join(BASE, 'code', f'q{n}.py')
    if not (os.path.exists(body_f) and os.path.exists(code_f)):
        print('skip', n); continue
    lines = blocks[n].split('\n')
    head = lines[0]
    asked = [l for l in lines if l.startswith('**Asked at:**')][0]
    r = subprocess.run([sys.executable, '-I', code_f], capture_output=True, text=True)
    assert r.returncode == 0, (n, r.stderr)
    body = open(body_f, encoding='utf-8').read()
    code = open(code_f, encoding='utf-8').read().rstrip('\n')
    body = body.replace('{{CODE}}', code).replace('{{OUTPUT}}', r.stdout.rstrip('\n'))
    out.append(head + '\n' + asked + '\n' + body.rstrip('\n') + '\n')
open(os.path.join(BASE, 'answers.md'), 'w', encoding='utf-8').write('\n'.join(out))
print('built', len(out))
