### Q7 ⭐⭐⭐ 🟡 Generate parentheses. `n` is an integer with 1 <= n <= 8. Return every balanced string of n pairs of '(' and ')', sorted ascending as Python strings (so '(' sorts before ')' and `'((()))'` comes first). Build them by recursion with two counters (open used, close used) and justify the two pruning rules: you may add '(' while open < n and ')' while close < open. State that the number of results is the n-th Catalan number and that no invalid prefix is ever extended (so every call leads to at least one answer). Recursion depth is at most the input size limit stated above (far below CPython's default recursion limit of 1000), so a recursive solution is fine. In the answer include a dry run on the first example and a seeded random cross-check of your solution against filtering all 2^(2n) strings of '(' and ')' for balance on small inputs. Example: n=1 -> ['()']; n=2 -> ['(())', '()()']; n=3 -> ['((()))', '(()())', '(())()', '()(())', '()()()'].
**Asked at:** Backtracking pattern guides and lists (techinterview.org backtracking and recursion patterns posts, designgurus backtracking interview questions, a DEV Community backtracking-patterns post; search snippets only, not opened)

**Pattern:** Backtracking with a validity invariant: only extend a prefix that can still be completed.

**Say this first (1 line):** "Build the string left to right with two counters. Add '(' while open < n. Add ')' while close < open. Those two rules keep every prefix valid, so nothing is ever thrown away. The count is the n-th Catalan number."

**Brute force:** Generate all 2^(2n) strings of '(' and ')' and keep the balanced ones. For n = 8 that is 65536 strings to test (131071 calls in the tree) for 1430 answers.

**Optimal:**
- State: `o` = '(' used, `c` = ')' used, `cur` = the string so far.
- Rule 1: add '(' only if `o < n` (we have only n pairs).
- Rule 2: add ')' only if `c < o` (there must be an unmatched '(' to close; otherwise the prefix is already unbalanced and no suffix can fix it).
- Stop when `len(cur) == 2n`; then `o == n` and `c == n`, hence balanced.
- Order: try '(' before ')'. Since '(' < ')' as characters, the leaves come out in ascending order, and the code also sorts (cheap) so the claim is by test, not trust.
- "No invalid prefix is ever extended": by induction, every prefix has `c <= o <= n`. Such a prefix can always be completed (add the missing '(' then close everything, or just close). I tested this: for n = 1..8, every prefix visited by the recursion is the prefix of at least one returned answer. So every call leads to at least one answer, and the work per answer is O(n).
- Call counts, pruned against the unpruned tree (which has 2^(2n+1) - 1 calls): n = 3: 22 against 127; n = 6: 625 against 8191; n = 8: 6917 against 131071.
- Recursion depth is 2n <= 16.

**Complexity:** Number of results is Catalan(n) = C(2n, n) / (n + 1): 1, 2, 5, 14, 42, 132, 429, 1430 for n = 1..8, checked by code. Time O(n * Catalan(n)) (every call is on a path to an answer, there are at most 2n calls per answer, and building each string costs O(n)). Asymptotically Catalan(n) ~ 4^n / (n^1.5 * sqrt(pi)). Space O(n) for the recursion plus the output.

**Dry run:** `n = 2`. The program prints the tree:
- empty -> '(' (o=1) -> '((' (o=2): '(' is blocked because o == n; ')' allowed -> '(()' -> '(())' answer.
- '(' -> '()' (o=1, c=1) -> '()(' -> '()()' answer; at '()' the ')' is blocked because c == o.
- At the root ')' is blocked because c == o == 0.
Result `['(())', '()()']`.

**Code:**
```python
import itertools
import math
import random

random.seed(1207)

def gen_parens(n):
    """Returns (sorted list, number of calls, list of every prefix visited)."""
    out, cur, calls, prefixes = [], [], [0], []
    def go(o, c):
        calls[0] += 1
        prefixes.append(''.join(cur))
        if len(cur) == 2 * n:
            out.append(''.join(cur)); return
        if o < n:                           # rule 1: may open while fewer than n opens used
            cur.append('('); go(o + 1, c); cur.pop()
        if c < o:                           # rule 2: may close only if an unmatched '(' exists
            cur.append(')'); go(o, c + 1); cur.pop()
    go(0, 0)
    return sorted(out), calls[0], prefixes

def gen_unpruned_calls(n):
    """Try '(' and ')' at every position, test balance at the leaves: calls = 2^(2n+1) - 1."""
    return 2 ** (2 * n + 1) - 1

def brute(n):
    def ok(s):
        bal = 0
        for ch in s:
            bal += 1 if ch == '(' else -1
            if bal < 0:
                return False
        return bal == 0
    return sorted(''.join(t) for t in itertools.product('()', repeat=2 * n) if ok(t))

examples = [(1, ['()']), (2, ['(())', '()()']), (3, ['((()))', '(()())', '(())()', '()(())', '()()()'])]
for n, want in examples:
    assert gen_parens(n)[0] == want == brute(n)
    print(n, '->', gen_parens(n)[0])

# decision tree for n = 2: which branches the two rules allow
def tree(n, s='', o=0, c=0, d=0):
    if len(s) == 2 * n:
        print('  ' * d + f'{s}  (answer)'); return
    print('  ' * d + f'{s or "(empty)"}  open={o} close={c}')
    if o < n: tree(n, s + '(', o + 1, c, d + 1)
    else: print('  ' * (d + 1) + "'(' blocked: open == n")
    if c < o: tree(n, s + ')', o, c + 1, d + 1)
    else: print('  ' * (d + 1) + "')' blocked: close == open")
tree(2)

# Catalan counts, calls pruned vs unpruned, and the claim 'no dead branch': every visited prefix begins some answer
for n in range(1, 9):
    res, calls, prefixes = gen_parens(n)
    assert len(res) == math.comb(2 * n, n) // (n + 1)
    assert all(any(r.startswith(p) for r in res) for p in prefixes), 'dead branch found'
    print(f'n={n} results={len(res):5} pruned calls={calls:6} unpruned calls={gen_unpruned_calls(n):7}')
    if n <= 6:
        assert res == brute(n)

# seeded cross-check (n up to 5, plus random ids)
for _ in range(100):
    n = random.randint(1, 5)
    assert gen_parens(n)[0] == brute(n)
print('random cross-check ok: 100 cases (n in 1..5; the oracle is exhaustive)')
# edge: n = 1, n = 8 (1430 = Catalan(8)), first and last strings
r = gen_parens(8)[0]
assert len(r) == 1430 and r[0] == '(' * 8 + ')' * 8 and r[-1] == '()' * 8
assert gen_parens(1)[0] == ['()']
print('edge asserts ok')
```

**Output (my run):**
```
1 -> ['()']
2 -> ['(())', '()()']
3 -> ['((()))', '(()())', '(())()', '()(())', '()()()']
(empty)  open=0 close=0
  (  open=1 close=0
    ((  open=2 close=0
      '(' blocked: open == n
      (()  open=2 close=1
        '(' blocked: open == n
        (())  (answer)
    ()  open=1 close=1
      ()(  open=2 close=1
        '(' blocked: open == n
        ()()  (answer)
      ')' blocked: close == open
  ')' blocked: close == open
n=1 results=    1 pruned calls=     3 unpruned calls=      7
n=2 results=    2 pruned calls=     8 unpruned calls=     31
n=3 results=    5 pruned calls=    22 unpruned calls=    127
n=4 results=   14 pruned calls=    64 unpruned calls=    511
n=5 results=   42 pruned calls=   196 unpruned calls=   2047
n=6 results=  132 pruned calls=   625 unpruned calls=   8191
n=7 results=  429 pruned calls=  2055 unpruned calls=  32767
n=8 results= 1430 pruned calls=  6917 unpruned calls= 131071
random cross-check ok: 100 cases (n in 1..5; the oracle is exhaustive)
edge asserts ok
```

**Edge cases:**
- n = 1 returns `['()']`.
- n = 8: 1430 strings; the first is `'(((((((())))))))'` and the last is `'()()()()()()()()'` (asserted).
- The oracle test is exhaustive (all 2^(2n) strings for n <= 6), so the "random" loop only repeats small n; it adds no variety. I say that plainly.
- Prompt claims checked: Catalan count (n = 1..8), no dead prefix (n = 1..8): both true.

**Follow-ups:**
- Count only: Catalan DP, `C(n) = sum C(i) * C(n-1-i)`, O(n^2), no listing.
- Several bracket types: add a stack of open brackets instead of counters; the pruning changes (close only the matching top).
- Longest valid parentheses (a DP/stack problem, not enumeration).

**Common mistakes:**
- Pruning only at the end (test balance at leaves): that is the 2^(2n) brute force.
- Rule 2 written as `c < n` instead of `c < o`: then ')' can come first and invalid strings appear.
- Forgetting to pop after the recursive call (with a list buffer).
