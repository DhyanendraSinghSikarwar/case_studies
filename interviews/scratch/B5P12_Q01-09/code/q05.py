import itertools
import random

random.seed(1205)
KEYS = {'2': 'abc', '3': 'def', '4': 'ghi', '5': 'jkl', '6': 'mno', '7': 'pqrs', '8': 'tuv', '9': 'wxyz'}

def letter_combos(digits):
    """Returns (list in ascending order, number of recursive calls)."""
    if not digits:
        return [], 1                        # empty input -> [] (not [''])
    out, cur, calls = [], [], [0]
    def go(i):
        calls[0] += 1
        if i == len(digits):
            out.append(''.join(cur))        # O(L) to build each string
            return
        for ch in KEYS[digits[i]]:          # keypad order => ascending output
            cur.append(ch)                  # choose
            go(i + 1)                       # explore
            cur.pop()                       # undo
    go(0)
    return out, calls[0]

def brute(digits):
    if not digits:
        return []
    return sorted(''.join(p) for p in itertools.product(*(KEYS[d] for d in digits)))

examples = [('27', ['ap', 'aq', 'ar', 'as', 'bp', 'bq', 'br', 'bs', 'cp', 'cq', 'cr', 'cs']),
            ('9', ['w', 'x', 'y', 'z']), ('', []),
            ('78', ['pt', 'pu', 'pv', 'qt', 'qu', 'qv', 'rt', 'ru', 'rv', 'st', 'su', 'sv'])]
for d, want in examples:
    assert letter_combos(d)[0] == want == brute(d)
    print(repr(d), '->', letter_combos(d)[0])

# decision tree for '9' then '2' is wide; show the tree for '27' as calls with depth (first 8 lines)
lines = []
def show(i, cur, digits='27'):
    if i == len(digits):
        lines.append('  ' * i + 'leaf ' + cur); return
    lines.append('  ' * i + f'digit {digits[i]} ({KEYS[digits[i]]}), prefix {cur!r}')
    for ch in KEYS[digits[i]]:
        show(i + 1, cur + ch, digits)
show(0, '')
print('\n'.join(lines[:9])); print('  ...', len(lines), 'lines in all')

# no pruning exists: every path of length L is an answer. Calls = 1 + k1 + k1*k2 + ...
def expected_calls(digits):
    total, prod = 1, 1
    for d in digits:
        prod *= len(KEYS[d]); total += prod
    return total
for d in ['', '2', '27', '7979', '999999', '234567']:
    r, c = letter_combos(d)
    assert c == (1 if not d else expected_calls(d))
    print(f'digits={d!r:10} results={len(r):5} calls={c}')

# seeded cross-check
for _ in range(2000):
    d = ''.join(random.choice('23456789') for _ in range(random.randint(0, 5)))
    assert letter_combos(d)[0] == brute(d)
print('random cross-check ok: 2000 cases')

# edge: max size 4^6 = 4096 results, all of length 6, sorted and distinct
r = letter_combos('777777')[0]
assert len(r) == 4096 and r == sorted(set(r)) and all(len(s) == 6 for s in r)
assert letter_combos('')[0] == [] and letter_combos('2')[0] == ['a', 'b', 'c']
print('edge asserts ok')
