# Assembles answers.md: heading + Asked-at lines copied verbatim from the part file, then parts/qNN.md with the
# code (code/qNN.py) and the REAL output of `python3 -I code/qNN.py` substituted in. Re-runs every code file.
import re, subprocess, os, sys
root = os.path.dirname(os.path.abspath(__file__))
part = open('/home/user/case_studies/interviews/Book5_DSA/Book5_DSA_Part14.md', encoding='utf-8').read().split('\n')
out = []
for n in range(1, 11):
    i = next(k for k, l in enumerate(part) if re.match(r'### Q%d ' % n, l))
    head, asked = part[i], part[i + 1]
    assert asked.startswith('**Asked at:**')
    code = open(f'{root}/code/q{n:02d}.py', encoding='utf-8').read()
    r = subprocess.run([sys.executable, '-I', f'{root}/code/q{n:02d}.py'], capture_output=True, text=True, cwd='/')
    assert r.returncode == 0, (n, r.stderr)
    body = open(f'{root}/parts/q{n:02d}.md', encoding='utf-8').read()
    body = body.replace('{{CODE}}', code.rstrip('\n') + '\n').replace('{{OUTPUT}}', r.stdout.rstrip('\n') + '\n')
    out.append(head + '\n' + asked + '\n\n' + body.rstrip('\n') + '\n')
    print(f'Q{n}: ok ({len(r.stdout.splitlines())} output lines)')
open(f'{root}/answers.md', 'w', encoding='utf-8').write('\n'.join(out))
for d, _, fs in os.walk(root):
    if d.endswith('__pycache__'):
        for f in fs: os.remove(os.path.join(d, f))
        os.rmdir(d)
