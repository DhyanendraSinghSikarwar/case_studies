# Assembles answers.md: heading + Asked-at copied verbatim from the part file, prose from prose/qNN.md,
# code from code/qNN.py, output pasted from a fresh `python3 -I` run of that file. Usage: python3 build.py
import re, subprocess, sys, os, shutil
HERE = os.path.dirname(os.path.abspath(__file__))
PART = os.path.join(HERE, '..', '..', 'Book5_DSA', 'Book5_DSA_Part13.md')
lines = open(PART, encoding='utf-8').read().split('\n')
out = []
for q in range(31, 41):
    idx = next(i for i, l in enumerate(lines) if l.startswith(f'### Q{q} '))
    heading, asked = lines[idx], lines[idx + 1]
    assert asked.startswith('**Asked at:**'), q
    code = open(os.path.join(HERE, 'code', f'q{q}.py'), encoding='utf-8').read().rstrip('\n')
    r = subprocess.run([sys.executable, '-I', os.path.join(HERE, 'code', f'q{q}.py')], capture_output=True, text=True, cwd=HERE)
    assert r.returncode == 0, (q, r.stderr[-800:])
    prose = open(os.path.join(HERE, 'prose', f'q{q}.md'), encoding='utf-8').read().rstrip('\n')
    for tag in ['Pattern', 'Say this first (1 line)', 'Brute force', 'Optimal', 'Complexity', 'Dry run', 'Code', 'Output (my run)', 'Edge cases', 'Follow-ups', 'Common mistakes']:
        assert f'**{tag}:**' in prose, (q, tag)
    prose = prose.replace('{{CODE}}', '```python\n' + code + '\n```').replace('{{OUTPUT}}', '```\n' + r.stdout.rstrip('\n') + '\n```')
    out.append(heading + '\n' + asked + '\n\n' + prose + '\n')
    print('Q%d ok (%d output lines)' % (q, r.stdout.count('\n')))
open(os.path.join(HERE, 'answers.md'), 'w', encoding='utf-8').write('\n'.join(out))
for d, _, _ in os.walk(HERE):
    if d.endswith('__pycache__'): shutil.rmtree(d, ignore_errors=True)
print('answers.md written')
