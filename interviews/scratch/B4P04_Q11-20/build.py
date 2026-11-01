import re, pathlib
base = pathlib.Path('/home/user/case_studies/interviews')
part = (base/'Book4_MLOps/Book4_MLOps_Part04.md').read_text().splitlines()
here = pathlib.Path(__file__).parent
code = here/'code'
out = []
for n in range(11, 21):
    i = next(k for k, l in enumerate(part) if l.startswith(f'### Q{n} '))
    head = part[i]; asked = part[i+1]
    assert asked.startswith('**Asked at:**'), n
    body = (here/'tpl'/f'Q{n}.md').read_text()
    body = re.sub(r'\{\{file:(.+?)\}\}', lambda m: (code/m.group(1)).read_text().rstrip('\n'), body)
    body = re.sub(r'\{\{out:(.+?)\}\}', lambda m: (code/'out'/(m.group(1)+'.txt')).read_text().rstrip('\n'), body)
    body = body.replace('{{lineage}}', (code/'out/lineage.txt').read_text().rstrip('\n'))
    out.append(f'{head}\n{asked}\n{body.rstrip()}\n')
(here/'answers.md').write_text('\n'.join(out))
