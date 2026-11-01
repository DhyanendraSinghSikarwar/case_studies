import re, subprocess, sys, os
HERE = os.path.dirname(os.path.abspath(__file__))
PART = os.path.join(HERE, '../../Book5_DSA/Book5_DSA_Part09.md')
lines = open(PART, encoding='utf-8').read().split('\n')
heads = {}
for i, l in enumerate(lines):
    m = re.match(r'### Q(\d+) ', l)
    if m: heads[int(m.group(1))] = (l, next(x for x in lines[i+1:i+6] if x.startswith('**Asked at:**')))
out, status = [], []
for q in range(23, 34):
    body_p = os.path.join(HERE, 'parts', f'q{q}.txt'); code_p = os.path.join(HERE, 'code', f'q{q}.py')
    if not (os.path.exists(body_p) and os.path.exists(code_p)): status.append((q, 'MISSING')); continue
    r = subprocess.run([sys.executable, '-I', code_p], capture_output=True, text=True, timeout=600)
    if r.returncode: status.append((q, 'FAIL\n' + r.stderr[-800:])); continue
    body = open(body_p, encoding='utf-8').read().rstrip('\n')
    code = open(code_p, encoding='utf-8').read().rstrip('\n')
    body = body.replace('@@CODE@@', '```python\n' + code + '\n```').replace('@@OUTPUT@@', '```\n' + r.stdout.rstrip('\n') + '\n```')
    h, a = heads[q]
    out.append(h + '\n' + a + '\n\n' + body + '\n'); status.append((q, 'OK'))
open(os.path.join(HERE, 'answers.md'), 'w', encoding='utf-8').write('\n'.join(out))
for s in status: print(*s)
