"""Assemble answers.md for Q21-Q30 from qNN.md prose files.
Each qNN.md holds the answer body (Pattern..Common mistakes) with one ```python block and a line @@OUTPUT@@.
Build: extracts code to code/qNN.py, re-runs it with python3 -I, pastes real output, copies heading + Asked-at verbatim."""
import re, subprocess, sys, os
HERE = os.path.dirname(os.path.abspath(__file__))
PART = os.path.join(HERE, '..', '..', 'Book5_DSA', 'Book5_DSA_Part04.md')
part = open(PART, encoding='utf-8').read().split('\n')
out = ["# Book 5 Part 4, Q21-Q30 answers (Wave B)\n"]
ok = []
for n in range(21, 31):
    i = next(k for k, l in enumerate(part) if l.startswith(f'### Q{n} '))
    head, asked = part[i], part[i + 1]
    assert asked.startswith('**Asked at:**')
    f = os.path.join(HERE, f'q{n}.md')
    if not os.path.exists(f):
        print(f'Q{n}: missing'); continue
    body = open(f, encoding='utf-8').read()
    m = re.search(r'```python\n(.*?)```', body, re.S)
    code = m.group(1)
    cf = os.path.join(HERE, 'code', f'q{n}.py')
    open(cf, 'w', encoding='utf-8').write(code)
    r = subprocess.run([sys.executable, '-I', cf], capture_output=True, text=True, encoding='utf-8')
    if r.returncode != 0:
        print(f'Q{n}: FAILED\n{r.stderr[-800:]}'); sys.exit(1)
    outp = r.stdout.rstrip('\n')
    assert '@@OUTPUT@@' in body
    body = body.replace('@@OUTPUT@@', '```\n' + outp + '\n```')
    for lab in ['**Pattern:**', '**Say this first (1 line):**', '**Brute force:**', '**Optimal:**', '**Complexity:**',
                '**Dry run:**', '**Code:**', '**Output (my run):**', '**Edge cases:**', '**Follow-ups:**', '**Common mistakes:**']:
        assert body.count(lab) == 1, (n, lab)
    out.append(f'\n{head}\n{asked}\n\n{body.strip()}\n')
    ok.append(n)
    print(f'Q{n}: ok')
open(os.path.join(HERE, 'answers.md'), 'w', encoding='utf-8').write('\n'.join(out))
print('complete:', ok)
