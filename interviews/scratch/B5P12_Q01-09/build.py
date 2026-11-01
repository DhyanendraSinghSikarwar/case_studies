# Assembles answers.md from body/qNN.md (text with @@CODE@@ and @@OUTPUT@@ markers), code/qNN.py and the part file headings.
# Re-runs every code file with python3 -I and pastes the real output. Run: python3 build.py
import os, re, subprocess, sys
HERE = os.path.dirname(os.path.abspath(__file__))
PART = os.path.join(HERE, '..', '..', 'Book5_DSA', 'Book5_DSA_Part12.md')
lines = open(PART, encoding='utf-8').read().split('\n')
heads = {}
for i, l in enumerate(lines):
    m = re.match(r'### Q(\d+) ', l)
    if m:
        heads[int(m.group(1))] = (l, lines[i + 1])
        assert lines[i + 1].startswith('**Asked at:**')
out = ['# Book 5 Part 12, answers Q1-Q9 (Wave B)\n']
for q in range(1, 10):
    body_path = os.path.join(HERE, 'body', f'q{q:02d}.md')
    if not os.path.exists(body_path):
        print('missing body', q); continue
    code_path = os.path.join(HERE, 'code', f'q{q:02d}.py')
    code = open(code_path, encoding='utf-8').read().rstrip('\n')
    r = subprocess.run([sys.executable, '-I', code_path], capture_output=True, text=True, cwd=os.path.join(HERE, 'code'))
    assert r.returncode == 0, (q, r.stderr)
    body = open(body_path, encoding='utf-8').read().strip('\n')
    assert '@@CODE@@' in body and '@@OUTPUT@@' in body
    body = body.replace('@@CODE@@', '```python\n' + code + '\n```').replace('@@OUTPUT@@', '```\n' + r.stdout.rstrip('\n') + '\n```')
    h, a = heads[q]
    one = h + '\n' + a + '\n\n' + body + '\n'
    open(os.path.join(HERE, f'q{q:02d}_answer.md'), 'w', encoding='utf-8').write(one)
    out.append(one)
    print('built Q%d' % q)
open(os.path.join(HERE, 'answers.md'), 'w', encoding='utf-8').write('\n'.join(out))
for root, d, f in os.walk(HERE):
    for x in d:
        if x == '__pycache__':
            import shutil; shutil.rmtree(os.path.join(root, x))
