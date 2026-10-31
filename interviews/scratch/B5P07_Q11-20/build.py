# Assembles answers.md for Q11-Q20 and re-runs every code file. Usage: python3 build.py
import os, re, subprocess, sys
ROOT = os.path.dirname(os.path.abspath(__file__))
PART = os.path.join(ROOT, '..', '..', 'Book5_DSA', 'Book5_DSA_Part07.md')
CODE = os.path.join(ROOT, 'code')
part = open(PART, encoding='utf-8').read()
prelude = open(os.path.join(CODE, 'prelude.py'), encoding='utf-8').read()
out = []
for n in range(11, 21):
    m = re.search(rf'^### Q{n} .*\n\*\*Asked at:\*\*.*\n', part, re.M)
    assert m, n
    body_p = os.path.join(CODE, f'body_q{n}.py'); text_p = os.path.join(CODE, f'text_q{n}.md')
    if not (os.path.exists(body_p) and os.path.exists(text_p)):
        print('Q%d: missing files, skipped' % n); continue
    code = prelude + '\n' + open(body_p, encoding='utf-8').read()
    code_p = os.path.join(CODE, f'q{n}.py'); open(code_p, 'w', encoding='utf-8').write(code)
    r = subprocess.run([sys.executable, '-I', code_p], capture_output=True, text=True, timeout=600, cwd=CODE)
    assert r.returncode == 0, (n, r.stderr[-2000:])
    open(os.path.join(CODE, f'out_q{n}.txt'), 'w', encoding='utf-8').write(r.stdout)
    text = open(text_p, encoding='utf-8').read()
    assert '{{CODE}}' in text and '{{OUTPUT}}' in text, n
    text = text.replace('{{CODE}}', '```python\n' + code.rstrip('\n') + '\n```').replace('{{OUTPUT}}', '```\n' + r.stdout.rstrip('\n') + '\n```')
    out.append(m.group(0) + '\n' + text.strip('\n') + '\n\n')
    print('Q%d ok' % n)
open(os.path.join(ROOT, 'answers.md'), 'w', encoding='utf-8').write(''.join(out))
