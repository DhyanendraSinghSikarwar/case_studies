### Q10 ⭐⭐ 🟡 Recover the longest common subsequence itself. `a` and `b` are lowercase strings with 0 <= len <= 1000. Return a longest common subsequence as a string ('' if there is none). Many LCS strings can exist, so the tie rule is fixed: return the lexicographically smallest among all longest common subsequences. Build the table on suffixes (`f[i][j]` = LCS length of a[i:] and b[j:]) and walk forward, at each step taking the smallest letter c that has a next occurrence i' >= i in `a` and j' >= j in `b` with `1 + f[i'+1][j'+1] == f[i][j]`, using the FIRST such occurrences. Explain why the usual back-pointer walk from the bottom-right cell does not give this string by itself. Sizes are large enough that a memoised top-down recursion can nest deeper than CPython's default recursion limit of 1000 and raise RecursionError; a bottom-up (iterative) solution is required (do not rely on raising the limit). In the answer include a table walk-through on the first example and a seeded random cross-check of your solution against enumerating every common subsequence of strings of length at most 8 and taking the longest, then the smallest on small inputs. Example: a='abcde', b='ace' -> 'ace'; a='abcbdab', b='bdcaba' -> 'bcab'; a='abc', b='def' -> ''; a='zxy', b='xyz' -> 'xy'; a='', b='' -> ''.
**Asked at:** 2D DP pattern guides and lists (techinterview.org two-dimensional DP interview patterns, a LeetCode Discuss '13 DP patterns' post, codemia 2D DP and DP on strings and intervals; search snippets only, not opened) | Standard-problem lists known to the editor (not found as an opened page; indicative only, no company attribution)

**Pattern:** Two-sequence DP on suffixes, then a forward walk with an explicit tie rule. The table gives the LENGTH; the rule picks WHICH string.

**Say this first (1 line):** "f[i][j] is the LCS length of a[i:] and b[j:]; I fill it bottom-up, then walk forward from (0,0), at each step taking the smallest letter c whose first occurrences keep the total optimal, so the string comes out lexicographically smallest."

**Brute force:** Enumerate every subsequence of each string (2^len each), intersect the two sets, take the longest, break ties by the smaller string. Fine for len <= 8 (256 subsets each). Exponential, so it is only the checker.

**Optimal:**
- State: `f[i][j]` = LCS length of the suffixes `a[i:]` and `b[j:]`.
- Transition: if `a[i] == b[j]` then `f[i][j] = 1 + f[i+1][j+1]`; else `max(f[i+1][j], f[i][j+1])`.
- Base cases: `f[len(a)][j] = 0` and `f[i][len(b)] = 0` (an empty suffix has no common letters). That is why the table is `(m+1) x (n+1)` and starts as all zeros.
- Walk forward from `(0, 0)` while `f[i][j] > 0`. Try letters in order a..z. For letter c, let `i'` be the first index `>= i` with `a[i'] == c` and `j'` the first `>= j` with `b[j'] == c`. If both exist and `1 + f[i'+1][j'+1] == f[i][j]`, emit c and jump to `(i'+1, j'+1)`. Stop at the first letter that works.
- Why FIRST occurrences: jumping to the earliest match leaves the largest suffixes, so `f` can only be as large or larger than from a later match. If any occurrence of c works, the first one works. Taking the smallest working letter at every step gives the smallest string, because every longest answer has the same length (the length is fixed, so comparing letter by letter is valid).
- Why the usual back-pointer walk fails: it starts at the bottom-right of a PREFIX table and decides "up or left" on a tie by a fixed direction. That chooses a path, not a letter order. It builds the string from the END, and a good last letter says nothing about the first letters. It returns a correct longest subsequence, just not the smallest one. Measured below: it differs from the smallest on 49 of 500 random pairs, e.g. `abcbdab` / `bdcaba` gives `bcba`, the smallest is `bcab`.
- Space: reconstruction needs the whole table (it needs `f` at arbitrary cells), so O(mn). Two rows give only the length. Hirschberg's divide and conquer recovers one LCS in O(n) space, but the smallest-string rule is easier with the table.
- Recursion: the top-down version `f(i, j)` nests up to `m + n` frames. As observed on Python 3.13 with the default limit 1000: two random 300-letter strings run fine; two disjoint 1000-letter strings (worst case: depth 2000) raise `RecursionError`. The prompt needs 1000 x 1000, so use the loops. Observation, not a rule: depth depends on the strings and the call path.

**Complexity:** Table O(mn) time and space. The walk does at most `min(m, n)` steps, each scanning up to 26 letters with `str.index` (O(len) each), so O(min(m,n) * 26 * (m+n)) worst case, which stays below the table cost for the prompt sizes. Brute force O(2^m + 2^n).

**Dry run:** `a = 'abcde'`, `b = 'ace'`. Rows are `i` (suffix of a), columns `j` (suffix of b).

| | j=0 `ace` | j=1 `ce` | j=2 `e` | j=3 `` |
|---|---|---|---|---|
| i=0 `abcde` | 3 | 2 | 1 | 0 |
| i=1 `bcde` | 2 | 2 | 1 | 0 |
| i=2 `cde` | 2 | 2 | 1 | 0 |
| i=3 `de` | 1 | 1 | 1 | 0 |
| i=4 `e` | 1 | 1 | 1 | 0 |
| i=5 `` | 0 | 0 | 0 | 0 |

Walk: at `(0,0)` f=3. Letters common to both suffixes: a, c, e. Try `a`: first a at i'=0, j'=0, `1 + f[1][1] = 3` equals 3, emit `a`, go to (1,1). Now f=2: common letters c, e. Try `c`: i'=2, j'=1, `1 + f[3][2] = 2`, emit `c`, go to (3,2). f=1: only `e` is common, i'=4, j'=2, `1 + f[5][3] = 1`, emit `e`, go to (5,3). f=0, stop. Result `ace`.

**Code:**
```python
import itertools
import random
import sys
from functools import lru_cache

random.seed(1010)

def suffix_table(a, b):
    """f[i][j] = LCS length of a[i:] and b[j:]; row len(a) and column len(b) stay 0 (empty suffix)."""
    m, n = len(a), len(b)
    f = [[0] * (n + 1) for _ in range(m + 1)]
    for i in range(m - 1, -1, -1):
        for j in range(n - 1, -1, -1):
            if a[i] == b[j]:
                f[i][j] = 1 + f[i + 1][j + 1]
            else:
                f[i][j] = max(f[i + 1][j], f[i][j + 1])
    return f

def lcs_smallest(a, b):
    """Lexicographically smallest longest common subsequence, bottom-up, no recursion."""
    f = suffix_table(a, b)
    i = j = 0
    out = []
    while f[i][j]:
        # candidate letters are those present in both remaining suffixes, tried a..z
        for c in sorted(set(a[i:]) & set(b[j:])):
            ii, jj = a.index(c, i), b.index(c, j)        # FIRST occurrences at or after i / j
            if 1 + f[ii + 1][jj + 1] == f[i][j]:
                out.append(c)
                i, j = ii + 1, jj + 1
                break
    return ''.join(out)

def lcs_backpointer(a, b):
    """The classic walk: prefix table, start at the bottom-right cell, go up/left. NOT lexicographically smallest."""
    m, n = len(a), len(b)
    g = [[0] * (n + 1) for _ in range(m + 1)]
    for i in range(1, m + 1):
        for j in range(1, n + 1):
            g[i][j] = g[i-1][j-1] + 1 if a[i-1] == b[j-1] else max(g[i-1][j], g[i][j-1])
    i, j, out = m, n, []
    while i and j:
        if a[i-1] == b[j-1]:
            out.append(a[i-1]); i -= 1; j -= 1
        elif g[i-1][j] >= g[i][j-1]:
            i -= 1
        else:
            j -= 1
    return ''.join(reversed(out))

def lcs_memo(a, b):
    """Top-down version of the same table (shows the recursion-limit problem)."""
    @lru_cache(maxsize=None)
    def f(i, j):
        if i == len(a) or j == len(b):
            return 0
        if a[i] == b[j]:
            return 1 + f(i + 1, j + 1)
        return max(f(i + 1, j), f(i, j + 1))
    return f(0, 0)

def subseqs(s):
    return {''.join(s[i] for i in range(len(s)) if mask >> i & 1) for mask in range(1 << len(s))}

def brute(a, b):
    """Every common subsequence (len <= 8), longest first, then smallest."""
    common = subseqs(a) & subseqs(b)
    return min(common, key=lambda t: (-len(t), t))

# 1. prompt examples
for a, b, want in [('abcde', 'ace', 'ace'), ('abcbdab', 'bdcaba', 'bcab'), ('abc', 'def', ''), ('zxy', 'xyz', 'xy'), ('', '', '')]:
    assert lcs_smallest(a, b) == brute(a, b) == want, (a, b)
print('5 prompt examples ok')

# 2. hand-table source: suffix table for a='abcde', b='ace'
f = suffix_table('abcde', 'ace')
print("f for a='abcde' (rows i=0..5), b='ace' (cols j=0..3):")
for i, row in enumerate(f):
    print(' ', ('abcde' + '-')[i], row)

# 3. seeded random cross-check against full enumeration
for _ in range(400):
    a = ''.join(random.choice('abc') for _ in range(random.randint(0, 8)))
    b = ''.join(random.choice('abc') for _ in range(random.randint(0, 8)))
    assert lcs_smallest(a, b) == brute(a, b), (a, b)
print('400 seeded random pairs (len 0..8, alphabet abc): smallest-LCS walk == enumeration')

# 4. exhaustive: all pairs up to length 4 over {a,b} (961 pairs)
cnt = 0
words = [''.join(w) for n in range(5) for w in itertools.product('ab', repeat=n)]
for a in words:
    for b in words:
        assert lcs_smallest(a, b) == brute(a, b); cnt += 1
print('exhaustive pairs over {a,b}, len <= 4:', cnt, 'ok')

# 5. the claim: the back-pointer walk is NOT automatically the smallest string (but it is still a longest one)
diff = 0
for _ in range(500):
    a = ''.join(random.choice('abcd') for _ in range(random.randint(0, 8)))
    b = ''.join(random.choice('abcd') for _ in range(random.randint(0, 8)))
    x, y = lcs_backpointer(a, b), lcs_smallest(a, b)
    assert len(x) == len(y)
    diff += x != y
print('back-pointer walk differs from the smallest LCS on', diff, 'of 500 random pairs')
print("example: abcbdab / bdcaba -> back-pointer", lcs_backpointer('abcbdab', 'bdcaba'), "vs smallest", lcs_smallest('abcbdab', 'bdcaba'))

# 6. size and recursion limit (default limit)
print('recursion limit:', sys.getrecursionlimit())
x = ''.join(random.choice('abcd') for _ in range(1000)); y = ''.join(random.choice('abcd') for _ in range(1000))
r = lcs_smallest(x, y)
assert len(r) == len(lcs_backpointer(x, y))
print('bottom-up 1000 x 1000 random: LCS length', len(r))
print('memoised, two 300-letter random strings ->', lcs_memo(x[:300], y[:300]))
try:
    lcs_memo('a' * 1000, 'b' * 1000)
    print('memoised disjoint 1000 + 1000: ok')
except RecursionError:
    print('memoised disjoint 1000 + 1000: RecursionError')
print('bottom-up disjoint 1000 + 1000 ->', repr(lcs_smallest('a' * 1000, 'b' * 1000)))

# 7. edge cases
assert lcs_smallest('', 'abc') == '' and lcs_smallest('abc', '') == ''
assert lcs_smallest('aaa', 'aa') == 'aa' and lcs_smallest('ba', 'ab') == 'a'
assert lcs_smallest('abc', 'abc') == 'abc'
print('edge asserts ok')
```

**Output (my run):**
```
5 prompt examples ok
f for a='abcde' (rows i=0..5), b='ace' (cols j=0..3):
  a [3, 2, 1, 0]
  b [2, 2, 1, 0]
  c [2, 2, 1, 0]
  d [1, 1, 1, 0]
  e [1, 1, 1, 0]
  - [0, 0, 0, 0]
400 seeded random pairs (len 0..8, alphabet abc): smallest-LCS walk == enumeration
exhaustive pairs over {a,b}, len <= 4: 961 ok
back-pointer walk differs from the smallest LCS on 49 of 500 random pairs
example: abcbdab / bdcaba -> back-pointer bcba vs smallest bcab
recursion limit: 1000
bottom-up 1000 x 1000 random: LCS length 651
memoised, two 300-letter random strings -> 191
memoised disjoint 1000 + 1000: RecursionError
bottom-up disjoint 1000 + 1000 -> ''
edge asserts ok
```

**Edge cases:**
- Both empty returns `''`; one empty returns `''`; no common letter returns `''` (the walk never starts because `f[0][0] == 0`).
- Equal strings return the string itself.
- `a='zxy'`, `b='xyz'` returns `'xy'`, not `'z'`: two letters beat one.
- Repeated letters (`'aaa'` vs `'aa'`) return `'aa'`.

**Follow-ups:**
- Count how many distinct LCS strings exist? Another table with the same suffix idea, but you must avoid counting one string many times (use first occurrences per letter, exactly as the walk does).
- Only the length, in less memory? Two rows (or one row plus a saved diagonal), O(min(m,n)) space.
- One LCS in linear space? Hirschberg: split `a` in half, find the best split point of `b` from forward and backward length rows, recurse.

**Common mistakes:**
- Using the back-pointer walk and assuming the answer is the smallest string.
- Picking the smallest letter that merely appears in both suffixes, without checking `1 + f[i'+1][j'+1] == f[i][j]`.
- Using the LAST occurrence instead of the first.
- Memoised recursion at 1000 x 1000 (`RecursionError` on the default limit) and a `[[0]*n]*m` table (see Part 10 Q31).

### Q11 ⭐⭐ 🟡 Longest common substring (contiguous). `a` and `b` are lowercase strings with 0 <= len <= 2000. Return `[length, i, j]` where `length` is the largest L such that a[i:i+L] == b[j:j+L] for some i, j; if several pairs reach it, return the smallest i and, for that i, the smallest j. If there is no common character return `[0, -1, -1]`. Use `dp[i][j]` = length of the common suffix of a[:i] and b[:j] (reset to 0 on a mismatch, unlike LCS) and say why one row suffices and why the answer is the maximum over all cells, not the last cell. In the answer include a table walk-through on the first example and a seeded random cross-check of your solution against a brute force over all lengths and start pairs (len <= 8) on small inputs. Example: a='abcdxyz', b='xyzabcd' -> [4, 0, 3]; a='abc', b='def' -> [0, -1, -1]; a='aaa', b='aa' -> [2, 0, 0]; a='xabcx', b='yabcy' -> [3, 1, 1].
**Asked at:** 2D DP pattern guides and lists (techinterview.org two-dimensional DP interview patterns, a LeetCode Discuss '13 DP patterns' post, codemia 2D DP and DP on strings and intervals; search snippets only, not opened) | Standard-problem lists known to the editor (not found as an opened page; indicative only, no company attribution)

**Pattern:** Two-string DP where the state is "common block ENDING here". A mismatch resets to 0, which is the whole difference from LCS.

**Say this first (1 line):** "d[i][j] is the length of the longest common suffix of a[:i] and b[:j]: equal letters give d[i-1][j-1] + 1, a mismatch gives 0; the answer is the maximum over all cells, tracked as I go, and one row is enough."

**Brute force:** For every length L from the largest possible down to 1, for every start i in `a` and j in `b`, compare `a[i:i+L]` with `b[j:j+L]`. The first hit in (L desc, i asc, j asc) order is the answer. About O(min(m,n) * m * n * L) work, so only for len <= 8. It is the checker.

**Optimal:**
- State: `d[i][j]` = length of the longest common suffix of `a[:i]` and `b[:j]` (a block that must end at `a[i-1]` and `b[j-1]`).
- Transition: `a[i-1] == b[j-1]` gives `d[i-1][j-1] + 1`; otherwise `0`. A block cannot skip a letter, so there is no `max(up, left)`.
- Base cases: row 0 and column 0 are 0 (empty prefix).
- Answer: the maximum over ALL cells, not `d[m][n]`. `d[m][n]` is only the common suffix of the two whole strings. On the first example the last cell is 0 but the answer is 4.
- Position: a cell with value L at `(i, j)` means the block starts at `a[i-L]` and `b[j-L]`. Update the best when `L` is larger, or equal with a smaller `(i-L, j-L)`. Because the prompt wants the smallest start i and then the smallest j, compare the pair of starts; do not rely on scan order.
- One row: `d[i][j]` needs only `d[i-1][j-1]`, the diagonal. Keep one list `row` of length n+1 and run j DESCENDING: when you write `row[j]`, `row[j-1]` has not been touched yet this pass, so it still holds `d[i-1][j-1]`. On a mismatch you MUST write `row[j] = 0`; an old value left there would be a fake block.
- Recursion: the problem is naturally a loop; a memoised version has the same n x m state grid, so use the loops at 2000 x 2000.

**Complexity:** Time O(mn) (4M cell updates at 2000 x 2000; sandbox time is a few seconds at most, not a proof). Space O(n) with the row, O(mn) with the full table. Brute force is far worse.

**Dry run:** `a = 'abcdxyz'`, `b = 'xyzabcd'`. Only the non-zero cells are listed; all other cells are 0.

| cell (i, j) | letters | value |
|---|---|---|
| (1, 4) | a = a | 1 |
| (2, 5) | b = b, diagonal was 1 | 2 |
| (3, 6) | c = c | 3 |
| (4, 7) | d = d | 4 |
| (5, 1) | x = x | 1 |
| (6, 2) | y = y, diagonal was 1 | 2 |
| (7, 3) | z = z | 3 |

The maximum is 4 at `(4, 7)`, so the block starts at `i = 4 - 4 = 0` and `j = 7 - 4 = 3`: `[4, 0, 3]` (`'abcd'`). The last cell `(7, 7)` is 0.

**Code:**
```python
import itertools
import random
import time

random.seed(1111)

def table(a, b):
    """Full table: d[i][j] = length of the common SUFFIX of a[:i] and b[:j] (0 on a mismatch)."""
    d = [[0] * (len(b) + 1) for _ in range(len(a) + 1)]
    for i in range(1, len(a) + 1):
        for j in range(1, len(b) + 1):
            if a[i - 1] == b[j - 1]:
                d[i][j] = d[i - 1][j - 1] + 1
    return d

def lcsubstr(a, b):
    """One row. Returns [length, i, j]; ties: smallest i, then smallest j; no common letter -> [0, -1, -1]."""
    n = len(b)
    row = [0] * (n + 1)              # row[j] = d[i-1][j] before the update, d[i][j] after it
    best_len, best_i, best_j = 0, -1, -1
    for i in range(1, len(a) + 1):
        for j in range(n, 0, -1):    # descending: row[j-1] still holds d[i-1][j-1] (the diagonal)
            if a[i - 1] == b[j - 1]:
                row[j] = row[j - 1] + 1
                L = row[j]
                si, sj = i - L, j - L            # start indices of this common block
                if L > best_len or (L == best_len and (si, sj) < (best_i, best_j)):
                    best_len, best_i, best_j = L, si, sj
            else:
                row[j] = 0           # the reset that makes it a SUBSTRING table
    return [best_len, best_i, best_j]

def brute(a, b):
    """All lengths, longest first, all start pairs in order (len <= 8)."""
    for L in range(min(len(a), len(b)), 0, -1):
        for i in range(len(a) - L + 1):
            for j in range(len(b) - L + 1):
                if a[i:i + L] == b[j:j + L]:
                    return [L, i, j]
    return [0, -1, -1]

for a, b, want in [('abcdxyz', 'xyzabcd', [4, 0, 3]), ('abc', 'def', [0, -1, -1]), ('aaa', 'aa', [2, 0, 0]), ('xabcx', 'yabcy', [3, 1, 1])]:
    assert lcsubstr(a, b) == brute(a, b) == want, (a, b)
print('4 prompt examples ok')

d = table('abcdxyz', 'xyzabcd')
print("d for a='abcdxyz' (rows) vs b='xyzabcd' (cols):")
print('       ', '  '.join(c for c in ' ' + 'xyzabcd'))
for i, row in enumerate(d):
    print('  ', ' ' if i == 0 else 'abcdxyz'[i - 1], row)

for _ in range(500):
    a = ''.join(random.choice('abc') for _ in range(random.randint(0, 8)))
    b = ''.join(random.choice('abc') for _ in range(random.randint(0, 8)))
    assert lcsubstr(a, b) == brute(a, b), (a, b)
print('500 seeded random pairs (len 0..8, alphabet abc): one-row DP == brute force')

cnt = 0
words = [''.join(w) for n in range(5) for w in itertools.product('ab', repeat=n)]
for a in words:
    for b in words:
        assert lcsubstr(a, b) == brute(a, b); cnt += 1
print('exhaustive pairs over {a,b}, len <= 4:', cnt, 'ok')

# why the answer is the MAX over all cells, not the last cell: d[m][n] is only the common suffix length
a, b = 'abcdxyz', 'xyzabcd'
print('last cell d[m][n] =', table(a, b)[-1][-1], 'but the answer is', lcsubstr(a, b)[0])
assert table(a, b)[-1][-1] == 0

# max size 2000 x 2000 (sandbox timing only)
x = ''.join(random.choice('ab') for _ in range(2000)); y = ''.join(random.choice('ab') for _ in range(2000))
t = time.perf_counter(); r = lcsubstr(x, y); dt = time.perf_counter() - t
assert x[r[1]:r[1] + r[0]] == y[r[2]:r[2] + r[0]]
print('2000 x 2000 over {a,b}: length', r[0], 'found; sandbox time under 5 s:', dt < 5)
print('2000 a vs 2000 a ->', lcsubstr('a' * 2000, 'a' * 2000))

assert lcsubstr('', '') == [0, -1, -1] and lcsubstr('a', '') == [0, -1, -1]
assert lcsubstr('abab', 'abab') == [4, 0, 0] and lcsubstr('ab', 'ba') == [1, 0, 1]
print('edge asserts ok')
```

**Output (my run):**
```
4 prompt examples ok
d for a='abcdxyz' (rows) vs b='xyzabcd' (cols):
           x  y  z  a  b  c  d
     [0, 0, 0, 0, 0, 0, 0, 0]
   a [0, 0, 0, 0, 1, 0, 0, 0]
   b [0, 0, 0, 0, 0, 2, 0, 0]
   c [0, 0, 0, 0, 0, 0, 3, 0]
   d [0, 0, 0, 0, 0, 0, 0, 4]
   x [0, 1, 0, 0, 0, 0, 0, 0]
   y [0, 0, 2, 0, 0, 0, 0, 0]
   z [0, 0, 0, 3, 0, 0, 0, 0]
500 seeded random pairs (len 0..8, alphabet abc): one-row DP == brute force
exhaustive pairs over {a,b}, len <= 4: 961 ok
last cell d[m][n] = 0 but the answer is 4
2000 x 2000 over {a,b}: length 25 found; sandbox time under 5 s: True
2000 a vs 2000 a -> [2000, 0, 0]
edge asserts ok
```

**Edge cases:**
- Nothing in common returns `[0, -1, -1]`; either string empty returns the same.
- `a='aaa'`, `b='aa'` returns `[2, 0, 0]` (smallest i, then smallest j), not `[2, 1, 0]`.
- Identical strings return `[n, 0, 0]`.
- Several blocks of the same length: the smaller start in `a` wins, then the smaller start in `b`.

**Follow-ups:**
- Linear space AND fast for huge strings? A suffix automaton or suffix array solves it in O(m + n) or O(n log n); the DP is the interview baseline.
- Return the substring itself? `a[i:i+length]`.
- Why not LCS code with a tweak? In LCS a mismatch carries `max(up, left)`; a substring must be contiguous, so the mismatch must reset.

**Common mistakes:**
- Returning `d[m][n]` instead of the maximum over all cells.
- Forgetting the reset to 0 on a mismatch (it silently turns the code into something between LCS and nonsense).
- Running j ascending in the one-row version (the diagonal gets overwritten).
- Reporting the END indices instead of the START indices the prompt asks for.

### Q12 ⭐⭐ 🟡 Count palindromic substrings with a DP table. `s` is a lowercase string with 1 <= len <= 1000. Count the substrings (by position) that are palindromes. Part 3 Q9 owns expand-around-center and Part 3 Q8 the longest palindromic substring; here use the interval table `dp[i][j] = s[i] == s[j] and (j - i < 3 or dp[i+1][j-1])`, say in which order i and j must be filled so that `dp[i+1][j-1]` is ready, then shrink it to ONE row and say which direction the inner loop must run. State the time and space of both this and expand-around-center, and when each wins. In the answer include a table walk-through on the first example and a seeded random cross-check of your solution against enumerating every substring and checking it, and expand-around-center on small inputs. Example: s='abc' -> 3; s='aaa' -> 6; s='abba' -> 6; s='a' -> 1; s='abacaba' -> 12.
**Asked at:** 2D DP pattern guides and lists (techinterview.org two-dimensional DP interview patterns, a LeetCode Discuss '13 DP patterns' post, codemia 2D DP and DP on strings and intervals; search snippets only, not opened) | Candidate-reported Flipkart rounds (a 2020 on-campus Naukri Code360 report with a longest palindromic substring solved by a 2-D boolean DP table, a 2024 off-campus SDE-1 LeetCode Discuss report with a 2D DP array-splitting question; search-result summaries only, pages not opened; self-reported, unverified)

**Pattern:** Interval DP on substrings `[i, j]`: a substring is a palindrome if its ends match and the inside is a palindrome.

**Say this first (1 line):** "dp[i][j] is true if s[i..j] is a palindrome: s[i] == s[j] and (the inside is at most one letter, or dp[i+1][j-1]); I fill i from the end and j upward so the inside is ready, count the trues, and one row suffices if j runs downward."

**Brute force:** Take every substring (n(n+1)/2 of them), reverse it, compare. O(n^3) time. It is the checker.

**Optimal:**
- State: `dp[i][j]` = `s[i..j]` is a palindrome (`i <= j`).
- Transition: `dp[i][j] = s[i] == s[j] and (j - i < 3 or dp[i+1][j-1])`. When `j - i < 3` the inside has length 0 or 1 (`j-i = 1` is a pair, `j-i = 2` has one middle letter), which is always a palindrome, so no lookup is needed.
- Base cases: every `dp[i][i]` is true (single letters); the `j - i < 3` branch covers pairs and triples.
- Order: `dp[i][j]` reads `dp[i+1][j-1]`, the row BELOW and one column left. So `i` must go from `n-1` down to 0 (or, equivalently, by increasing length). Within a row `j` can go either way for the full table.
- Count: add 1 for every true cell.
- One row: keep `dp[j]` meaning "`s[i..j]` is a palindrome for the current i". Cell `(i, j)` needs old-row `dp[j-1]`. Run `j` DESCENDING (from `n-1` to `i`): `dp[j-1]` has not yet been overwritten when you compute `dp[j]`. Ascending would read the new row's value and is wrong; the code measures this: wrong on 248 of 300 random strings of length 8.
- Compared with expand-around-center (Part 3 Q9): centres use 2n-1 centres, each expands while the ends match, O(n^2) time worst case (all letters equal), O(n) typical, and O(1) space. The DP is O(n^2) time always, O(n^2) space for the table, O(n) for the row. For this question centres win (less space, usually faster, simpler); the DP wins when you will ask many "is s[i..j] a palindrome?" queries or need the table for another DP (such as minimum palindrome cuts).
- Recursion: `pal(i, j)` recursion peels two letters per call, so its depth is about n/2. As observed on Python 3.13 with the default limit, the memoised version works at n = 1000 (all `a`, depth about 500), well inside 1000. At n = 2100 (all `a`, depth about 1050) it raises `RecursionError` (shown in the code). The prompt stops at 1000, but the safe habit is still the loops; the exact depth is an observation, not a rule.

**Complexity:** DP: time O(n^2), space O(n^2) for the table or O(n) for one row. Centres: time O(n^2) worst case, O(1) space. Brute force O(n^3).

**Dry run:** `s = 'abba'`. T marks a palindrome.

| i \ j | 0 `a` | 1 `b` | 2 `b` | 3 `a` |
|---|---|---|---|---|
| 0 `a` | T | . | . | T |
| 1 `b` | | T | T | . |
| 2 `b` | | | T | . |
| 3 `a` | | | | T |

Fill order i = 3, 2, 1, 0. Row 3: `(3,3)` T. Row 2: `(2,2)` T, `(2,3)` b != a so `.`. Row 1: `(1,1)` T; `(1,2)` b = b and `j-i = 1 < 3`, T; `(1,3)` b != a, `.`. Row 0: `(0,0)` T; `(0,1)` a != b; `(0,2)` a != b; `(0,3)` a = a and `j-i = 3` is not below 3, so it needs `dp[1][2]`, which is T, so T. Total 4 singles + `bb` + `abba` = 6.

**Code:**
```python
import random
import sys
from functools import lru_cache

random.seed(1212)

def count_table(s):
    """Full interval table. dp[i][j] = s[i..j] is a palindrome. i DESCENDING, j ASCENDING so dp[i+1][j-1] is ready."""
    n = len(s)
    dp = [[False] * n for _ in range(n)]
    cnt = 0
    for i in range(n - 1, -1, -1):
        for j in range(i, n):
            dp[i][j] = s[i] == s[j] and (j - i < 3 or dp[i + 1][j - 1])
            cnt += dp[i][j]
    return cnt, dp

def count_row(s):
    """ONE row. dp[j] means 'is s[i..j] a palindrome' for the current i. j DESCENDING so dp[j-1] still holds row i+1."""
    n = len(s)
    dp = [False] * n
    cnt = 0
    for i in range(n - 1, -1, -1):
        for j in range(n - 1, i - 1, -1):
            dp[j] = s[i] == s[j] and (j - i < 3 or dp[j - 1])
            cnt += dp[j]
    return cnt

def count_center(s):
    """Expand around each of the 2n-1 centres (Part 3 Q9 idea)."""
    n, cnt = len(s), 0
    for c in range(2 * n - 1):
        l, r = c // 2, c // 2 + c % 2
        while l >= 0 and r < n and s[l] == s[r]:
            cnt += 1; l -= 1; r += 1
    return cnt

def brute(s):
    return sum(s[i:j] == s[i:j][::-1] for i in range(len(s)) for j in range(i + 1, len(s) + 1))

def count_memo(s):
    @lru_cache(maxsize=None)
    def pal(i, j):
        if i >= j: return True
        return s[i] == s[j] and pal(i + 1, j - 1)
    return sum(pal(i, j) for i in range(len(s)) for j in range(i, len(s)))

for s, want in [('abc', 3), ('aaa', 6), ('abba', 6), ('a', 1), ('abacaba', 12)]:
    assert count_table(s)[0] == count_row(s) == count_center(s) == brute(s) == want, s
print('5 prompt examples ok')

cnt, dp = count_table('abba')
print("dp for s='abba' (row i, col j, T = palindrome):")
print('     ', ' '.join('abba'))
for i, row in enumerate(dp):
    print('  ', 'abba'[i], ' '.join('T' if v else '.' for v in row))
print('count =', cnt)

for _ in range(1000):
    s = ''.join(random.choice('ab') for _ in range(random.randint(1, 12)))
    assert count_table(s)[0] == count_row(s) == count_center(s) == brute(s) == count_memo(s), s
print('1000 seeded random strings (len 1..12, alphabet ab): table == one row == centres == enumeration == memo')

# what breaks if the one-row inner loop runs ASCENDING: dp[j-1] would already be row i, not row i+1
def bad_row(s):
    n = len(s); dp = [False] * n; cnt = 0
    for i in range(n - 1, -1, -1):
        for j in range(i, n):
            dp[j] = s[i] == s[j] and (j - i < 3 or dp[j - 1]); cnt += dp[j]
    return cnt
wrong = sum(bad_row(s) != brute(s) for s in (''.join(random.choice('ab') for _ in range(8)) for _ in range(300)))
print('ascending inner loop in the one-row version is wrong on', wrong, 'of 300 random strings')
assert wrong > 0

big = 'a' * 1000
print('n = 1000 all a:', count_row(big), '== n(n+1)/2 =', 1000 * 1001 // 2)
assert count_row(big) == count_table(big)[0] == count_center(big) == 500500
rnd = ''.join(random.choice('ab') for _ in range(1000))
assert count_row(rnd) == count_center(rnd)
print('random 1000 over {a,b}: DP row == centres ==', count_row(rnd))

# memoised version: recursion depth is only ~n/2 per call chain, but the outer loop makes n^2/2 cache entries
print('recursion limit:', sys.getrecursionlimit(), '| memo n=1000 all a:', end=' ')
try:
    print(count_memo(big))
except RecursionError:
    print('RecursionError')
print('memo n=2100 all a (depth about 1050):', end=' ')
try:
    count_memo('a' * 2100); print('ok')
except RecursionError:
    print('RecursionError')
assert count_center('') == 0
print('edge asserts ok')
```

**Output (my run):**
```
5 prompt examples ok
dp for s='abba' (row i, col j, T = palindrome):
      a b b a
   a T . . T
   b . T T .
   b . . T .
   a . . . T
count = 6
1000 seeded random strings (len 1..12, alphabet ab): table == one row == centres == enumeration == memo
ascending inner loop in the one-row version is wrong on 248 of 300 random strings
n = 1000 all a: 500500 == n(n+1)/2 = 500500
random 1000 over {a,b}: DP row == centres == 3065
recursion limit: 1000 | memo n=1000 all a: 500500
memo n=2100 all a (depth about 1050): RecursionError
edge asserts ok
```

**Edge cases:**
- `'a'` returns 1; all-equal letters of length n return n(n+1)/2 (500500 at n = 1000).
- No equal neighbours (`'abc'`) returns n.
- Count by position: `'aaa'` has 6 (three `a`, two `aa`, one `aaa`), not 3 distinct strings.
- The `j - i < 3` guard: without it you would read `dp[i+1][j-1]` with `j-1 < i+1`, an empty interval, a classic off-by-one.

**Follow-ups:**
- Longest palindromic substring? Track the longest true cell (Part 3 Q8); same table.
- Minimum cuts into palindromes? Use the table as `pal[l][r]` and a 1D cuts array.
- Manacher's algorithm? O(n) time; mention it, you rarely code it.

**Common mistakes:**
- Filling rows top to bottom (`dp[i+1][j-1]` is not ready).
- Using `j - i < 2` and then reading an empty or out-of-range interval, or `<= 3` which wrongly accepts `abca`.
- Running the one-row loop upward.
- Counting distinct palindromes instead of positions.

### Q13 ⭐⭐ 🟡 Interleaving string. `s1`, `s2` and `s3` are lowercase strings with 0 <= len(s1), len(s2) <= 100 and 0 <= len(s3) <= 200. `s3` is an interleaving of `s1` and `s2` if it can be formed by merging them while keeping the relative order of the letters of each (take letters from either string in turn, any number at a time). Return True or False (all three empty is True; unequal lengths is False). Define `dp[i][j]` = the first i letters of s1 and the first j of s2 interleave into the first i + j of s3, give the transition, and then use one row of length len(s2) + 1. In the answer include a table walk-through on the first example and a seeded random cross-check of your solution against a plain recursion without a memo (len(s1), len(s2) <= 6) on small inputs. Example: s1='aabcc', s2='dbbca', s3='aadbbcbcac' -> True; s1='aabcc', s2='dbbca', s3='aadbbbaccc' -> False; s1='', s2='', s3='' -> True; s1='a', s2='', s3='b' -> False.
**Asked at:** 2D DP pattern guides and lists (techinterview.org two-dimensional DP interview patterns, a LeetCode Discuss '13 DP patterns' post, codemia 2D DP and DP on strings and intervals; search snippets only, not opened) | Standard-problem lists known to the editor (not found as an opened page; indicative only, no company attribution)

**Pattern:** Two-string DP where the position in the THIRD string is forced: `k = i + j`. The table only needs the pair (i, j).

**Say this first (1 line):** "dp[i][j] is true if the first i letters of s1 and the first j of s2 can interleave into the first i + j of s3: the last letter of that prefix came from s1 (dp[i-1][j] and s1[i-1] == s3[i+j-1]) or from s2 (dp[i][j-1] and s2[j-1] == s3[i+j-1]); one row of length len(s2) + 1 is enough."

**Brute force:** Plain recursion `f(i, j)`: look at `s3[i+j]` and branch into "take from s1" and "take from s2" when the letters match. Up to 2^(m+n) calls when many letters are equal, so only for len(s1), len(s2) <= 6. It is the checker.

**Optimal:**
- Quick reject: `len(s1) + len(s2) != len(s3)` is False.
- State: `dp[i][j]` = the first i letters of s1 and the first j letters of s2 interleave into the first `i + j` letters of s3.
- Transition: `dp[i][j] = (i > 0 and dp[i-1][j] and s1[i-1] == s3[i+j-1]) or (j > 0 and dp[i][j-1] and s2[j-1] == s3[i+j-1])`.
- Base case: `dp[0][0] = True` (all three empty). Row 0 and column 0 come out of the same transition with one term guarded away.
- Why `s3` needs no index of its own: after taking i letters from s1 and j from s2, exactly i + j letters of s3 are used.
- One row: keep `dp[j]` for the current i. Before you overwrite it, `dp[j]` still holds `(i-1, j)` (the "from s1" term), and `dp[j-1]` was just written for this row, so it holds `(i, j-1)` (the "from s2" term). Loop j upward and assign `dp[j] = ok` every time (set it to False when neither term holds, never leave the old value).
- Recursion: the top-down depth is `len(s3) <= 200`, far under 1000. As observed on Python 3.13 the memoised version runs at the maximum size 100 + 100 (all `a`, depth 200). Nothing here needs bottom-up for safety, but the table is still the cleaner interview answer.
- Greedy matching ("take from s1 whenever the letters match") is wrong when both strings offer the same letter; the table keeps both possibilities.

**Complexity:** Time O(mn), space O(n) with the row (O(mn) with the table). Brute force up to O(2^(m+n)).

**Dry run:** `s1 = 'aabcc'`, `s2 = 'dbbca'`, `s3 = 'aadbbcbcac'`. T = true, `.` = false. Row label = letters of s1 used so far, column label = letters of s2 used so far.

| i \ j | 0 | 1 `d` | 2 `db` | 3 `dbb` | 4 `dbbc` | 5 `dbbca` |
|---|---|---|---|---|---|---|
| 0 | T | . | . | . | . | . |
| 1 `a` | T | . | . | . | . | . |
| 2 `aa` | T | T | T | T | T | . |
| 3 `aab` | . | T | T | . | T | . |
| 4 `aabc` | . | . | T | T | T | T |
| 5 `aabcc` | . | . | . | T | . | T |

Check a few cells. `(2,1)`: s3 prefix of 3 letters is `aad`; from `(2,0)` T plus `s2[0] = d == s3[2] = d`, so T. `(1,1)`: prefix `aa`; from `(0,1)` F (s2 letter `d` != `a`) and `(1,0)` T with `s2[0] = d != s3[1] = a`, so F. `(2,5)`: prefix of 7 is `aadbbcb`, last letter `b`, but `s1[1] = a` and `s2[4] = a`: F. `(5,5)`: last letter `c` (s3[9]); the s1 term needs `dp[4][5]` T and `s1[4] = c`: T. The answer is `dp[5][5] = True`.

**Code:**
```python
import itertools
import random
import sys
from functools import lru_cache

random.seed(1313)

def interleave_table(s1, s2, s3):
    """dp[i][j] = first i letters of s1 and first j of s2 interleave into the first i + j of s3."""
    m, n = len(s1), len(s2)
    if m + n != len(s3):
        return None
    dp = [[False] * (n + 1) for _ in range(m + 1)]
    dp[0][0] = True
    for i in range(m + 1):
        for j in range(n + 1):
            if i and dp[i - 1][j] and s1[i - 1] == s3[i + j - 1]:
                dp[i][j] = True
            if j and dp[i][j - 1] and s2[j - 1] == s3[i + j - 1]:
                dp[i][j] = True
    return dp

def interleave(s1, s2, s3):
    """One row of length len(s2) + 1. Before the update dp[j] is (i-1, j); dp[j-1] is already (i, j-1)."""
    m, n = len(s1), len(s2)
    if m + n != len(s3):
        return False
    dp = [False] * (n + 1)
    for i in range(m + 1):
        for j in range(n + 1):
            if i == 0 and j == 0:
                dp[0] = True
                continue
            ok = False
            if i and dp[j] and s1[i - 1] == s3[i + j - 1]:        # last letter came from s1
                ok = True
            if j and dp[j - 1] and s2[j - 1] == s3[i + j - 1]:    # last letter came from s2
                ok = True
            dp[j] = ok          # overwrites (i-1, j); for i = 0 the old value is not read (guarded by `i and`)
    return dp[n]

def interleave_memo(s1, s2, s3):
    if len(s1) + len(s2) != len(s3):
        return False
    @lru_cache(maxsize=None)
    def f(i, j):
        k = i + j
        if k == len(s3):
            return True
        return (i < len(s1) and s1[i] == s3[k] and f(i + 1, j)) or (j < len(s2) and s2[j] == s3[k] and f(i, j + 1))
    return f(0, 0)

def brute(s1, s2, s3):
    """Plain recursion, no memo (len(s1), len(s2) <= 6)."""
    def f(i, j):
        k = i + j
        if k == len(s3):
            return i == len(s1) and j == len(s2)
        return (i < len(s1) and s1[i] == s3[k] and f(i + 1, j)) or (j < len(s2) and s2[j] == s3[k] and f(i, j + 1))
    return len(s1) + len(s2) == len(s3) and f(0, 0)

for a, b, c, want in [('aabcc', 'dbbca', 'aadbbcbcac', True), ('aabcc', 'dbbca', 'aadbbbaccc', False), ('', '', '', True), ('a', '', 'b', False)]:
    assert interleave(a, b, c) == interleave_memo(a, b, c) == brute(a, b, c) == want, (a, b, c)
print('4 prompt examples ok')

dp = interleave_table('aabcc', 'dbbca', 'aadbbcbcac')
print("dp for s1='aabcc' (rows i=0..5), s2='dbbca' (cols j=0..5), T = true:")
print('      ', ' '.join('-dbbca'))
for i, row in enumerate(dp):
    print('  ', '-aabcc'[i], ' '.join('T' if v else '.' for v in row))

true_cases = 0
for _ in range(2000):
    s1 = ''.join(random.choice('abc') for _ in range(random.randint(0, 6)))
    s2 = ''.join(random.choice('abc') for _ in range(random.randint(0, 6)))
    if random.random() < 0.5:                       # build a true interleaving
        pool, i, j, out = (s1, s2), 0, 0, []
        while i < len(s1) or j < len(s2):
            if j == len(s2) or (i < len(s1) and random.random() < 0.5): out.append(s1[i]); i += 1
            else: out.append(s2[j]); j += 1
        s3 = ''.join(out)
        if random.random() < 0.3 and s3:           # corrupt one letter sometimes
            k = random.randrange(len(s3)); s3 = s3[:k] + random.choice('abc') + s3[k + 1:]
    else:
        s3 = ''.join(random.choice('abc') for _ in range(random.randint(0, 12)))
    r = interleave(s1, s2, s3)
    assert r == brute(s1, s2, s3) == interleave_memo(s1, s2, s3), (s1, s2, s3)
    assert (interleave_table(s1, s2, s3) or [[False]])[-1][-1] == r
    true_cases += r
print('2000 seeded random triples: one row == plain recursion == memo == table; True in', true_cases, 'of 2000 (both answers occur)')
assert 0 < true_cases < 2000

cnt = 0
for l1 in range(4):
    for l2 in range(4):
        for s1 in itertools.product('ab', repeat=l1):
            for s2 in itertools.product('ab', repeat=l2):
                for s3 in itertools.product('ab', repeat=l1 + l2):
                    a, b, c = ''.join(s1), ''.join(s2), ''.join(s3)
                    assert interleave(a, b, c) == brute(a, b, c); cnt += 1
print('exhaustive over {a,b}, len(s1), len(s2) <= 3, len(s3) = len(s1) + len(s2):', cnt, 'ok')

# maximum size and recursion depth (the memo recursion depth is len(s3) <= 200)
print('recursion limit:', sys.getrecursionlimit())
x, y = 'a' * 100, 'a' * 100
print('max size 100 + 100 -> 200, all a: row', interleave(x, y, 'a' * 200), '| memo (depth 200)', interleave_memo(x, y, 'a' * 200))
x = ''.join(random.choice('ab') for _ in range(100)); y = ''.join(random.choice('ab') for _ in range(100))
z = ''.join(x[i // 2] if i % 2 == 0 else y[i // 2] for i in range(200))      # strict alternation is a valid interleaving
assert interleave(x, y, z) and interleave_memo(x, y, z)
print('alternating merge of two random 100-letter strings:', interleave(x, y, z))

assert interleave('', 'abc', 'abc') and interleave('abc', '', 'abc') and not interleave('a', 'b', 'a')
assert not interleave('a', 'b', 'abc')
print('edge asserts ok')
```

**Output (my run):**
```
4 prompt examples ok
dp for s1='aabcc' (rows i=0..5), s2='dbbca' (cols j=0..5), T = true:
       - d b b c a
   - T . . . . .
   a T . . . . .
   a T T T T T .
   b . T T . T .
   c . . T T T T
   c . . . T . T
2000 seeded random triples: one row == plain recursion == memo == table; True in 828 of 2000 (both answers occur)
exhaustive over {a,b}, len(s1), len(s2) <= 3, len(s3) = len(s1) + len(s2): 7225 ok
recursion limit: 1000
max size 100 + 100 -> 200, all a: row True | memo (depth 200) True
alternating merge of two random 100-letter strings: True
edge asserts ok
```

**Edge cases:**
- All three empty returns True; `s1 = ''` reduces to `s2 == s3`.
- Length mismatch returns False before any table work.
- `s1 = 'a'`, `s2 = ''`, `s3 = 'b'` returns False.
- Same letters everywhere (`a` repeated): every split works, so a greedy "prefer s1" stays right by luck; random letters expose it.

**Follow-ups:**
- Count the number of ways? Replace `or` by `+` (and `and` by multiplication of the flag), same table.
- Three strings and an interleaving of k strings? State grows to a k-tuple; the idea is the same, the cost is the product of the lengths.
- Return one interleaving? Keep the full table and walk back from `(m, n)`, choosing the term that is true.

**Common mistakes:**
- Forgetting the length check, then indexing `s3` out of range.
- Off-by-one on `s3`: the letter being placed is `s3[i+j-1]` (1-based prefix lengths), not `s3[i+j]`.
- In the one-row version, leaving `dp[j]` unchanged when neither term holds (a stale True survives).
- Using `[[False]*(n+1)]*(m+1)` for the table (see Part 10 Q31).

### Q14 ⭐⭐ 🟡 Minimum path sum, and the path itself. `grid` is an m x n list of lists (1 <= m, n <= 200) of integers in 0..100. Moves are right 'R' or down 'D'. Return `[best, moves]` where `best` is the minimum path sum and `moves` is the string of m + n - 2 moves of an optimal path. Several optimal paths may exist, so the tie rule is fixed: among all minimum-sum paths return the lexicographically smallest move string with 'D' < 'R'. Build the table on SUFFIXES (cost from the cell to the end) so that at each cell you can step 'D' whenever it keeps the total optimal, and explain why walking back from the end with parent pointers does not give this string automatically. The 1 x 1 grid returns `[value, '']`. In the answer include a table walk-through on the first example and a seeded random cross-check of your solution against enumerating every path (m, n <= 5) and taking the smallest (sum, string) pair on small inputs. Example: grid=[[1, 3, 1], [1, 5, 1], [4, 2, 1]] -> [7, 'RRDD']; grid=[[1, 1], [1, 1]] -> [3, 'DR']; grid=[[5]] -> [5, '']; grid=[[0, 0, 0], [0, 0, 0]] -> [0, 'DRR'].
**Asked at:** 2D DP pattern guides and lists (techinterview.org two-dimensional DP interview patterns, a LeetCode Discuss '13 DP patterns' post, codemia 2D DP and DP on strings and intervals; search snippets only, not opened) | Standard-problem lists known to the editor (not found as an opened page; indicative only, no company attribution)

**Pattern:** Grid DP (right/down moves) plus path reconstruction under an explicit tie rule. The tie rule decides the table direction.

**Say this first (1 line):** "f[i][j] is the cheapest cost from (i, j) to the bottom-right cell; f[i][j] = grid[i][j] + min(f[i+1][j], f[i][j+1]); then I walk from the start and step D whenever D still keeps the total optimal, otherwise R, which gives the smallest D < R string."

**Brute force:** Enumerate every path: choose which of the `m + n - 2` moves are D (`C(m+n-2, m-1)` paths), sum the cells, keep the smallest `(sum, string)` pair. Fine for m, n <= 5 (at most 70 paths). It is the checker, and it applies the same tie rule by comparing the move strings.

**Optimal:**
- State: `f[i][j]` = minimum sum of a path from `(i, j)` to `(m-1, n-1)`, including the cell `(i, j)`. This is the SUFFIX direction.
- Transition: `f[i][j] = grid[i][j] + min(f[i+1][j], f[i][j+1])` (down or right). Use a border of infinity on row m and column n so edge cells have only one real option.
- Base case: `f[m-1][n-1] = grid[m-1][n-1]`.
- Walk forward from `(0, 0)`: at each cell, D is allowed to be chosen when `f[i+1][j] <= f[i][j+1]`, because then the remaining cost after stepping down equals the best remaining cost. If `D` is cheaper or equal, take `D` (tie goes to D, since `'D' < 'R'`); otherwise take `R`. On the last row or column the infinite border forces the only legal move.
- Why this is the lexicographically smallest optimal string: the first move is the most significant character. The suffix table tells us, at every cell, exactly which first moves stay optimal, so choosing the smaller letter among them at every step is greedy-correct.
- Why parent pointers from the end do not do it: with a PREFIX table (cost from the start) you walk back from the end and decide the LAST move first. A tie rule there ("came from above") fixes the last letters, not the first letters, so the string it returns is some optimal path but not the smallest. Measured below: on `[[1,1],[1,1]]` it gives `RD`, the rule wants `DR`; it differs on 264 of 500 random grids. The sum is the same, the string is not.
- Greedy "step to the cheaper neighbour" is not the DP at all: it gets the sum wrong on 184 of 500 random 4 x 4 grids.
- One row: the value alone needs only `row[j] = grid[i][j] + min(row[j], row[j+1])` going j downward (old `row[j]` is the cell below, `row[j+1]` is the cell to the right, just updated). Reconstruction needs the full table.
- Recursion: memoised `f(i, j)` nests `m + n - 1` frames. As observed on Python 3.13 with the default limit 1000: 200 x 200 (depth 399) runs, 600 x 600 (depth 1199) raises `RecursionError`. The prompt's maximum, 200 x 200, is safe, but bottom-up is the habit.

**Complexity:** Time O(mn), space O(mn) for the table (needed for the walk), O(n) for the value only. Walk O(m + n). Brute force O(C(m+n-2, m-1) * (m+n)).

**Dry run:** `grid = [[1,3,1],[1,5,1],[4,2,1]]`. Suffix table `f`:

| | j=0 | j=1 | j=2 |
|---|---|---|---|
| i=0 | 7 | 6 | 3 |
| i=1 | 8 | 7 | 2 |
| i=2 | 7 | 3 | 1 |

Fill order bottom-right to top-left: `f[2][2] = 1`; `f[2][1] = 2 + 1 = 3`; `f[2][0] = 4 + 3 = 7`; `f[1][2] = 1 + 1 = 2`; `f[1][1] = 5 + min(3, 2) = 7`; `f[1][0] = 1 + min(7, 7) = 8`; `f[0][2] = 1 + 2 = 3`; `f[0][1] = 3 + min(7, 3) = 6`; `f[0][0] = 1 + min(8, 6) = 7`. Best sum 7.
Walk: at `(0,0)` D leads to 8, R to 6, so R (f = 1 + 6). At `(0,1)` D leads to 7, R to 3, so R. At `(0,2)` only D (border): D. At `(1,2)` only D: D. Result `RRDD`.
A tie example is `[[1,1],[1,1]]`: at `(0,0)` D and R both lead to 2, so the rule picks D, giving `DR`.

**Code:**
```python
import itertools
import random
import sys
import time
from functools import lru_cache

random.seed(1414)
INF = float('inf')

def suffix_table(grid):
    """f[i][j] = minimum cost of a path from (i, j) to the bottom-right cell, cell (i, j) included."""
    m, n = len(grid), len(grid[0])
    f = [[INF] * (n + 1) for _ in range(m + 1)]        # a border of INF so out-of-grid moves never win
    for i in range(m - 1, -1, -1):
        for j in range(n - 1, -1, -1):
            if i == m - 1 and j == n - 1:
                f[i][j] = grid[i][j]
            else:
                f[i][j] = grid[i][j] + min(f[i + 1][j], f[i][j + 1])
    return f

def min_path(grid):
    """[best, moves]: smallest sum, then lexicographically smallest move string with 'D' < 'R'."""
    m, n = len(grid), len(grid[0])
    f = suffix_table(grid)
    i = j = 0
    out = []
    while (i, j) != (m - 1, n - 1):
        if f[i + 1][j] <= f[i][j + 1]:          # D keeps the total optimal whenever it is no worse; tie -> D
            out.append('D'); i += 1
        else:
            out.append('R'); j += 1
    return [f[0][0], ''.join(out)]

def min_sum_one_row(grid):
    """Value only, one row (reconstruction needs the full table). row[j] = cost from (i, j) to the end."""
    m, n = len(grid), len(grid[0])
    row = [INF] * (n + 1)
    for i in range(m - 1, -1, -1):
        for j in range(n - 1, -1, -1):
            if i == m - 1 and j == n - 1:
                row[j] = grid[i][j]
            else:
                row[j] = grid[i][j] + min(row[j], row[j + 1])    # row[j] = below (old row), row[j+1] = right (new row)
    return row[0]

def prefix_parent_walk(grid):
    """The tempting alternative: prefix table g (cost from the start), then walk back from the end by parent pointers."""
    m, n = len(grid), len(grid[0])
    g = [[INF] * n for _ in range(m)]
    for i in range(m):
        for j in range(n):
            g[i][j] = grid[i][j] + (0 if i == j == 0 else min(g[i - 1][j] if i else INF, g[i][j - 1] if j else INF))
    i, j, out = m - 1, n - 1, []
    while (i, j) != (0, 0):
        if i and (not j or g[i - 1][j] <= g[i][j - 1]):    # tie: arrived by D
            out.append('D'); i -= 1
        else:
            out.append('R'); j -= 1
    return [g[m - 1][n - 1], ''.join(reversed(out))]

def min_path_memo(grid):
    m, n = len(grid), len(grid[0])
    @lru_cache(maxsize=None)
    def f(i, j):
        if i == m - 1 and j == n - 1:
            return grid[i][j]
        best = INF
        if i + 1 < m: best = min(best, f(i + 1, j))
        if j + 1 < n: best = min(best, f(i, j + 1))
        return grid[i][j] + best
    return f(0, 0)

def brute(grid):
    """Every path (m, n <= 5): all choices of which of the m+n-2 moves are D; min of (sum, string)."""
    m, n = len(grid), len(grid[0]); best = None
    for ds in itertools.combinations(range(m + n - 2), m - 1):
        mv = ['R'] * (m + n - 2)
        for d in ds: mv[d] = 'D'
        i = j = 0; tot = grid[0][0]
        for c in mv:
            if c == 'D': i += 1
            else: j += 1
            tot += grid[i][j]
        cand = (tot, ''.join(mv))
        if best is None or cand < best: best = cand
    return list(best)

for g, want in [([[1, 3, 1], [1, 5, 1], [4, 2, 1]], [7, 'RRDD']), ([[1, 1], [1, 1]], [3, 'DR']), ([[5]], [5, '']), ([[0, 0, 0], [0, 0, 0]], [0, 'DRR'])]:
    assert min_path(g) == brute(g) == want, g
    assert min_sum_one_row(g) == want[0] == min_path_memo(g)
print('4 prompt examples ok')

g = [[1, 3, 1], [1, 5, 1], [4, 2, 1]]
print('suffix table f (cost from the cell to the end) for', g)
for row in suffix_table(g)[:-1]:
    print(' ', row[:-1])
print('walk ->', min_path(g))

for _ in range(1000):
    m, n = random.randint(1, 5), random.randint(1, 5)
    grid = [[random.randint(0, 3) for _ in range(n)] for _ in range(m)]
    assert min_path(grid) == brute(grid), grid
    assert min_sum_one_row(grid) == min_path_memo(grid) == brute(grid)[0]
print('1000 seeded random grids (m, n <= 5, values 0..3): table walk == enumeration of (sum, string); one row and memo give the same sum')

# exhaustive: every 2 x 3 grid with values 0..2 (729) and every 3 x 3 grid with values 0..1 (512)
cnt = 0
for m, n, vmax in ((2, 3, 3), (3, 3, 2)):
    for cells in itertools.product(range(vmax), repeat=m * n):
        grid = [list(cells[r * n:(r + 1) * n]) for r in range(m)]
        assert min_path(grid) == brute(grid); cnt += 1
print('exhaustive 2x3 (values 0..2) and 3x3 (values 0..1) grids:', cnt, 'ok')

# claim: parent pointers from the end do not give the D < R smallest string automatically
diff = 0
for _ in range(500):
    m, n = random.randint(2, 5), random.randint(2, 5)
    grid = [[random.randint(0, 2) for _ in range(n)] for _ in range(m)]
    a, b = prefix_parent_walk(grid), min_path(grid)
    assert a[0] == b[0]
    diff += a[1] != b[1]
print('prefix-table parent walk (tie: arrived by D) returns a different path than the suffix tie rule on', diff, 'of 500 random grids')
assert diff > 0
print('example [[1,1],[1,1]]: parent walk', prefix_parent_walk([[1, 1], [1, 1]]), 'vs suffix walk', min_path([[1, 1], [1, 1]]))

# greedy "step to the cheaper neighbour" is not the DP
def greedy(grid):
    m, n = len(grid), len(grid[0]); i = j = 0; tot = grid[0][0]
    while (i, j) != (m - 1, n - 1):
        if i == m - 1: j += 1
        elif j == n - 1: i += 1
        elif grid[i + 1][j] <= grid[i][j + 1]: i += 1
        else: j += 1
        tot += grid[i][j]
    return tot
bad = 0
for _ in range(500):
    grid = [[random.randint(0, 9) for _ in range(4)] for _ in range(4)]
    bad += greedy(grid) != min_path(grid)[0]
print('greedy cheaper-neighbour sum is wrong on', bad, 'of 500 random 4x4 grids')

# max size and recursion
print('recursion limit:', sys.getrecursionlimit())
big = [[random.randint(0, 100) for _ in range(200)] for _ in range(200)]
t = time.perf_counter(); r = min_path(big); dt = time.perf_counter() - t
assert r[0] == min_sum_one_row(big) == min_path_memo(big) and len(r[1]) == 398 and r[1].count('D') == 199
print('200 x 200: best', r[0], 'path length', len(r[1]), '| memo (depth 399) agrees | sandbox time under 2 s:', dt < 2)
huge = [[1] * 600 for _ in range(600)]
print('bottom-up 600 x 600 all ones ->', min_path(huge)[0], end=' | memo 600 x 600: ')
try:
    min_path_memo(huge); print('ok')
except RecursionError:
    print('RecursionError (depth 1199)')

assert min_path([[7]]) == [7, ''] and min_path([[1, 2, 3]]) == [6, 'RR'] and min_path([[1], [2], [3]]) == [6, 'DD']
print('edge asserts ok')
```

**Output (my run):**
```
4 prompt examples ok
suffix table f (cost from the cell to the end) for [[1, 3, 1], [1, 5, 1], [4, 2, 1]]
  [7, 6, 3]
  [8, 7, 2]
  [7, 3, 1]
walk -> [7, 'RRDD']
1000 seeded random grids (m, n <= 5, values 0..3): table walk == enumeration of (sum, string); one row and memo give the same sum
exhaustive 2x3 (values 0..2) and 3x3 (values 0..1) grids: 1241 ok
prefix-table parent walk (tie: arrived by D) returns a different path than the suffix tie rule on 264 of 500 random grids
example [[1,1],[1,1]]: parent walk [3, 'RD'] vs suffix walk [3, 'DR']
greedy cheaper-neighbour sum is wrong on 184 of 500 random 4x4 grids
recursion limit: 1000
200 x 200: best 10070 path length 398 | memo (depth 399) agrees | sandbox time under 2 s: True
bottom-up 600 x 600 all ones -> 1199 | memo 600 x 600: RecursionError (depth 1199)
edge asserts ok
```

**Edge cases:**
- 1 x 1 returns `[value, '']`.
- One row or one column has exactly one path (`'RR'`, `'DD'`).
- All zeros returns `'D'` repeated, then `'R'` repeated (`'DRR'` for 2 x 3): D first as long as it is optimal.
- Zeros and large values mixed: ties are common with 0..3 values, which is why the random tests use a tiny range.

**Follow-ups:**
- Count how many minimum paths exist? A second table with the same shape (add the counts of the cells that achieve the minimum), with the modulus rule of that prompt.
- Largest sum instead of smallest? Swap `min` for `max` (same table, same walk rule).
- Allow diagonal moves? Add `f[i+1][j+1]` to the `min`, and a third letter to the tie rule.

**Common mistakes:**
- Using a prefix table and walking back with a tie rule, expecting the smallest string.
- Walking with `<` instead of `<=` (then ties go to R, giving `RD` on `[[1,1],[1,1]]`).
- Forgetting the infinity border and reading out of range on the last row or column.
- Adding `grid[i][j]` twice, or leaving out the end cell in the base case.

### Q15 ⭐⭐ 🟡 Edit distance with the edit script. `a` and `b` are lowercase strings with 0 <= len <= 300 each. Return `[distance, script]` where `script` is a string over the letters D (delete the next letter of `a`), I (insert the next letter of `b`), M (match: the next letters are equal and both advance) and S (substitute: the next letters differ, both advance); D, I and S cost 1, M costs 0, and the script consumes all of `a` and all of `b`. Many optimal scripts can exist, so the tie rule is fixed: return the lexicographically smallest script among the optimal ones (alphabet order D < I < M < S). Fill the table on suffixes and walk forward trying D, I, M, S in that order. Show that applying the script to `a` gives `b`. In the answer include a table walk-through on the first example and a seeded random cross-check of your solution against enumerating every valid script by plain recursion (len <= 5) and taking the smallest (cost, script) pair on small inputs. Example: a='horse', b='ros' -> [3, 'SMDMD']; a='ab', b='ba' -> [2, 'DMI']; a='', b='ab' -> [2, 'II']; a='abc', b='abc' -> [0, 'MMM']; a='kitten', b='sitting' -> [3, 'SMMMSMI'].
**Asked at:** 2D DP pattern guides and lists (techinterview.org two-dimensional DP interview patterns, a LeetCode Discuss '13 DP patterns' post, codemia 2D DP and DP on strings and intervals; search snippets only, not opened) | Standard-problem lists known to the editor (not found as an opened page; indicative only, no company attribution)

**Pattern:** Two-string DP (edit distance) on SUFFIXES, then a forward walk that tries the operations in the tie-rule order D, I, M, S.

**Say this first (1 line):** "f[i][j] is the edit distance between a[i:] and b[j:]: delete costs 1 + f[i+1][j], insert costs 1 + f[i][j+1], and a diagonal step costs f[i+1][j+1] plus 1 if the letters differ; I fill it bottom-up and walk forward trying D, I, M, S in that order, which is exactly the smallest optimal script."

**Brute force:** Plain recursion over `(i, j)`: at each point try D, I, and the diagonal (M when the letters are equal, S otherwise), collect every complete script with its cost, and take the smallest `(cost, script)` pair. Exponential (about 3^(m+n) leaves), so only for len <= 5. It is the checker and applies the same tie rule.

**Optimal:**
- State: `f[i][j]` = minimum cost to turn `a[i:]` into `b[j:]`.
- Transition (`i < n` and `j < m`): `f[i][j] = min(1 + f[i+1][j] (D), 1 + f[i][j+1] (I), f[i+1][j+1] + (a[i] != b[j]) (M if equal, S if not))`.
- Base cases: `f[n][j] = m - j` (only inserts remain), `f[i][m] = n - i` (only deletes remain), `f[n][m] = 0`.
- Walk from `(0, 0)` until both strings are consumed. At each cell check in order:
  1. `D` if `i < n` and `f[i][j] == 1 + f[i+1][j]`.
  2. `I` if `j < m` and `f[i][j] == 1 + f[i][j+1]`.
  3. `M` if both letters exist, are equal and `f[i][j] == f[i+1][j+1]` (when letters are equal this always holds if D and I did not apply; the code asserts it).
  4. otherwise `S` (letters differ and `f[i][j] == 1 + f[i+1][j+1]`).
- Why lexicographically smallest: the table tells which first operations keep the total optimal; trying them in alphabet order D < I < M < S and committing to the first that works makes every character as small as possible from the front.
- Replaying the script: `D` skips the next letter of `a`, `I` copies the next letter of `b`, `M` and `S` consume one letter of each and write the letter of `b`. After the whole script you have consumed all of `a` and all of `b`, and the output equals `b`. The number of non-M letters equals the distance because D, I, S cost 1 and M costs 0.
- Space: the value alone needs two rows (`prev` = row i+1, `cur` = row i). The script needs the full table (or Hirschberg's linear-space method, not required here).
- Recursion: the top-down version nests up to `m + n` frames. As observed on Python 3.13 with the default limit 1000: two 300-letter strings run (depth at most 600); two disjoint 600-letter strings (depth 1200) raise `RecursionError`. The prompt's maximum is 300 each, but I still use bottom-up. Observation, not a rule.

**Complexity:** Time O(mn), space O(mn) for the script, O(min(m, n)) for the distance alone. Walk O(m + n). Brute force exponential.

**Dry run:** `a = 'horse'`, `b = 'ros'`. Rows are suffixes of `a`, columns suffixes of `b`.

| | j=0 `ros` | j=1 `os` | j=2 `s` | j=3 `` |
|---|---|---|---|---|
| i=0 `horse` | 3 | 3 | 4 | 5 |
| i=1 `orse` | 3 | 2 | 3 | 4 |
| i=2 `rse` | 2 | 2 | 2 | 3 |
| i=3 `se` | 3 | 2 | 1 | 2 |
| i=4 `e` | 3 | 2 | 1 | 1 |
| i=5 `` | 3 | 2 | 1 | 0 |

Walk. `(0,0)` f=3: D gives `1 + f[1][0] = 4` no; I gives `1 + f[0][1] = 4` no; `h != r`, so S (`1 + f[1][1] = 3`). `(1,1)` f=2: D `1 + f[2][1] = 3` no; I `1 + f[1][2] = 4` no; `o == o` and `f[2][2] = 2`, so M. `(2,2)` f=2 (`rse` vs `s`): D `1 + f[3][2] = 2` yes, D. `(3,2)` f=1 (`se` vs `s`): D `1 + f[4][2] = 2` no; I `1 + f[3][3] = 3` no; `s == s`, `f[4][3] = 1`, M. `(4,3)` f=1: only `e` left in `a`, D. Script `SMDMD`, distance 3. Replay on `horse`: S writes `r`, M writes `o`, D skips `r`, M writes `s`, D skips `e`: `ros`.

**Code:**
```python
import itertools
import random
import sys
import time
from functools import lru_cache

random.seed(1515)

def suffix_table(a, b):
    """f[i][j] = edit distance between a[i:] and b[j:]. Base: f[n][j] = m - j (insert the rest), f[i][m] = n - i (delete the rest)."""
    n, m = len(a), len(b)
    f = [[0] * (m + 1) for _ in range(n + 1)]
    for i in range(n, -1, -1):
        for j in range(m, -1, -1):
            if i == n:
                f[i][j] = m - j
            elif j == m:
                f[i][j] = n - i
            else:
                f[i][j] = min(1 + f[i + 1][j],                              # D: delete a[i]
                              1 + f[i][j + 1],                              # I: insert b[j]
                              f[i + 1][j + 1] + (a[i] != b[j]))             # M (free) or S (cost 1)
    return f

def edit_script(a, b):
    """[distance, script], lexicographically smallest optimal script with D < I < M < S."""
    n, m = len(a), len(b)
    f = suffix_table(a, b)
    i = j = 0
    out = []
    while i < n or j < m:
        if i < n and f[i][j] == 1 + f[i + 1][j]:
            out.append('D'); i += 1
        elif j < m and f[i][j] == 1 + f[i][j + 1]:
            out.append('I'); j += 1
        elif i < n and j < m and a[i] == b[j] and f[i][j] == f[i + 1][j + 1]:
            out.append('M'); i += 1; j += 1
        else:
            assert i < n and j < m and a[i] != b[j] and f[i][j] == 1 + f[i + 1][j + 1]
            out.append('S'); i += 1; j += 1
    return [f[0][0], ''.join(out)]

def distance_two_rows(a, b):
    """Value only, O(min) space: prev = row i+1, cur = row i."""
    n, m = len(a), len(b)
    prev = [m - j for j in range(m + 1)]                    # row i = n
    for i in range(n - 1, -1, -1):
        cur = [0] * (m + 1)
        cur[m] = n - i
        for j in range(m - 1, -1, -1):
            cur[j] = min(1 + prev[j], 1 + cur[j + 1], prev[j + 1] + (a[i] != b[j]))
        prev = cur
    return prev[0]

def distance_memo(a, b):
    @lru_cache(maxsize=None)
    def f(i, j):
        if i == len(a): return len(b) - j
        if j == len(b): return len(a) - i
        return min(1 + f(i + 1, j), 1 + f(i, j + 1), f(i + 1, j + 1) + (a[i] != b[j]))
    return f(0, 0)

def apply_script(a, b, script):
    """Replay the script on a; asserts every M is a real match, every S a real difference, and everything is consumed."""
    i = j = 0; out = []
    for c in script:
        if c == 'D': i += 1
        elif c == 'I': out.append(b[j]); j += 1
        elif c == 'M': assert a[i] == b[j]; out.append(a[i]); i += 1; j += 1
        else: assert a[i] != b[j]; out.append(b[j]); i += 1; j += 1
    assert i == len(a) and j == len(b)
    return ''.join(out)

def brute(a, b):
    """Every valid script by plain recursion (len <= 5); smallest (cost, script)."""
    res = []
    def go(i, j, s, cost):
        if i == len(a) and j == len(b): res.append((cost, s)); return
        if i < len(a): go(i + 1, j, s + 'D', cost + 1)
        if j < len(b): go(i, j + 1, s + 'I', cost + 1)
        if i < len(a) and j < len(b):
            go(i + 1, j + 1, s + ('M' if a[i] == b[j] else 'S'), cost + (a[i] != b[j]))
    go(0, 0, '', 0)
    return list(min(res))

for a, b, want in [('horse', 'ros', [3, 'SMDMD']), ('ab', 'ba', [2, 'DMI']), ('', 'ab', [2, 'II']), ('abc', 'abc', [0, 'MMM']), ('kitten', 'sitting', [3, 'SMMMSMI'])]:
    r = edit_script(a, b)
    assert r == brute(a, b) == want and distance_two_rows(a, b) == distance_memo(a, b) == want[0], (a, b)
    assert apply_script(a, b, r[1]) == b
print('5 prompt examples ok')

f = suffix_table('horse', 'ros')
print("f (distance of a[i:], b[j:]) for a='horse' (rows), b='ros' (cols j=0..3):")
for i, row in enumerate(f):
    print(' ', ('horse-')[i], row)
print('script ->', edit_script('horse', 'ros'))

for _ in range(500):
    a = ''.join(random.choice('abc') for _ in range(random.randint(0, 5)))
    b = ''.join(random.choice('abc') for _ in range(random.randint(0, 5)))
    r = edit_script(a, b)
    assert r == brute(a, b), (a, b)
    assert distance_two_rows(a, b) == distance_memo(a, b) == r[0]
    assert apply_script(a, b, r[1]) == b and sum(c != 'M' for c in r[1]) == r[0]
print('500 seeded random pairs (len 0..5, alphabet abc): script == enumeration, two-row == memo, script turns a into b, non-M count == distance')

cnt = 0
words = [''.join(w) for n in range(5) for w in itertools.product('ab', repeat=n)]
for a in words:
    for b in words:
        r = edit_script(a, b)
        assert r == brute(a, b) and apply_script(a, b, r[1]) == b and sum(c != 'M' for c in r[1]) == r[0]; cnt += 1
print('exhaustive pairs over {a,b}, len <= 4:', cnt, 'ok (script == smallest optimal, replay gives b, non-M letters == distance)')

# recursion and size
print('recursion limit:', sys.getrecursionlimit())
x = ''.join(random.choice('abcd') for _ in range(300)); y = ''.join(random.choice('abcd') for _ in range(300))
t = time.perf_counter(); r = edit_script(x, y); dt = time.perf_counter() - t
assert r[0] == distance_two_rows(x, y) and apply_script(x, y, r[1]) == y
print('bottom-up 300 x 300: distance', r[0], 'script length', len(r[1]), '| memo 300 x 300 agrees:', distance_memo(x, y) == r[0])
try:
    distance_memo('a' * 600, 'b' * 600); print('memo 600 + 600 disjoint: ok')
except RecursionError:
    print('memo 600 + 600 disjoint: RecursionError')
assert edit_script('', '') == [0, ''] and edit_script('abc', '') == [3, 'DDD'] and edit_script('a', 'b') == [1, 'S']
print('edge asserts ok')
```

**Output (my run):**
```
5 prompt examples ok
f (distance of a[i:], b[j:]) for a='horse' (rows), b='ros' (cols j=0..3):
  h [3, 3, 4, 5]
  o [3, 2, 3, 4]
  r [2, 2, 2, 3]
  s [3, 2, 1, 2]
  e [3, 2, 1, 1]
  - [3, 2, 1, 0]
script -> [3, 'SMDMD']
500 seeded random pairs (len 0..5, alphabet abc): script == enumeration, two-row == memo, script turns a into b, non-M count == distance
exhaustive pairs over {a,b}, len <= 4: 961 ok (script == smallest optimal, replay gives b, non-M letters == distance)
recursion limit: 1000
bottom-up 300 x 300: distance 157 script length 343 | memo 300 x 300 agrees: True
memo 600 + 600 disjoint: RecursionError
edge asserts ok
```

**Edge cases:**
- `a = ''`, `b = 'ab'` returns `[2, 'II']`; `a = 'abc'`, `b = ''` returns `[3, 'DDD']`; both empty returns `[0, '']`.
- Equal strings return all `M`.
- `'ab'` to `'ba'`: distance 2 (no swap operation), script `DMI` (delete `a`, match `b`, insert `a`).
- Several optimal scripts exist for most inputs; the tie rule picks one (for `'ab'`, `'ba'` the alternative `SS` also costs 2 but sorts after `DMI`).

**Follow-ups:**
- Allow a transposition (Damerau)? Add a fourth transition when `a[i] == b[j+1]` and `a[i+1] == b[j]`.
- Different costs for D, I, S? Put the weights into the transitions; the walk compares against the weighted values.
- Linear space with the script? Hirschberg: forward and backward distance rows around the middle row of `a`, recurse.

**Common mistakes:**
- Treating a mismatch diagonal as free, or an equal-letter diagonal as cost 1.
- Wrong bases (`f[0][j] = j` is the PREFIX version; for suffixes it is `m - j`).
- Trying M before D and I in the walk, so the script is optimal but not the smallest.
- Replaying with `S` when the letters are equal (the script must use `M` there, which costs 0).

### Q16 ⭐⭐ 🟡 Shortest common supersequence. `a` and `b` are lowercase strings with 0 <= len <= 500 each. Return a shortest string that has both `a` and `b` as subsequences. Several shortest strings can exist, so the tie rule is fixed: return the lexicographically smallest of the shortest. State the length as len(a) + len(b) - LCS(a, b) and why, build the table on suffixes (`f[i][j]` = SCS length of a[i:] and b[j:]) and walk forward: equal heads are emitted once, otherwise emit the smaller head letter among the moves that keep the total optimal. In the answer include a table walk-through on the first example and a seeded random cross-check of your solution against enumerating every string of the right length in alphabetical order (len <= 4, alphabet a-c) on small inputs. Example: a='abac', b='cab' -> 'cabac'; a='abc', b='abc' -> 'abc'; a='', b='xy' -> 'xy'; a='ab', b='ba' -> 'aba'.
**Asked at:** 2D DP pattern guides and lists (techinterview.org two-dimensional DP interview patterns, a LeetCode Discuss '13 DP patterns' post, codemia 2D DP and DP on strings and intervals; search snippets only, not opened) | Standard-problem lists known to the editor (not found as an opened page; indicative only, no company attribution)

**Pattern:** LCS in disguise. The supersequence shares every common letter once and pays for the rest. The table is on suffixes so the walk can fix the smallest letter first.

**Say this first (1 line):** "g[i][j] is the shortest common supersequence length of a[i:] and b[j:]: equal heads cost one letter, otherwise 1 + min(skip a's head, skip b's head); the length is m + n - LCS, and I rebuild the string forward, emitting equal heads once and otherwise the smaller head among the moves that keep the total optimal."

**Brute force:** Compute the target length `L`, then try every string of length L over the letters of `a` and `b` in alphabetical order; the first one that contains both inputs as subsequences is the answer. Exponential, so only len <= 4 over a-c (the check also verifies the length against a pure search that does not use the LCS formula).

**Optimal:**
- State: `g[i][j]` = length of a shortest common supersequence of `a[i:]` and `b[j:]`.
- Transition: if `a[i] == b[j]` then `g[i][j] = 1 + g[i+1][j+1]`; else `g[i][j] = 1 + min(g[i+1][j], g[i][j+1])` (emit `a[i]` and move in `a`, or emit `b[j]` and move in `b`).
- Base cases: `g[n][j] = m - j`, `g[i][m] = n - i` (emit what remains of the other string).
- Length identity: `g[0][0] = m + n - LCS(a, b)`. Each letter of an LCS is emitted once for two inputs, so we save one letter per common letter and no more can be saved.
- Walk from `(0, 0)` while both strings have letters left:
  - equal heads: emit the letter once, move both;
  - different heads: collect the moves that keep the total (`g[i][j] == 1 + g[i+1][j]` means emit `a[i]`; `g[i][j] == 1 + g[i][j+1]` means emit `b[j]`) and take the one with the smaller letter (the two letters differ, so there is no tie);
  - when one string is exhausted, append the rest of the other.
- Why lexicographically smallest: the first emitted letter is the most significant, and the table says exactly which letters can come first in some shortest answer; take the smallest at every step. Equal heads: emitting the shared letter once is optimal, and the string starts with that letter either way. The exhaustive check below confirms it against the alphabetical enumeration for all 961 pairs over {a, b} up to length 4.
- Space: length alone needs two rows (as in LCS); the string needs the table (or Hirschberg).
- Recursion: top-down nests up to `m + n` frames. As observed on Python 3.13 with the default limit 1000: two random 300-letter strings run; two disjoint 500-letter strings (depth up to 1000) raise `RecursionError`. The prompt allows 500 each, so use the loops.

**Complexity:** Time O(mn), space O(mn) for the string (O(min(m, n)) for the length only). Walk O(m + n). Brute force O(k^L * L), exponential.

**Dry run:** `a = 'abac'`, `b = 'cab'`.

| | j=0 `cab` | j=1 `ab` | j=2 `b` | j=3 `` |
|---|---|---|---|---|
| i=0 `abac` | 5 | 4 | 4 | 4 |
| i=1 `bac` | 5 | 4 | 3 | 3 |
| i=2 `ac` | 4 | 3 | 3 | 2 |
| i=3 `c` | 3 | 3 | 2 | 1 |
| i=4 `` | 3 | 2 | 1 | 0 |

Length 5 = 4 + 3 - 2 (LCS `ab`). Walk: `(0,0)`: heads `a` and `c` differ. Emit `a` would need `1 + g[1][0] = 6`, not 5, so it is not allowed; emit `c` needs `1 + g[0][1] = 5`, allowed. Emit `c`, go to `(0,1)`. Heads `a` and `a` are equal: emit `a`, go to `(1,2)`. Heads `b` and `b`: emit `b`, go to `(2,3)`. `b` is exhausted: append `a[2:] = 'ac'`. Result `cabac`.

**Code:**
```python
import itertools
import random
import sys
from functools import lru_cache

random.seed(1616)

def suffix_table(a, b):
    """g[i][j] = length of a shortest common supersequence of a[i:] and b[j:]."""
    n, m = len(a), len(b)
    g = [[0] * (m + 1) for _ in range(n + 1)]
    for i in range(n, -1, -1):
        for j in range(m, -1, -1):
            if i == n:
                g[i][j] = m - j                       # only b's rest is left: emit it
            elif j == m:
                g[i][j] = n - i
            elif a[i] == b[j]:
                g[i][j] = 1 + g[i + 1][j + 1]         # equal heads: emit once
            else:
                g[i][j] = 1 + min(g[i + 1][j], g[i][j + 1])
    return g

def scs(a, b):
    """Lexicographically smallest shortest common supersequence."""
    n, m = len(a), len(b)
    g = suffix_table(a, b)
    i = j = 0
    out = []
    while i < n and j < m:
        if a[i] == b[j]:
            out.append(a[i]); i += 1; j += 1
        else:
            options = []                              # (letter, move) for the moves that keep the total optimal
            if g[i][j] == 1 + g[i + 1][j]: options.append((a[i], 'a'))
            if g[i][j] == 1 + g[i][j + 1]: options.append((b[j], 'b'))
            letter, move = min(options)               # letters differ, so no tie inside min
            out.append(letter)
            if move == 'a': i += 1
            else: j += 1
    out.append(a[i:]); out.append(b[j:])              # at most one of these is non-empty
    return ''.join(out)

def lcs_length(a, b):
    prev = [0] * (len(b) + 1)
    for ch in a:
        cur = [0] * (len(b) + 1)
        for j in range(1, len(b) + 1):
            cur[j] = prev[j - 1] + 1 if ch == b[j - 1] else max(prev[j], cur[j - 1])
        prev = cur
    return prev[-1]

def scs_length_memo(a, b):
    @lru_cache(maxsize=None)
    def f(i, j):
        if i == len(a): return len(b) - j
        if j == len(b): return len(a) - i
        if a[i] == b[j]: return 1 + f(i + 1, j + 1)
        return 1 + min(f(i + 1, j), f(i, j + 1))
    return f(0, 0)

def is_subseq(t, s):
    it = iter(s)
    return all(ch in it for ch in t)

def brute(a, b):
    """Every string of the right length in alphabetical order; the first that contains both is the answer."""
    L = len(a) + len(b) - lcs_length(a, b)
    alpha = sorted(set(a) | set(b))
    for t in itertools.product(alpha, repeat=L):
        t = ''.join(t)
        if is_subseq(a, t) and is_subseq(b, t):
            return t
    return None

def brute_length(a, b):
    """Independent length check (does not use the LCS formula): shortest L for which some string works."""
    alpha = sorted(set(a) | set(b))
    for L in range(max(len(a), len(b)), len(a) + len(b) + 1):
        for t in itertools.product(alpha, repeat=L):
            t = ''.join(t)
            if is_subseq(a, t) and is_subseq(b, t):
                return L

for a, b, want in [('abac', 'cab', 'cabac'), ('abc', 'abc', 'abc'), ('', 'xy', 'xy'), ('ab', 'ba', 'aba')]:
    assert scs(a, b) == brute(a, b) == want, (a, b)
print('4 prompt examples ok')

g = suffix_table('abac', 'cab')
print("g (SCS length of a[i:], b[j:]) for a='abac' (rows), b='cab' (cols j=0..3):")
for i, row in enumerate(g):
    print(' ', 'abac-'[i], row)
print('walk ->', scs('abac', 'cab'))

for _ in range(500):
    a = ''.join(random.choice('abc') for _ in range(random.randint(0, 4)))
    b = ''.join(random.choice('abc') for _ in range(random.randint(0, 4)))
    r = scs(a, b)
    assert r == brute(a, b), (a, b)
    assert len(r) == len(a) + len(b) - lcs_length(a, b) == suffix_table(a, b)[0][0] == scs_length_memo(a, b)
    assert is_subseq(a, r) and is_subseq(b, r)
print('500 seeded random pairs (len 0..4, alphabet abc): walk == alphabetical enumeration; length == m + n - LCS == memo; both inputs are subsequences')

cnt = 0
words = [''.join(w) for n in range(5) for w in itertools.product('ab', repeat=n)]
for a in words:
    for b in words:
        r = scs(a, b)
        assert r == brute(a, b) and len(r) == brute_length(a, b); cnt += 1
print('exhaustive pairs over {a,b}, len <= 4:', cnt, 'ok (also the length equals the shortest length found by search, not by the LCS formula)')

print('recursion limit:', sys.getrecursionlimit())
x = ''.join(random.choice('abcd') for _ in range(500)); y = ''.join(random.choice('abcd') for _ in range(500))
r = scs(x, y)
assert len(r) == 1000 - lcs_length(x, y) and is_subseq(x, r) and is_subseq(y, r)
print('bottom-up 500 + 500 random: length', len(r), '(= 1000 - LCS)')
print('memoised length, two random 300-letter strings:', scs_length_memo(x[:300], y[:300]))
try:
    scs_length_memo('a' * 500, 'b' * 500); print('memoised disjoint 500 + 500: ok')
except RecursionError:
    print('memoised disjoint 500 + 500: RecursionError (depth up to 1000)')
print('disjoint 500 + 500 bottom-up length:', len(scs('a' * 500, 'b' * 500)))

assert scs('', '') == '' and scs('abc', '') == 'abc' and scs('a', 'a') == 'a' and scs('b', 'a') == 'ab'
print('edge asserts ok')
```

**Output (my run):**
```
4 prompt examples ok
g (SCS length of a[i:], b[j:]) for a='abac' (rows), b='cab' (cols j=0..3):
  a [5, 4, 4, 4]
  b [5, 4, 3, 3]
  a [4, 3, 3, 2]
  c [3, 3, 2, 1]
  - [3, 2, 1, 0]
walk -> cabac
500 seeded random pairs (len 0..4, alphabet abc): walk == alphabetical enumeration; length == m + n - LCS == memo; both inputs are subsequences
exhaustive pairs over {a,b}, len <= 4: 961 ok (also the length equals the shortest length found by search, not by the LCS formula)
recursion limit: 1000
bottom-up 500 + 500 random: length 677 (= 1000 - LCS)
memoised length, two random 300-letter strings: 408
memoised disjoint 500 + 500: RecursionError (depth up to 1000)
disjoint 500 + 500 bottom-up length: 1000
edge asserts ok
```

**Edge cases:**
- One or both empty: the other string (or `''`).
- Equal strings return the string; `a` a subsequence of `b` returns `b`.
- `'ab'` and `'ba'` give `'aba'` (length 3 = 2 + 2 - 1), not `'abba'`.
- Disjoint alphabets: the answer has length m + n and the smaller letters come first where allowed.

**Follow-ups:**
- Why is the answer length m + n - LCS? Every common letter that is shared saves one; the best sharing is an LCS.
- Count the shortest supersequences? Counting DP with care for duplicates; ask for the distinct strings or the ways.
- Minimum insertions to make a string a palindrome? `n - LPS(s)` (LPS is the LCS of `s` and its reverse).

**Common mistakes:**
- Emitting the equal letter twice.
- Picking "the first option that works" without comparing the letters (gives a shortest, not the smallest).
- Building the answer from the end of a prefix table (the tie rule is on the front of the string).
- Forgetting to append the leftover tail once one string runs out.

### Q17 ⭐⭐ 🟡 Wildcard matching as a counting DP. `s` is a lowercase string (0 <= len <= 300) and `p` a pattern (0 <= len <= 300) of lowercase letters, '?' (exactly one character) and '*' (any run of characters, possibly empty). Return `[matches, ways]` where `matches` is True when `p` matches the whole of `s` and `ways` is the number of distinct assignments of run lengths to the '*' symbols (in order, each '*' counted separately, so '**' is two stars) that make the pattern match; `ways` is exact, and `matches` equals `ways > 0`. The boolean question solved with two pointers is Part 3 Q38; here fill the 2D table and show that the boolean and counting tables have the same shape, with `or` becoming `+` (a '*' takes `f[i][j-1]` for zero characters plus `f[i-1][j]` for one more). In the answer include a table walk-through on the first example and a seeded random cross-check of your solution against enumerating every run-length assignment by plain recursion (len(s) <= 7) on small inputs. Example: s='aa', p='a' -> [False, 0]; s='aa', p='*' -> [True, 1]; s='cb', p='?a' -> [False, 0]; s='adceb', p='*a*b' -> [True, 1]; s='', p='**' -> [True, 1]; s='abc', p='a?c' -> [True, 1].
**Asked at:** 2D DP pattern guides and lists (techinterview.org two-dimensional DP interview patterns, a LeetCode Discuss '13 DP patterns' post, codemia 2D DP and DP on strings and intervals; search snippets only, not opened) | Standard-problem lists known to the editor (not found as an opened page; indicative only, no company attribution)

**Pattern:** Two-sequence DP where the pattern symbol decides the move. The boolean table becomes a counting table by turning `or` into `+`. (The two-pointer boolean matcher is Part 3 Q38.)

**Say this first (1 line):** "f[i][j] is the number of ways the first j pattern symbols match the first i letters; a letter or '?' copies f[i-1][j-1] when it fits, and a '*' adds f[i][j-1] (matches nothing) and f[i-1][j] (eats one more letter); matches is just ways > 0."

**Brute force:** Plain recursion over `(i, j)`; at a `*` try every run length `k = 0 .. len(s) - i` and recurse, which enumerates every assignment of run lengths to the stars. Exponential, only for len(s) <= 7. It returns the same `[matches, ways]` pair.

**Optimal:**
- State: `f[i][j]` = number of distinct run-length assignments to the stars among `p[:j]` such that `p[:j]` matches exactly `s[:i]`. (Each `*` is counted separately, so `**` is two stars.)
- Base: `f[0][0] = 1`. Column 0 is 0 for `i > 0` (an empty pattern matches only the empty string). Row 0 follows from the transition: `f[0][j] = f[0][j-1]` if `p[j-1]` is `*`, else 0.
- Transition for symbol `c = p[j-1]`:
  - `c == '*'`: `f[i][j] = f[i][j-1] + f[i-1][j]` (the star takes zero letters; or it takes one more letter, and `f[i-1][j]` already counts the star having taken the others). For `i = 0` only the first term exists.
  - `c == '?'` or `c == s[i-1]`: `f[i][j] = f[i-1][j-1]`.
  - otherwise `0`.
- Boolean vs counting: the boolean table has `f[i][j] = f[i][j-1] or f[i-1][j]` for a star and `f[i-1][j-1]` for a letter. Same shape, same loops; `or` becomes `+`, `and`-with-flag becomes copy. That is why `matches == (ways > 0)`; the code checks it, and also against a regular-expression translation (`*` to `.*`, `?` to `.`).
- Counting is exact (Python integers). With `s = 'a' * n` and `k` stars the count is `C(n + k - 1, k - 1)` (stars and bars); the code checks it. For `s='ab'`, `p='**'` the answer is `[True, 3]`; the prompt's `s=''`, `p='**'` gives one way (both stars take 0).
- Space: row `i` reads row `i-1` only, so two rows (or one row plus one saved diagonal) suffice, O(n).
- Recursion: top-down `go(i, j)` consumes one symbol of `i` or `j` per call, so the depth is up to `m + n`. As observed on Python 3.13 with the default limit 1000: at the prompt's maximum 300 + 300 (depth <= 600) the memoised version runs and agrees; at 700 + 700 (outside the prompt) it raises `RecursionError`. The prompt does not require bottom-up here, but the loops are safer.

**Complexity:** Time O(mn), space O(mn) for the table, O(n) for the two rows. The counts can have many digits (89 digits in the max-size test), so each addition is not strictly O(1); say so. Brute force is exponential in the number of stars.

**Dry run:** `s = 'adceb'`, `p = '*a*b'`. Rows = letters of s used (i), columns = pattern symbols used (j).

| i \ j | 0 | 1 `*` | 2 `a` | 3 `*` | 4 `b` |
|---|---|---|---|---|---|
| 0 | 1 | 1 | 0 | 0 | 0 |
| 1 `a` | 0 | 1 | 1 | 1 | 0 |
| 2 `d` | 0 | 1 | 0 | 1 | 0 |
| 3 `c` | 0 | 1 | 0 | 1 | 0 |
| 4 `e` | 0 | 1 | 0 | 1 | 0 |
| 5 `b` | 0 | 1 | 0 | 1 | 1 |

Cells: `f[0][1]` is a star over zero letters: `f[0][0] = 1`. `f[1][1] = f[1][0] + f[0][1] = 0 + 1 = 1` (the first star eats `a`). `f[1][2]`: `a == a`, copy `f[0][1] = 1`. `f[1][3] = f[1][2] + f[0][3] = 1 + 0 = 1`. `f[2][3] = f[2][2] + f[1][3] = 0 + 1 = 1` (second star eats `d`), and likewise down the column. `f[5][4]`: `b == b`, copy `f[4][3] = 1`. Answer `f[5][4] = 1`, so `[True, 1]`.

**Code:**
```python
import itertools
import random
import re
import sys
from functools import lru_cache
from math import comb

random.seed(1717)

def wildcard_table(s, p):
    """f[i][j] = number of ways the first j pattern symbols match the first i letters of s (each '*' counted separately)."""
    m, n = len(s), len(p)
    f = [[0] * (n + 1) for _ in range(m + 1)]
    f[0][0] = 1
    for i in range(m + 1):
        for j in range(1, n + 1):
            c = p[j - 1]
            if c == '*':
                # zero characters: f[i][j-1]; one more character (absorbed by this star): f[i-1][j]
                f[i][j] = f[i][j - 1] + (f[i - 1][j] if i else 0)
            elif i and (c == '?' or c == s[i - 1]):
                f[i][j] = f[i - 1][j - 1]
    return f

def wildcard(s, p):
    f = wildcard_table(s, p)
    return [f[-1][-1] > 0, f[-1][-1]]

def wildcard_row(s, p):
    """One row over the pattern. Rows are indexed by i (letters of s used); row[j] holds f[i][j]."""
    m, n = len(s), len(p)
    row = [0] * (n + 1)
    row[0] = 1                                   # i = 0
    for j in range(1, n + 1):
        row[j] = row[j - 1] if p[j - 1] == '*' else 0
    for i in range(1, m + 1):
        new = [0] * (n + 1)
        for j in range(1, n + 1):
            c = p[j - 1]
            if c == '*':
                new[j] = new[j - 1] + row[j]     # f[i][j-1] + f[i-1][j]
            elif c == '?' or c == s[i - 1]:
                new[j] = row[j - 1]              # f[i-1][j-1]
        row = new
    return [row[n] > 0, row[n]]

def wildcard_bool(s, p):
    """Same shape, 'or' instead of '+'."""
    m, n = len(s), len(p)
    f = [[False] * (n + 1) for _ in range(m + 1)]
    f[0][0] = True
    for i in range(m + 1):
        for j in range(1, n + 1):
            c = p[j - 1]
            if c == '*':
                f[i][j] = f[i][j - 1] or (i > 0 and f[i - 1][j])
            elif i and (c == '?' or c == s[i - 1]):
                f[i][j] = f[i - 1][j - 1]
    return f[m][n]

def wildcard_memo(s, p):
    @lru_cache(maxsize=None)
    def go(i, j):                                # i letters, j pattern symbols consumed from the FRONT
        if j == len(p): return 1 if i == len(s) else 0
        if p[j] == '*': return go(i, j + 1) + (go(i + 1, j) if i < len(s) else 0)
        return go(i + 1, j + 1) if i < len(s) and p[j] in ('?', s[i]) else 0
    return go(0, 0)

def brute(s, p):
    """Enumerate every run-length assignment to the stars (plain recursion)."""
    def go(i, j):
        if j == len(p): return 1 if i == len(s) else 0
        if p[j] == '*': return sum(go(i + k, j + 1) for k in range(len(s) - i + 1))
        return go(i + 1, j + 1) if i < len(s) and p[j] in ('?', s[i]) else 0
    c = go(0, 0)
    return [c > 0, c]

def as_regex(p):
    return ''.join('.*' if c == '*' else '.' if c == '?' else c for c in p)

for s, p, want in [('aa', 'a', [False, 0]), ('aa', '*', [True, 1]), ('cb', '?a', [False, 0]), ('adceb', '*a*b', [True, 1]), ('', '**', [True, 1]), ('abc', 'a?c', [True, 1])]:
    assert wildcard(s, p) == wildcard_row(s, p) == brute(s, p) == want, (s, p)
    assert wildcard_bool(s, p) == want[0]
print('6 prompt examples ok')

f = wildcard_table('adceb', '*a*b')
print("f for s='adceb' (rows i=0..5 letters used), p='*a*b' (cols j=0..4 symbols used):")
print('      ', ' '.join('-*a*b'))
for i, row in enumerate(f):
    print('  ', '-adceb'[i], row)

pos = 0
for _ in range(1500):
    s = ''.join(random.choice('ab') for _ in range(random.randint(0, 7)))
    p = ''.join(random.choice('ab?**') for _ in range(random.randint(0, 6)))
    r = wildcard(s, p)
    assert r == brute(s, p) == wildcard_row(s, p) == [wildcard_memo(s, p) > 0, wildcard_memo(s, p)], (s, p)
    assert r[0] == wildcard_bool(s, p) == (r[1] > 0) == (re.fullmatch(as_regex(p), s, re.S) is not None)
    pos += r[0]
print('1500 seeded random (s, p): table == plain recursion == one row == memo; boolean table == (ways > 0) == regex translation; True in', pos, 'of 1500')
assert 0 < pos < 1500

# closed form: s = a^n against k stars has C(n + k - 1, k - 1) assignments
for n_ in range(0, 9):
    for k in range(1, 6):
        assert wildcard('a' * n_, '*' * k)[1] == comb(n_ + k - 1, k - 1)
print('closed form checked: ways(a^n, k stars) == C(n + k - 1, k - 1) for n 0..8, k 1..5')
print("'**' on 'ab' gives", wildcard('ab', '**'), '(three splits: 0|2, 1|1, 2|0)')

print('recursion limit:', sys.getrecursionlimit())
s = 'a' * 300; p = '*a' * 150
r = wildcard(s, p)
print('max size 300 vs 300 symbols (150 stars): ways =', r[1] if r[1] < 10**12 else str(r[1])[:12] + '... (%d digits)' % len(str(r[1])), '| one row agrees:', wildcard_row(s, p) == r)
print('memoised version at 300 + 300 (depth <= 600):', 'agrees' if wildcard_memo(s, p) == r[1] else 'DIFFERS')
rs = ''.join(random.choice('ab') for _ in range(300)); rp = ''.join(random.choice('ab?*') for _ in range(300))
assert wildcard(rs, rp) == wildcard_row(rs, rp)
try:
    wildcard_memo('a' * 700, '*' * 700); print('memoised 700 + 700: ok')
except RecursionError:
    print('memoised 700 + 700 (outside the prompt sizes): RecursionError')

assert wildcard('', '') == [True, 1] and wildcard('a', '') == [False, 0] and wildcard('', 'a') == [False, 0] and wildcard('', '?') == [False, 0]
print('edge asserts ok')
```

**Output (my run):**
```
6 prompt examples ok
f for s='adceb' (rows i=0..5 letters used), p='*a*b' (cols j=0..4 symbols used):
       - * a * b
   - [1, 1, 0, 0, 0]
   a [0, 1, 1, 1, 0]
   d [0, 1, 0, 1, 0]
   c [0, 1, 0, 1, 0]
   e [0, 1, 0, 1, 0]
   b [0, 1, 0, 1, 1]
1500 seeded random (s, p): table == plain recursion == one row == memo; boolean table == (ways > 0) == regex translation; True in 489 of 1500
closed form checked: ways(a^n, k stars) == C(n + k - 1, k - 1) for n 0..8, k 1..5
'**' on 'ab' gives [True, 3] (three splits: 0|2, 1|1, 2|0)
recursion limit: 1000
max size 300 vs 300 symbols (150 stars): ways = 468798513864... (89 digits) | one row agrees: True
memoised version at 300 + 300 (depth <= 600): agrees
memoised 700 + 700 (outside the prompt sizes): RecursionError
edge asserts ok
```

**Edge cases:**
- `s = ''`, `p = ''` returns `[True, 1]`; `s='a'`, `p=''` returns `[False, 0]`; `s=''`, `p='?'` returns `[False, 0]`.
- `s = ''`, `p = '**'` returns `[True, 1]` (each star takes nothing, one assignment).
- `s='ab'`, `p='**'` returns `[True, 3]`: consecutive stars multiply the count.
- `'?'` never matches the empty string.

**Follow-ups:**
- Same for regular expressions with `.` and `*` meaning "zero or more of the previous element"? Different transition: a starred element can repeat or vanish. The shape of the table is the same.
- Count modulo 10^9 + 7 for huge answers? Take the modulus in each cell; exactness is needed only for the question as stated here.
- Collapse repeated stars first? `**` and `*` match the same strings, but the COUNT of assignments differs, which is why the prompt counts them separately.

**Common mistakes:**
- Handling row 0 wrongly (`f[0][j]` is 1 only while the pattern prefix is all stars).
- In the star case, using `f[i-1][j-1]` instead of `f[i-1][j]` (the star can eat more than one letter).
- Treating `matches` as a separate calculation instead of `ways > 0`.
- Memoised recursion at larger sizes than the prompt (`RecursionError` when depth passes the limit).

### Q18 ⭐⭐ 🟡 Minimum ASCII delete sum. `s1` and `s2` are lowercase strings with 0 <= len <= 1000. You may delete letters from either string; deleting a letter costs its ASCII code (a = 97, ..., z = 122). Return the minimum total cost to make the two strings equal. Reduce it to a maximum-weight common subsequence, give the transition, and state the identity `total ASCII - 2 * (best common weight)`. Sizes are large enough that a memoised top-down recursion can nest deeper than CPython's default recursion limit of 1000 and raise RecursionError; a bottom-up (iterative) solution is required (do not rely on raising the limit). In the answer include a table walk-through on the first example and a seeded random cross-check of your solution against a plain recursion without a memo (len <= 7) on small inputs. Example: s1='sea', s2='eat' -> 231; s1='delete', s2='leet' -> 403; s1='', s2='ab' -> 195; s1='abc', s2='abc' -> 0.
**Asked at:** 2D DP pattern guides and lists (techinterview.org two-dimensional DP interview patterns, a LeetCode Discuss '13 DP patterns' post, codemia 2D DP and DP on strings and intervals; search snippets only, not opened) | Standard-problem lists known to the editor (not found as an opened page; indicative only, no company attribution)

**Pattern:** Two-string DP; deleting letters until the strings are equal means keeping a common subsequence, and the cheapest plan keeps the heaviest one. LCS with weights.

**Say this first (1 line):** "Whatever I keep is a common subsequence, everything else is deleted, so cost = total ASCII of both strings - 2 * (ASCII weight of what I keep); I maximise that weight with the LCS table where a match adds ord(letter) instead of 1."

**Brute force:** Plain recursion `f(i, j)`: if the heads are equal, advance both for free; otherwise delete one head, paying its ASCII code, and try both. Exponential, only for len <= 7. It is the checker (it is the cost recursion itself, not the reduction).

**Optimal:**
- Reduction: the two final equal strings are a common subsequence `t` of `s1` and `s2`. Deleted cost = `(total(s1) - weight(t)) + (total(s2) - weight(t))`. So minimise cost by maximising `weight(t)`.
- State: `w[i][j]` = maximum ASCII weight of a common subsequence of `s1[i:]` and `s2[j:]`.
- Transition: if `s1[i] == s2[j]` then `w[i][j] = ord(s1[i]) + w[i+1][j+1]`; else `max(w[i+1][j], w[i][j+1])`.
- Base cases: `w[n][j] = 0` and `w[i][m] = 0` (empty suffix).
- Answer: `sum(ord) of s1 + sum(ord) of s2 - 2 * w[0][0]`.
- Why weight, not length: the code uses `aaaaazzzz` / `zzzzaaaaa`. The longest common subsequence is `aaaaa` (length 5, weight 485), but `zzzz` (length 4) weighs 488, so the best plan keeps `zzzz`: answer 970, while a length-based shortcut gives 976.
- The direct cost DP (`d[i][j]` = min cost to equalise the suffixes) gives the same numbers; the code checks all three (reduction, direct table, plain recursion).
- Space: two rows (`prev` = row i+1, `cur` = row i). This question needs only the value, so no table is stored.
- Recursion: the top-down version nests up to `m + n` frames. As observed on Python 3.13 with the default limit 1000: two random 300-letter strings work; two disjoint 1000-letter strings (depth 2000) raise `RecursionError`. The prompt allows 1000 each, so the solution is bottom-up. Observation, not a rule: depth depends on the strings.

**Complexity:** Time O(mn) (1,000,000 cells at the maximum; sandbox time well under a few seconds, not a proof), space O(min(m, n)) with two rows if you put the shorter string on the column axis (O(n) for the code as written). Brute force exponential.

**Dry run:** `s1 = 'sea'`, `s2 = 'eat'`. `ord('s') = 115`, `ord('e') = 101`, `ord('a') = 97`, `ord('t') = 116`. Table `w` (rows = suffix of s1, columns = suffix of s2):

| | j=0 `eat` | j=1 `at` | j=2 `t` | j=3 `` |
|---|---|---|---|---|
| i=0 `sea` | 198 | 97 | 0 | 0 |
| i=1 `ea` | 198 | 97 | 0 | 0 |
| i=2 `a` | 97 | 97 | 0 | 0 |
| i=3 `` | 0 | 0 | 0 | 0 |

Cells: `w[2][1]`: `a == a`, so `97 + w[3][2] = 97`. `w[2][0]`: `a != e`, `max(w[3][0] = 0, w[2][1] = 97) = 97`. `w[1][0]`: `e == e`, so `101 + w[2][1] = 198`. `w[0][0]`: `s != e`, `max(w[1][0] = 198, w[0][1] = 97) = 198`. The best kept string is `ea`, weight 198. Total ASCII = `(115 + 101 + 97) + (101 + 97 + 116) = 313 + 314 = 627`. Answer `627 - 2 * 198 = 231` (delete `s` = 115 and `t` = 116).

**Code:**
```python
import itertools
import random
import sys
import time
from functools import lru_cache

random.seed(1818)

def weight_table(s1, s2):
    """w[i][j] = maximum total ASCII weight of a common subsequence of s1[i:] and s2[j:]."""
    n, m = len(s1), len(s2)
    w = [[0] * (m + 1) for _ in range(n + 1)]
    for i in range(n - 1, -1, -1):
        for j in range(m - 1, -1, -1):
            if s1[i] == s2[j]:
                w[i][j] = ord(s1[i]) + w[i + 1][j + 1]
            else:
                w[i][j] = max(w[i + 1][j], w[i][j + 1])
    return w

def min_delete_sum(s1, s2):
    """total ASCII of both strings - 2 * (best common weight). Two rows."""
    n, m = len(s1), len(s2)
    prev = [0] * (m + 1)
    for i in range(n - 1, -1, -1):
        cur = [0] * (m + 1)
        for j in range(m - 1, -1, -1):
            if s1[i] == s2[j]:
                cur[j] = ord(s1[i]) + prev[j + 1]
            else:
                cur[j] = max(prev[j], cur[j + 1])
        prev = cur
    return sum(map(ord, s1)) + sum(map(ord, s2)) - 2 * prev[0]

def direct_delete_table(s1, s2):
    """The cost DP itself (no reduction): d[i][j] = min cost to make s1[i:] and s2[j:] equal."""
    n, m = len(s1), len(s2)
    d = [[0] * (m + 1) for _ in range(n + 1)]
    for i in range(n, -1, -1):
        for j in range(m, -1, -1):
            if i == n: d[i][j] = sum(map(ord, s2[j:]))
            elif j == m: d[i][j] = sum(map(ord, s1[i:]))
            elif s1[i] == s2[j]: d[i][j] = d[i + 1][j + 1]
            else: d[i][j] = min(ord(s1[i]) + d[i + 1][j], ord(s2[j]) + d[i][j + 1])
    return d

def min_delete_memo(s1, s2):
    @lru_cache(maxsize=None)
    def f(i, j):
        if i == len(s1): return sum(map(ord, s2[j:]))
        if j == len(s2): return sum(map(ord, s1[i:]))
        if s1[i] == s2[j]: return f(i + 1, j + 1)
        return min(ord(s1[i]) + f(i + 1, j), ord(s2[j]) + f(i, j + 1))
    return f(0, 0)

def brute(s1, s2):
    """Plain recursion, no memo (len <= 7)."""
    def f(i, j):
        if i == len(s1): return sum(map(ord, s2[j:]))
        if j == len(s2): return sum(map(ord, s1[i:]))
        if s1[i] == s2[j]: return f(i + 1, j + 1)
        return min(ord(s1[i]) + f(i + 1, j), ord(s2[j]) + f(i, j + 1))
    return f(0, 0)

for a, b, want in [('sea', 'eat', 231), ('delete', 'leet', 403), ('', 'ab', 195), ('abc', 'abc', 0)]:
    assert min_delete_sum(a, b) == brute(a, b) == min_delete_memo(a, b) == direct_delete_table(a, b)[0][0] == want, (a, b)
print('4 prompt examples ok')

w = weight_table('sea', 'eat')
print("w (best common ASCII weight of s1[i:], s2[j:]) for s1='sea' (rows), s2='eat' (cols j=0..3):")
for i, row in enumerate(w):
    print(' ', 'sea-'[i], row)
tot = sum(map(ord, 'sea')) + sum(map(ord, 'eat'))
print('total ASCII =', tot, '| best common weight =', w[0][0], '| answer =', tot, '-', 2, '*', w[0][0], '=', tot - 2 * w[0][0])

for _ in range(1000):
    a = ''.join(random.choice('abcz') for _ in range(random.randint(0, 7)))
    b = ''.join(random.choice('abcz') for _ in range(random.randint(0, 7)))
    r = min_delete_sum(a, b)
    assert r == brute(a, b) == min_delete_memo(a, b) == direct_delete_table(a, b)[0][0], (a, b)
    assert r == sum(map(ord, a)) + sum(map(ord, b)) - 2 * weight_table(a, b)[0][0]
print('1000 seeded random pairs (len 0..7, alphabet abcz): two-row identity == plain recursion == memo == direct cost table')

cnt = 0
words = [''.join(x) for n in range(5) for x in itertools.product('ab', repeat=n)]
for a in words:
    for b in words:
        assert min_delete_sum(a, b) == brute(a, b); cnt += 1
print('exhaustive pairs over {a,b}, len <= 4:', cnt, 'ok')

# why weight and not length: with lowercase letters a LONGER common subsequence can weigh LESS (5 x 'a' = 485 < 4 x 'z' = 488)
a, b = 'aaaaazzzz', 'zzzzaaaaa'
tot = sum(map(ord, a)) + sum(map(ord, b))
print("s1='aaaaazzzz', s2='zzzzaaaaa': longest common is 'aaaaa' (len 5, weight 485); best weight keeps 'zzzz' (len 4, weight 488)")
print('  answer by weight:', min_delete_sum(a, b), '== plain recursion', brute(a, b), '| a length-based shortcut would say', tot - 2 * 485)
assert min_delete_sum(a, b) == tot - 2 * 488 < tot - 2 * 485

print('recursion limit:', sys.getrecursionlimit())
x = ''.join(random.choice('abcdefghij') for _ in range(1000)); y = ''.join(random.choice('abcdefghij') for _ in range(1000))
t = time.perf_counter(); r = min_delete_sum(x, y); dt = time.perf_counter() - t
assert r == sum(map(ord, x)) + sum(map(ord, y)) - 2 * weight_table(x, y)[0][0]
print('bottom-up 1000 x 1000 random:', r, '| sandbox time under 5 s:', dt < 5)
print('bottom-up disjoint 1000 + 1000 ->', min_delete_sum('a' * 1000, 'b' * 1000), '(= 97000 + 98000)')
print('memoised, two random 300-letter strings agrees:', min_delete_memo(x[:300], y[:300]) == min_delete_sum(x[:300], y[:300]))
try:
    min_delete_memo('a' * 1000, 'b' * 1000); print('memoised disjoint 1000 + 1000: ok')
except RecursionError:
    print('memoised disjoint 1000 + 1000: RecursionError')

assert min_delete_sum('', '') == 0 and min_delete_sum('a', 'a') == 0 and min_delete_sum('a', 'b') == 195 and min_delete_sum('z', '') == 122
print('edge asserts ok')
```

**Output (my run):**
```
4 prompt examples ok
w (best common ASCII weight of s1[i:], s2[j:]) for s1='sea' (rows), s2='eat' (cols j=0..3):
  s [198, 97, 0, 0]
  e [198, 97, 0, 0]
  a [97, 97, 0, 0]
  - [0, 0, 0, 0]
total ASCII = 627 | best common weight = 198 | answer = 627 - 2 * 198 = 231
1000 seeded random pairs (len 0..7, alphabet abcz): two-row identity == plain recursion == memo == direct cost table
exhaustive pairs over {a,b}, len <= 4: 961 ok
s1='aaaaazzzz', s2='zzzzaaaaa': longest common is 'aaaaa' (len 5, weight 485); best weight keeps 'zzzz' (len 4, weight 488)
  answer by weight: 970 == plain recursion 970 | a length-based shortcut would say 976
recursion limit: 1000
bottom-up 1000 x 1000 random: 107150 | sandbox time under 5 s: True
bottom-up disjoint 1000 + 1000 -> 195000 (= 97000 + 98000)
memoised, two random 300-letter strings agrees: True
memoised disjoint 1000 + 1000: RecursionError
edge asserts ok
```

**Edge cases:**
- Both empty returns 0; identical strings return 0.
- One empty: the answer is the total ASCII of the other (`''`, `'ab'` gives 195).
- No common letter: the answer is the total of both strings (disjoint 1000 + 1000 gives 195000).
- A longer common subsequence is not always the better one (see the `a`/`z` example).

**Follow-ups:**
- Minimum number of deletions (not weighted)? `m + n - 2 * LCS`, same table with weight 1.
- Return the strings that remain? Keep the table and walk forward like Q10, choosing the tie rule you state.
- Why is the identity `total - 2 * best`? Every kept letter is counted once in each string and is never deleted from either.

**Common mistakes:**
- Counting kept letters by length (LCS) instead of by weight.
- Subtracting the weight once instead of twice.
- Memoised recursion at 1000 x 1000 (`RecursionError`).
- Wrong base case: when one string is empty, the other's whole tail must be paid (its ASCII sum), not zero.
