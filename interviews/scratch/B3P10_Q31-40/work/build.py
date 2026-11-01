import re
from prose import P, F
part = open('/home/user/case_studies/interviews/Book3_SQL/Book3_SQL_Part10.md', encoding='utf-8').read().split('\n')
out = []
for n in range(31, 41):
    idx = next(i for i, l in enumerate(part) if l.startswith(f'### Q{n} '))
    head, asked = part[idx], part[idx + 1]
    assert asked.startswith('**Asked at:**')
    d = P[n]
    code = open(f'q{n}.py', encoding='utf-8').read().rstrip('\n')
    assert F not in code
    res = open(f'out{n}.txt', encoding='utf-8').read().rstrip('\n')
    out.append('\n'.join([
        head, asked,
        f"**Say this first (1 line):** {d['say']}", '',
        f"**Schema and sample data:**\n{d['schema']}", '',
        f"**SQL answer:** {d['sql']}", '',
        f"**pandas answer:** {d['pandas']}", '',
        f"**Example:** {d['example']}", '',
        f"**Code:** run with `python3 -I`; the two results are compared after the stated sort, then asserted.\n{F}python\n{code}\n{F}", '',
        f"**Output (my run):**\n{F}text\n{res}\n{F}", '',
        f"**Edge cases:**\n{d['edge']}", '',
        f"**Then explain:**\n{d['explain']}", '',
        f"**Follow-ups:**\n{d['follow']}", '',
        f"**Common mistakes:**\n{d['mistakes']}", '', '']))
open('../answers.md', 'w', encoding='utf-8').write('\n'.join(out).rstrip('\n') + '\n')
