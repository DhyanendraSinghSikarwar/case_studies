# Assembles answers.md from parts/qNN_pre.md, code/qNN.py (re-run with python3 -I), parts/qNN_post.md.
# Headings and Asked-at lines are copied verbatim from the part file.
import re, subprocess, sys, os
HERE = os.path.dirname(os.path.abspath(__file__))
PART = os.path.join(HERE, '..', '..', 'Book5_DSA', 'Book5_DSA_Part09.md')
lines = open(PART, encoding='utf-8').read().split('\n')
out = []; done = []
for q in range(12, 23):
    pre, code, post = [os.path.join(HERE, d, f) for d, f in (('parts', f'q{q}_pre.md'), ('code', f'q{q}.py'), ('parts', f'q{q}_post.md'))]
    if not all(os.path.exists(x) for x in (pre, code, post)):
        print('Q%d missing, skipped' % q); continue
    i = next(k for k, l in enumerate(lines) if l.startswith(f'### Q{q} '))
    assert lines[i + 1].startswith('**Asked at:**')
    r = subprocess.run([sys.executable, '-I', code], capture_output=True, text=True, timeout=600, cwd=os.path.dirname(code))
    if r.returncode: print('Q%d FAILED' % q, r.stderr[-500:]); sys.exit(1)
    out.append('\n'.join([lines[i], lines[i + 1], '']))
    out.append(open(pre).read().rstrip() + '\n')
    out.append('**Code:**\n\n```python\n' + open(code).read().rstrip() + '\n```\n')
    out.append('**Output (my run):**\n\n```text\n' + r.stdout.rstrip() + '\n```\n')
    out.append(open(post).read().rstrip() + '\n\n---\n')
    done.append(q); print('Q%d ok' % q)
open(os.path.join(HERE, 'answers.md'), 'w', encoding='utf-8').write('\n'.join(out))
print('complete:', done)
