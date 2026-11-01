import re, sys, pathlib
sys.path.insert(0, str(pathlib.Path(__file__).parent))
from bodies import B
here = pathlib.Path(__file__).parent
part = pathlib.Path('/home/user/case_studies/interviews/Book4_MLOps/Book4_MLOps_Part01.md').read_text().splitlines()
env = (here/'env.sh').read_text().strip()
def block(lang, text): return f"```{lang}\n{text.rstrip()}\n```"
def sh(name):
    t = (here/name).read_text()
    t = re.sub(r'^\. "\$\(dirname "\$0"\)/env\.sh"$', "# --- env.sh (shared setup, shown inline) ---\n"+env+"\n# --- end env.sh ---", t, flags=re.M)
    return block('bash', t)
def py(names):
    parts = []
    for n in names.split(','):
        parts.append(f"# ===== {n} =====\n" + (here/n).read_text().rstrip())
    return block('python', "\n\n".join(parts))
def out(n): return block('text', (here/'out'/f'{n}.txt').read_text())
out_lines = []
for q in range(1, 11):
    h = next(i for i, l in enumerate(part) if l.startswith(f'### Q{q} '))
    body = B[q]
    body = re.sub(r'\{\{SH:([^}]+)\}\}', lambda m: sh(m.group(1)), body)
    body = re.sub(r'\{\{PY:([^}]+)\}\}', lambda m: py(m.group(1)), body)
    body = re.sub(r'\{\{OUT:([^}]+)\}\}', lambda m: out(m.group(1)), body)
    out_lines += [part[h], part[h+1], body.rstrip(), '']
(here.parent/'answers.md').write_text("\n".join(out_lines))
