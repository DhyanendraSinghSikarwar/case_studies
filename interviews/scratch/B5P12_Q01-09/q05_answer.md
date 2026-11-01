### Q5 ⭐⭐⭐ 🟡 Letter combinations of a phone number. `digits` is a string (0 <= len <= 6) of characters from '2' to '9' on a phone keypad (2 abc, 3 def, 4 ghi, 5 jkl, 6 mno, 7 pqrs, 8 tuv, 9 wxyz). Return every string you can type, one letter per digit, in ascending alphabetical order (which is the order a recursion that tries letters in keypad order produces). An empty `digits` returns an empty list (not `['']`). State the number of results as the product of the key sizes (3 or 4 per digit, at most 4^6 = 4096) and the cost of building each string. Recursion depth is at most the input size limit stated above (far below CPython's default recursion limit of 1000), so a recursive solution is fine. In the answer include a dry run on the first example and a seeded random cross-check of your solution against itertools.product over the key letters on small inputs. Example: digits='27' -> ['ap', 'aq', 'ar', 'as', 'bp', 'bq', 'br', 'bs', 'cp', 'cq', 'cr', 'cs']; digits='9' -> ['w', 'x', 'y', 'z']; digits='' -> []; digits='78' -> ['pt', 'pu', 'pv', 'qt', 'qu', 'qv', 'rt', 'ru', 'rv', 'st', 'su', 'sv'].
**Asked at:** Backtracking pattern guides and lists (techinterview.org backtracking and recursion patterns posts, designgurus backtracking interview questions, a DEV Community backtracking-patterns post; search snippets only, not opened)

**Pattern:** Backtracking over a product of choices: one letter per digit, a fixed-depth tree.

**Say this first (1 line):** "Recurse digit by digit, try each letter of that key in keypad order, undo after. Letters in keypad order give ascending output for free. Results are the product of the key sizes, at most 4^6 = 4096, and each string costs O(L) to build."

**Brute force:** `itertools.product(*keys)` and join. Same count, no recursion. That is the oracle in the cross-check. Naive string concatenation at each level also works but copies prefixes.

**Optimal:**
- `go(i)`: if `i == len(digits)`, join `cur` and append. Else for each letter in `KEYS[digits[i]]` in order: `cur.append(ch)`, `go(i + 1)`, `cur.pop()`.
- Keys are stored in alphabetical order, and the first digit is the most significant "digit" of the result, so the output comes out sorted: no final sort needed. The tests check this against a sorted `itertools.product` result.
- Empty `digits` returns `[]`, not `['']`: special-case it first (otherwise the recursion would hit the leaf at once and return one empty string).
- Pruning rule: none exists. Every path of length L is an answer, so the tree has no dead end. The call count is 1 + k1 + k1*k2 + ... + (k1*...*kL), shown below (for '999999' it is 5461 calls for 4096 results, so the internal nodes add only about 33 per cent).
- Recursion depth is L <= 6.

**Complexity:** Results R = product of the key sizes (3 or 4 each), at most 4096. Each result is a string of L characters built with `join`: O(L). Time O(L * R) (plus the calls, which are O(R) in total because the tree is bushy). Space O(L) for the recursion and `cur`, plus the output O(L * R).

**Dry run:** `'27'`. Level 0 digit 2 ('abc'): choose 'a'. Level 1 digit 7 ('pqrs'): choose p, q, r, s, producing `ap aq ar as`. Undo to the prefix `''`, choose 'b', again four leaves, then 'c'. 3 * 4 = 12 results, in the order shown. The program prints the first lines of this tree.

**Code:**
```python
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
```

**Output (my run):**
```
'27' -> ['ap', 'aq', 'ar', 'as', 'bp', 'bq', 'br', 'bs', 'cp', 'cq', 'cr', 'cs']
'9' -> ['w', 'x', 'y', 'z']
'' -> []
'78' -> ['pt', 'pu', 'pv', 'qt', 'qu', 'qv', 'rt', 'ru', 'rv', 'st', 'su', 'sv']
digit 2 (abc), prefix ''
  digit 7 (pqrs), prefix 'a'
    leaf ap
    leaf aq
    leaf ar
    leaf as
  digit 7 (pqrs), prefix 'b'
    leaf bp
    leaf bq
  ... 16 lines in all
digits=''         results=    0 calls=1
digits='2'        results=    3 calls=4
digits='27'       results=   12 calls=16
digits='7979'     results=  256 calls=341
digits='999999'   results= 4096 calls=5461
digits='234567'   results=  972 calls=1336
random cross-check ok: 2000 cases
edge asserts ok
```

**Edge cases:**
- `''` returns `[]`.
- A single digit returns that key's letters, in order.
- '7' and '9' have four letters; '777777' gives 4096 strings, all distinct and sorted (asserted).
- Input never contains '0' or '1' by the prompt. If it could, you would have to define what they mean.

**Follow-ups:**
- Iterative version: start with `['']` and for each digit replace the list with every `p + ch`. Same output order, O(R * L) time, no recursion.
- Count only: the product of key sizes, no enumeration.
- Dictionary words only: prune a prefix that is not in a trie (Q11 uses this idea).

**Common mistakes:**
- Returning `['']` for empty input.
- Using a list for `cur` and forgetting `cur.pop()` (passing an immutable string `prefix + ch` down needs no undo, a shared list does).
- Assuming 3 letters per digit: 7 and 9 have 4.
