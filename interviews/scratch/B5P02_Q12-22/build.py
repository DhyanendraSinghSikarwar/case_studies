import pathlib, subprocess, sys, shutil
here = pathlib.Path(__file__).parent
part = pathlib.Path('/home/user/case_studies/interviews/Book5_DSA/Book5_DSA_Part02.md').read_text().split('\n')
out = []; bad = []
for n in range(12, 23):
    i = next(k for k, l in enumerate(part) if l.startswith(f'### Q{n} '))
    head, asked = part[i], part[i + 1]
    assert asked.startswith('**Asked at:**')
    p = here / 'parts' / f'q{n}.md'; c = here / 'code' / f'q{n}.py'
    if not (p.exists() and c.exists()):
        continue
    r = subprocess.run([sys.executable, '-I', str(c)], capture_output=True, text=True, cwd='/tmp')
    if r.returncode:
        bad.append(n); print('FAIL', n, r.stderr[-500:]); continue
    (here / 'code' / f'q{n}.out').write_text(r.stdout)
    code = c.read_text(); code = code if code.endswith('\n') else code + '\n'
    body = p.read_text().replace('{{CODE}}', code).replace('{{OUTPUT}}', r.stdout)
    out.append(head + '\n' + asked + '\n\n' + body.rstrip() + '\n\n---\n')
(here / 'answers.md').write_text('\n'.join(out))
print(len(out), 'answers built; failures:', bad)
shutil.rmtree(here / '__pycache__', ignore_errors=True)
