import sys, copy, os
HERE = os.path.dirname(os.path.abspath(__file__)); sys.path.insert(0, HERE)
exec(open(os.path.join(HERE, 'draft.py')).read())
import refs
out = ["# Question data for Book 5 Part 10 (DP I). Entry: (stars, difficulty, key, prompt, examples, asked-at).\n# examples = list of (kwargs dict, expected); rendered into the prompts AND executed by check_examples.py (single source of truth).\n"]
for k, v in AK.items(): out.append(f"{k}={v!r}\n")
out.append("QS=[\n")
for s, d, key, text, exs, asked in D:
    ex = [(kw, refs.S[key](**copy.deepcopy(kw))) for kw in exs]
    out.append(f"({s},{d!r},{key!r},{text!r},\n {ex!r},{asked!r}),\n")
out.append("]\n")
open(os.path.join(HERE, 'qs.py'), 'w', encoding='utf-8').write(''.join(out))
print(len(D))
