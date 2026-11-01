# Build answers.md: copy each heading + Asked-at line verbatim from the part file, add prose/qNN.md with the real code and real output.
# Re-runs every code file with python3 -I. Usage: python3 build.py
import os, re, subprocess, sys
HERE = os.path.dirname(os.path.abspath(__file__))
PART = os.path.join(HERE, '..', '..', 'Book5_DSA', 'Book5_DSA_Part12.md')
text = open(PART, encoding='utf-8').read()
blocks = re.split(r'(?m)^(?=### Q\d+ )', text)
head = {}
for b in blocks:
    m = re.match(r'### Q(\d+) ', b)
    if m:
        lines = b.split('\n')
        asked = [l for l in lines if l.startswith('**Asked at:**')]
        head[int(m.group(1))] = (lines[0], asked[0])
out = ['# Book 5 Part 12, Q10-Q18 answers (Wave B)\n']
status = []
for q in range(10, 19):
    code_path = os.path.join(HERE, 'code', 'q%02d.py' % q)
    prose_path = os.path.join(HERE, 'prose', 'q%02d.md' % q)
    if not (os.path.exists(code_path) and os.path.exists(prose_path)):
        status.append((q, 'MISSING FILES')); continue
    r = subprocess.run([sys.executable, '-I', code_path], capture_output=True, text=True, cwd='/')
    if r.returncode != 0:
        status.append((q, 'CODE FAILED: ' + r.stderr[-300:])); continue
    code = open(code_path, encoding='utf-8').read().rstrip('\n')
    prose = open(prose_path, encoding='utf-8').read().rstrip('\n')
    assert '{{CODE}}' in prose and '{{OUTPUT}}' in prose, q
    prose = prose.replace('{{CODE}}', '```python\n' + code + '\n```').replace('{{OUTPUT}}', '```text\n' + r.stdout.rstrip('\n') + '\n```')
    out.append(head[q][0] + '\n' + head[q][1] + '\n\n' + prose + '\n\n---\n')
    status.append((q, 'ok'))
open(os.path.join(HERE, 'answers.md'), 'w', encoding='utf-8').write('\n'.join(out))
for q, s in status: print('Q%d' % q, s)
