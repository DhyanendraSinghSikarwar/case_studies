import re, pathlib
here = pathlib.Path(__file__).parent
part = pathlib.Path('/home/user/case_studies/interviews/Book5_DSA/Book5_DSA_Part01.md').read_text().split('\n')
out = []
for n in range(11, 21):
    i = next(k for k, l in enumerate(part) if l.startswith(f'### Q{n} '))
    head, asked = part[i], part[i + 1]
    assert asked.startswith('**Asked at:**')
    p = here / 'parts' / f'q{n}.md'
    if not p.exists():
        continue
    body = p.read_text()
    code = (here / 'code' / f'q{n}.py').read_text()
    outp = (here / 'code' / f'q{n}.out').read_text()
    body = body.replace('{{CODE}}', code if code.endswith('\n') else code + '\n').replace('{{OUTPUT}}', outp if outp.endswith('\n') else outp + '\n')
    out.append(head + '\n' + asked + '\n\n' + body.rstrip() + '\n\n---\n')
(here / 'answers.md').write_text('\n'.join(out))
print(len(out), 'answers built')
