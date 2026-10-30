import re, subprocess, os, sys
D = os.path.dirname(os.path.abspath(__file__))
ROOT = os.path.abspath(os.path.join(D, '..', '..'))
part = open(os.path.join(ROOT, 'Book6_Scenarios', 'Book6_Scenarios_Part03.md'), encoding='utf-8').read()
CHECK = {  # cross-reference snippets that must exist in the named files
 11: [('Book1_DS_ML/Book1_DS_ML_Part02.md', 'How do outliers affect linear regression and what robust options exist')],
 12: [('Book6_Scenarios/Book6_Scenarios_Part02.md', 'An upstream team renamed a column and changed its type')],
 13: [('Book1_DS_ML/Book1_DS_ML_Part03.md', 'Does class weighting, SMOTE or undersampling break probability calibration?')],
 15: [('Book1_DS_ML/Book1_DS_ML_Part02.md', 'How do you do target encoding without leakage')],
 16: [('Book6_Scenarios/Book6_Scenarios_Part02.md', "After an upstream deploy, the merchant_category feature's null rate jumped")],
 17: [('Book1_DS_ML/Book1_DS_ML_Part03.md', 'Class weights vs resampling (over/under-sampling)'),
      ('Book1_DS_ML/Book1_DS_ML_Part03.md', 'PR-AUC: what is its random baseline'),
      ('Book1_DS_ML/Book1_DS_ML_Part03.md', 'Where in the pipeline do you apply SMOTE or resampling?')],
}
for q, lst in CHECK.items():
    for f, s in lst:
        assert s in open(os.path.join(ROOT, f), encoding='utf-8').read(), (q, s)
out = []
for q in range(11, 21):
    m = re.search(r'(?m)^(### Q%d .*)\n(\*\*Asked at:\*\*.*)\n' % q, part)
    head, asked = m.group(1), m.group(2)
    body = open(os.path.join(D, f'q{q}.md'), encoding='utf-8').read().rstrip('\n')
    r = subprocess.run(['python3', '-I', f'q{q}.py'], cwd=D, capture_output=True, text=True, timeout=300, stdin=subprocess.DEVNULL)
    assert r.returncode == 0, (q, r.stderr)
    code = open(os.path.join(D, f'q{q}.py'), encoding='utf-8').read().rstrip('\n')
    body = body.replace('@@CODE@@', '```python\n' + code + '\n```').replace('@@OUTPUT@@', '```text\n' + r.stdout.rstrip('\n') + '\n```')
    open(os.path.join(D, f'q{q}_out.txt'), 'w').write(r.stdout)
    out.append(head + '\n' + asked + '\n' + body + '\n')
open(os.path.join(D, 'answers.md'), 'w', encoding='utf-8').write('\n'.join(out))
for f in os.listdir(D):
    if f == '__pycache__': import shutil; shutil.rmtree(os.path.join(D, f))
print('built', len(out))
