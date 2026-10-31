"""Assemble answers.md from the part file headings + qNN.md templates + code/qNN.py (re-run with python3 -I)."""
import os, re, subprocess, sys
HERE = os.path.dirname(os.path.abspath(__file__))
PART = os.path.join(HERE, '..', '..', 'Book5_DSA', 'Book5_DSA_Part11.md')
txt = open(PART, encoding='utf-8').read().split('\n')
heads = {}
for k, line in enumerate(txt):
    m = re.match(r'### Q(\d+) ', line)
    if m and 1 <= int(m.group(1)) <= 9:
        asked = next(l for l in txt[k + 1:k + 6] if l.startswith('**Asked at:**'))
        heads[int(m.group(1))] = (line, asked)
out = ['# Book 5 Part 11 answers Q1-Q9 (Wave B)', '']
done = []
for q in range(1, 10):
    md = os.path.join(HERE, 'q%02d.md' % q)
    py = os.path.join(HERE, 'code', 'q%02d.py' % q)
    if not (os.path.exists(md) and os.path.exists(py)):
        print('Q%d missing' % q); continue
    r = subprocess.run([sys.executable, '-I', py], capture_output=True, text=True, cwd=os.path.join(HERE, 'code'))
    if r.returncode != 0:
        print('Q%d FAILED\n%s' % (q, r.stderr[-800:])); continue
    body = open(md, encoding='utf-8').read()
    body = body.replace('{{CODE}}', open(py, encoding='utf-8').read().rstrip('\n')).replace('{{OUTPUT}}', r.stdout.rstrip('\n'))
    out += [heads[q][0], heads[q][1], '', body.rstrip('\n'), '', '---', '']
    done.append(q)
open(os.path.join(HERE, 'answers.md'), 'w', encoding='utf-8').write('\n'.join(out))
print('assembled Q', done)
