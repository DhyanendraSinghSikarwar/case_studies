# Assembles answers.md: heading + Asked-at copied verbatim from the part file, then text/qNN.md with code and real output substituted.
# Re-runs every code file with python3 -I and asserts it exits 0. Run from anywhere: python3 build.py
import os, re, subprocess, sys
here = os.path.dirname(os.path.abspath(__file__))
part = os.path.join(here, '..', '..', 'Book5_DSA', 'Book5_DSA_Part07.md')
lines = open(part, encoding='utf-8').read().split('\n')
head = open(os.path.join(here, 'code', '_head.py')).read()
out = []
for q in range(21, 31):
    i = next(k for k, l in enumerate(lines) if re.match(rf'### Q{q} ', l))
    heading, asked = lines[i], lines[i + 1]
    assert asked.startswith('**Asked at:**'), q
    body = open(os.path.join(here, 'text', f'q{q}.md'), encoding='utf-8').read().rstrip('\n')
    code = head + open(os.path.join(here, 'code', f'q{q}_body.py'), encoding='utf-8').read()
    cp = os.path.join(here, 'code', f'q{q}.py'); open(cp, 'w', encoding='utf-8').write(code)
    r = subprocess.run([sys.executable, '-I', cp], capture_output=True, text=True, timeout=300)
    assert r.returncode == 0, f'Q{q} failed:\n{r.stderr}'
    assert body.count('@@CODE@@') == 1 and body.count('@@OUTPUT@@') == 1
    body = body.replace('@@CODE@@', code.rstrip('\n')).replace('@@OUTPUT@@', r.stdout.rstrip('\n'))
    out.append(heading + '\n' + asked + '\n\n' + body + '\n')
    print('Q%d ok' % q)
open(os.path.join(here, 'answers.md'), 'w', encoding='utf-8').write('\n'.join(out))
