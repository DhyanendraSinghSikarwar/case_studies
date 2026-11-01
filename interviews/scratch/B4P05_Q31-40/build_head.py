import re, json
L = open('/home/user/case_studies/interviews/Book4_MLOps/Book4_MLOps_Part05.md').read().split('\n')
heads = {}
for i, l in enumerate(L):
    m = re.match(r'### Q(\d+) ', l)
    if m: heads[int(m.group(1))] = (l, L[i+1] if L[i+1].startswith('**Asked at:**') else L[i+2])
json.dump(heads, open('/tmp/claude-0/b5p05_q31_40/heads.json', 'w'))
print({k: v[1][:30] for k, v in heads.items() if 31 <= k <= 40})
