# Book 5 Part 12, Q10-Q18 answers (Wave B)

### Q10 ⭐⭐⭐ 🔴 N-Queens: list every solution. `n` is an integer with 1 <= n <= 9. Place n queens on an n x n board so that no two share a row, a column or a diagonal. Return every solution as a list of n strings of length n (`'Q'` for the queen, `'.'` for empty), ordered so that the solutions are ascending by the tuple of queen columns row by row (row 0 first), which is the order a recursion that tries columns left to right produces. Return an empty list when there is no solution (n = 2 and n = 3). Use three sets (columns, `r - c` diagonals, `r + c` diagonals) and explain why one queen per row is not a restriction. Recursion depth is n <= 9. State, without proving it, that the number of solutions for n = 1..9 is 1, 0, 0, 2, 10, 4, 40, 92, 352 and show that your program prints exactly these counts. In the answer include a dry run on the first example and a seeded random cross-check of your solution against trying every permutation of columns and testing the diagonals on small inputs. Example: n=4 -> [['.Q..', '...Q', 'Q...', '..Q.'], ['..Q.', 'Q...', '...Q', '.Q..']]; n=1 -> [['Q']]; n=3 -> [].
**Asked at:** Backtracking pattern guides and lists (techinterview.org backtracking and recursion patterns posts, designgurus backtracking interview questions, a DEV Community backtracking-patterns post; search snippets only, not opened)

**Pattern:** Backtracking with constraint sets (choose a column for this row, explore, undo). It is a constraint-satisfaction search: the three sets are the pruning rule.

**Say this first (1 line):** "One queen per row, columns left to right, three sets for column, `r - c` and `r + c`; skip an attacked square, recurse, undo. Solutions come out in ascending column-tuple order for free."

**Brute force:** Try every permutation of columns (one queen per row and per column) and test every pair for a shared diagonal. That is n! permutations times O(n^2) pair checks. Fine as an oracle for n <= 8. Even more naive: any column in any row, which is n^n placements (n = 9: 387,420,489 leaves).

**Optimal:**
- Row-by-row recursion `go(r)`. At row `r` try columns `0..n-1` in order.
- Why one queen per row is not a restriction: two queens in the same row attack each other, and there are n queens and n rows, so every row holds exactly one. Same for columns, which is why the column set exists.
- Diagonals: cells on one `\` diagonal share `r - c`; cells on one `/` diagonal share `r + c`. Three sets give an O(1) "is this square attacked" test.
- Pruning rule: only recurse into a square that no earlier queen attacks. A partial board with an attacked pair can never become a solution, so the whole subtree is dead.
- Undo: remove the column and both diagonals from the sets when you come back.
- Order: columns are tried 0, 1, 2, ... so the first queen's column is the outermost sort key, then the second, and so on. That is exactly "ascending by the tuple of queen columns". The code asserts it for n = 1..9.
- Recursion depth is n <= 9, nowhere near CPython's default limit of 1000.

**Complexity:** Time: no polynomial bound; the search is exponential. A loose upper bound is the permutation tree, O(n!) leaves, and pruning cuts far below it. What I can state is measured: 8,394 calls for n = 9, against 986,410 calls for a columns-only search and 435,848,050 for the tree with no test at all. Building each solution's strings costs O(n^2). Space: O(n) for the recursion and the three sets, plus the output (352 boards of 81 characters for n = 9).

**Dry run:** n = 4. Each line is one call; "safe columns" are the squares the sets allow.
```
[]  row 0: safe columns [0, 1, 2, 3]
  [0]  row 1: safe columns [2, 3]
    [0, 2]  row 2: safe columns []  DEAD END
    [0, 3]  row 2: safe columns [1]
      [0, 3, 1]  row 3: safe columns []  DEAD END
  [1]  row 1: safe columns [3]
    ... [1, 3] -> [1, 3, 0] -> [1, 3, 0, 2]  SOLUTION
  [2]  row 1: safe columns [0] ... [2, 0, 3, 1]  SOLUTION
  [3]  row 1: safe columns [0, 1]  both end in DEAD END
```
The full tree is in the output below: 17 calls. The unpruned row-by-row tree (every column tried in every row) has 1 + 4 + 16 + 64 + 256 = 341 nodes. The two solutions are `[1, 3, 0, 2]` and `[2, 0, 3, 1]` (queen columns per row), which render as `['.Q..', '...Q', 'Q...', '..Q.']` and `['..Q.', 'Q...', '...Q', '.Q..']`.

**Code:**
```python
import itertools
import random

random.seed(1210)

def solve_queens(n, trace=None):
    """Backtracking, one queen per row. cols / (r-c) / (r+c) sets give O(1) conflict tests.
    Returns (solutions as strings, number of recursive calls). Columns tried left to right => ascending order."""
    out, placed = [], []
    cs, d1, d2 = set(), set(), set()
    calls = 0
    def go(r):
        nonlocal calls
        calls += 1
        if r == n:
            out.append(['.' * c + 'Q' + '.' * (n - c - 1) for c in placed])
            if trace is not None: trace.append('  ' * r + str(placed) + '  SOLUTION')
            return
        safe = [c for c in range(n) if c not in cs and (r - c) not in d1 and (r + c) not in d2]
        if trace is not None:
            trace.append('  ' * r + str(placed) + '  row %d: safe columns %s%s' % (r, safe, '  DEAD END' if not safe else ''))
        for c in safe:
            cs.add(c); d1.add(r - c); d2.add(r + c); placed.append(c)
            go(r + 1)
            placed.pop(); cs.discard(c); d1.discard(r - c); d2.discard(r + c)
    go(0)
    return out, calls

def unpruned_calls(n):
    """Same row-by-row tree but with NO conflict test: every column is tried in every row. Closed form: 1 + n + n^2 + ... + n^n."""
    return sum(n ** k for k in range(n + 1))

def unpruned_measured(n):
    """Count the calls of the unpruned row-by-row tree by actually running it (n <= 6)."""
    calls = 0
    def go(r):
        nonlocal calls
        calls += 1
        if r == n: return
        for _ in range(n): go(r + 1)
    go(0); return calls

def perm_tree_calls(n):
    """Calls of the 'one queen per row and per column' tree (no diagonal test): 1 + n + n(n-1) + ... + n!."""
    t, f = 0, 1
    for k in range(n + 1):
        t += f; f *= (n - k)
    return t

def brute(n):
    """Oracle: every permutation of columns (one queen per row AND per column), test diagonals pairwise.
    itertools.permutations yields lexicographic order, i.e. ascending column tuples."""
    res = []
    for p in itertools.permutations(range(n)):
        if all(abs(p[i] - p[j]) != j - i for i in range(n) for j in range(i + 1, n)):
            res.append(['.' * c + 'Q' + '.' * (n - c - 1) for c in p])
    return res

# prompt examples
assert solve_queens(4)[0] == [['.Q..', '...Q', 'Q...', '..Q.'], ['..Q.', 'Q...', '...Q', '.Q..']]
assert solve_queens(1)[0] == [['Q']]
assert solve_queens(3)[0] == [] and solve_queens(2)[0] == []
print("3 prompt examples ok")

# decision tree for n = 4
tr = []
sols, calls = solve_queens(4, tr)
print("--- decision tree, n=4 ---")
print("\n".join(tr))
print("calls with pruning:", calls, "| unpruned row-by-row tree:", unpruned_calls(4))
for n in range(1, 7):
    assert unpruned_measured(n) == unpruned_calls(n), n
print("closed form 1+n+...+n^n matches a measured run for n=1..6")

# counts for n = 1..9 and node-visit comparison
print("--- counts and calls ---")
counts = []
for n in range(1, 10):
    s, c = solve_queens(n)
    counts.append(len(s))
    assert s == sorted(s, key=lambda sol: [row.index('Q') for row in sol])   # ascending by queen columns
    print("n=%d solutions=%d calls=%d columns-only=%d unpruned=%d" % (n, len(s), c, perm_tree_calls(n), unpruned_calls(n)))
assert counts == [1, 0, 0, 2, 10, 4, 40, 92, 352]
print("counts n=1..9:", counts)

# seeded random cross-check against the permutation oracle (n = 1..8)
for _ in range(300):
    n = random.randint(1, 8)
    assert solve_queens(n)[0] == brute(n), n
print("300 seeded random sizes (1..8) agree with the permutation oracle")
# edge asserts
assert solve_queens(2) == ([], 3)          # root + two row-0 placements; every row-1 try is attacked
assert all(len(s) == 4 and all(len(row) == 4 for row in s) for s in solve_queens(4)[0])
print("edge asserts ok")
```

**Output (my run):**
```text
3 prompt examples ok
--- decision tree, n=4 ---
[]  row 0: safe columns [0, 1, 2, 3]
  [0]  row 1: safe columns [2, 3]
    [0, 2]  row 2: safe columns []  DEAD END
    [0, 3]  row 2: safe columns [1]
      [0, 3, 1]  row 3: safe columns []  DEAD END
  [1]  row 1: safe columns [3]
    [1, 3]  row 2: safe columns [0]
      [1, 3, 0]  row 3: safe columns [2]
        [1, 3, 0, 2]  SOLUTION
  [2]  row 1: safe columns [0]
    [2, 0]  row 2: safe columns [3]
      [2, 0, 3]  row 3: safe columns [1]
        [2, 0, 3, 1]  SOLUTION
  [3]  row 1: safe columns [0, 1]
    [3, 0]  row 2: safe columns [2]
      [3, 0, 2]  row 3: safe columns []  DEAD END
    [3, 1]  row 2: safe columns []  DEAD END
calls with pruning: 17 | unpruned row-by-row tree: 341
closed form 1+n+...+n^n matches a measured run for n=1..6
--- counts and calls ---
n=1 solutions=1 calls=2 columns-only=2 unpruned=2
n=2 solutions=0 calls=3 columns-only=5 unpruned=7
n=3 solutions=0 calls=6 columns-only=16 unpruned=40
n=4 solutions=2 calls=17 columns-only=65 unpruned=341
n=5 solutions=10 calls=54 columns-only=326 unpruned=3906
n=6 solutions=4 calls=153 columns-only=1957 unpruned=55987
n=7 solutions=40 calls=552 columns-only=13700 unpruned=960800
n=8 solutions=92 calls=2057 columns-only=109601 unpruned=19173961
n=9 solutions=352 calls=8394 columns-only=986410 unpruned=435848050
counts n=1..9: [1, 0, 0, 2, 10, 4, 40, 92, 352]
300 seeded random sizes (1..8) agree with the permutation oracle
edge asserts ok
```

**Edge cases:**
- n = 1 gives `[['Q']]`; n = 2 and n = 3 give `[]` (the search makes 3 calls for n = 2 and 6 for n = 3).
- Counts for n = 1..9 are 1, 0, 0, 2, 10, 4, 40, 92, 352; the program prints exactly these and asserts them. I state them, I do not prove them.
- Return a list of boards (list of list of strings), not one flat list; an empty result is `[]`, not `[[]]`.

**Follow-ups:**
- *Count only, n up to 14?* Use three bitmasks (columns, left diagonals shifted left, right diagonals shifted right) and `avail & -avail` to pick the lowest free column. No board strings, so it is much faster.
- *Use the symmetry?* Solve the left half of row 0 and mirror, about half the work; the odd-n middle column needs care.
- *Why not itertools.permutations?* It is correct (that is my oracle) but it never prunes: it builds all n! orders before testing.

**Common mistakes:**
- Forgetting to undo one of the three sets (usually a diagonal), which silently loses solutions.
- Using `r - c` for both diagonals; the second one must be `r + c`.
- Appending the same mutable list of columns to the output instead of building strings or copying.
- Claiming a time complexity like "O(n!)" as the exact cost; say it is an upper bound and quote the measured calls instead.

---

### Q11 ⭐⭐⭐ 🔴 Word search II with a trie. `board` is a list of 1 to 10 strings of equal length 1 to 10 (lowercase) and `words` is a list of 1 to 3000 distinct lowercase words (each 1 to 10 letters). Return the sorted list (ascending strings) of the words that can be spelled by a path of adjacent (horizontal or vertical) cells that uses no cell twice in one path; a word that cannot be spelled is not returned and the result is empty if none can. Build a trie of the words, run one DFS from each cell that walks the board and the trie together, store the whole word at the end node so you do not rebuild it, and prune: stop when the next letter is not a child, and (as an improvement) delete trie branches that no longer hold words. Explain why running the single-word search of Q9 once per word is too slow when there are thousands of words. Depth is at most 10. In the answer include a dry run on the first example and a seeded random cross-check of your solution against running the single-word search of Q9 once per word on small inputs. Example: board=['cats', 'xaot', 'dgsr'], words=['cat', 'cats', 'tar', 'dog', 'sat', 'star', 'cot'] -> ['cat', 'cats']; board=['ab'], words=['ab', 'ba', 'aba'] -> ['ab', 'ba']; board=['a'], words=['b'] -> [].
**Asked at:** Trie pattern guides (techinterview.org trie and prefix-tree interview patterns posts: autocomplete, word search, wildcard, maximum XOR; search snippets only, not opened) | Backtracking pattern guides and lists (techinterview.org backtracking and recursion patterns posts, designgurus backtracking interview questions, a DEV Community backtracking-patterns post; search snippets only, not opened)

**Pattern:** Trie plus grid DFS backtracking. The trie is the pruning rule: a path is only extended while it is a prefix of some word.

**Say this first (1 line):** "Put all words in a trie, run one DFS per start cell that walks the board and the trie together, stop when the next letter is not a child, store the whole word at the end node, and delete exhausted branches."

**Brute force:** For every word run the single-word search of Q9 (DFS from every cell, mark, recurse, unmark). With W words that repeats the same board walks W times and never shares a prefix: `cat` and `cats` explore the same cells twice.

**Optimal:**
- Build: for each word walk/create child dicts; at the last node store `node['$'] = word`. The key `'$'` cannot clash with a lowercase letter.
- Search: for each start cell whose letter is a child of the root, call `dfs(r, c, parent)`. Inside: take `nd = parent[ch]`; if `'$'` is in `nd`, record the word and `pop` it (so it is reported once, even if two paths spell it).
- Backtracking: write `'#'` into the cell (it is never a trie key, so the neighbour test `g[nr][nc] in nd` fails for it), recurse into neighbours whose letter is a child, then restore the letter.
- Pruning 1: no child for the next letter means no call at all.
- Pruning 2 (the improvement): after exploring, if `nd` has no children and no word left, delete it from its parent. Later starts then fail at the first letter instead of re-walking dead ground. Observed: same answer, 516 visits against 36,796 without it on one 8 x 8 random board.
- Depth is at most 10 (the longest word), so plain recursion is safe.
- Why per-word search is too slow: it costs W times a full search (up to 100 start cells and about 4 * 3^9 paths of length 10 each), while the trie search shares every common prefix and only follows letters that start some word. The trie cost does not multiply by W.

**Complexity:** Build O(total letters), at most about 30,000 for 3000 words of up to 10 letters. Search: each start cell explores at most 4 * 3^(L - 1) paths for the longest word length L, so a loose bound is R * C * 4 * 3^9, about 7.9 million for a 10 x 10 board and L = 10; in practice the trie cuts this to the prefixes that exist. Space O(total letters) for the trie plus O(L) recursion. Measured on a random 10 x 10 board over {a, b, c} with 3000 distinct words: 24,917 (cell, trie node) visits for the trie against 638,891 recursive calls for 3000 single-word searches (different units, a call is a smaller step, but the gap is the point).

**Dry run:** `board = ['cats','xaot','dgsr']`, words `cat, cats, tar, dog, sat, star, cot`. The program prints every (cell, trie node) visit; here is the story in order.
- Start (0,0) `c` (visit 1): child of the root. Neighbour (0,1) `a` fits `ca` (visit 2); (1,0) `x` does not. From `a`, neighbour (0,2) `t` fits `cat` (visit 3): the node holds `'$'`, so record `cat`. From `t`, neighbour (0,3) `s` fits `cats` (visit 4): record `cats`.
- The `cats` node has no children left, so it is deleted from its parent; then `cat` is empty and deleted, then `ca`. The `c` node stays because `cot` is still below it.
- Start (0,2) `t` (visits 5-6): `t` then `a` at (0,1) fits `ta`, but `tar` needs an `r` next to (0,1) and there is none: dead end.
- Start (0,3) `s` (visits 7-10): the neighbour `t` at (1,3) fits `st` but `star` needs an `a` next to it: dead. The neighbour `t` at (0,2) then `a` at (0,1) fits `sta`, but there is no `r` next to (0,1): dead.
- Starts (1,3) `t`, (2,0) `d`, (2,2) `s` (visits 11-13): one visit each, no neighbour continues any word. The other cells hold letters that are not children of the root (`x`, `a`, `o`, `g`, `r`), so they are skipped without a call.
- Total 13 visits; sorted result `['cat', 'cats']`. One single-word search per word needs 104 calls on the same input.

**Code:**
```python
import random

random.seed(1211)
DIRS = ((1, 0), (-1, 0), (0, 1), (0, -1))

def find_words(board, words, stats=None, prune=True, log=None):
    """Trie of all words + ONE DFS per start cell. The word is stored at its end node; found leaves are pruned."""
    R, C = len(board), len(board[0])
    root = {}
    for w in words:
        nd = root
        for ch in w:
            nd = nd.setdefault(ch, {})
        nd['$'] = w                                   # whole word stored at the end node
    g = [list(r) for r in board]
    found = []
    visits = 0
    def dfs(r, c, parent):
        nonlocal visits
        ch = g[r][c]
        nd = parent[ch]
        visits += 1                                   # one visit = one (cell, trie node) pair entered
        if log is not None: log.append('visit (%d,%d) %r%s' % (r, c, ch, '  -> found ' + nd['$'] if '$' in nd else ''))
        if '$' in nd:
            found.append(nd.pop('$'))                 # report once; pop so it cannot be reported twice
        g[r][c] = '#'                                 # mark the cell used on this path
        for dr, dc in DIRS:
            nr, nc = r + dr, c + dc
            if 0 <= nr < R and 0 <= nc < C and g[nr][nc] in nd:   # '#' and '$' are never children letters
                dfs(nr, nc, nd)
        g[r][c] = ch                                  # undo
        if prune and not nd:                          # no words left below: cut the branch
            del parent[ch]
    for r in range(R):
        for c in range(C):
            if g[r][c] in root:
                dfs(r, c, root)
    if stats is not None: stats.append(visits)
    return sorted(found)

def single_word(board, word, counter=None):
    """Q9-style search for ONE word (recursive, marks and unmarks the cell)."""
    R, C = len(board), len(board[0])
    g = [list(r) for r in board]
    def go(r, c, k):
        if counter is not None: counter[0] += 1
        if g[r][c] != word[k]: return False
        if k == len(word) - 1: return True
        g[r][c] = '#'
        for dr, dc in DIRS:
            nr, nc = r + dr, c + dc
            if 0 <= nr < R and 0 <= nc < C and go(nr, nc, k + 1):
                g[r][c] = word[k]; return True
        g[r][c] = word[k]
        return False
    return any(go(r, c, 0) for r in range(R) for c in range(C))

def brute(board, words, counter=None):
    return sorted(w for w in words if single_word(board, w, counter))

for b, ws, want in [(['cats', 'xaot', 'dgsr'], ['cat', 'cats', 'tar', 'dog', 'sat', 'star', 'cot'], ['cat', 'cats']),
                    (['ab'], ['ab', 'ba', 'aba'], ['ab', 'ba']), (['a'], ['b'], [])]:
    assert find_words(b, ws) == brute(b, ws) == want, (b, ws)
print("3 prompt examples ok")

# dry run: which words the trie DFS reports on the first example, and how many (cell, node) visits it needs
b, ws = ['cats', 'xaot', 'dgsr'], ['cat', 'cats', 'tar', 'dog', 'sat', 'star', 'cot']
st = []
print("first example:", find_words(b, ws, st), "trie visits:", st[0])
cnt = [0]; brute(b, ws, cnt)
lg = []; find_words(b, ws, [], log=lg)
print("\n".join(lg))
print("same example, one search per word: calls =", cnt[0])

# seeded random cross-check
for _ in range(400):
    R_, C_ = random.randint(1, 4), random.randint(1, 4)
    board = [''.join(random.choice('abc') for _ in range(C_)) for _ in range(R_)]
    words = list({''.join(random.choice('abc') for _ in range(random.randint(1, 6))) for _ in range(random.randint(1, 15))})
    assert find_words(board, words) == brute(board, words), (board, words)
print("400 seeded random boards agree with one single-word search per word")

# why the trie wins: many words, shared prefixes (10 x 10 board, 3000 words, alphabet 'abc')
board = [''.join(random.choice('abc') for _ in range(10)) for _ in range(10)]
words = set()
while len(words) < 3000:
    words.add(''.join(random.choice('abc') for _ in range(random.randint(1, 10))))
words = sorted(words)
st = []; a = find_words(board, words, st)
cnt = [0]; b2 = brute(board, words, cnt)
assert a == b2
print("10x10 board, 3000 words: found %d words | trie visits %d | single-word calls %d" % (len(a), st[0], cnt[0]))
# effect of deleting exhausted branches: same answer, fewer visits when many words are found
board = [''.join(random.choice('ab') for _ in range(8)) for _ in range(8)]
words = sorted({''.join(random.choice('ab') for _ in range(random.randint(1, 8))) for _ in range(300)})
s1, s2 = [], []
assert find_words(board, words, s1, prune=True) == find_words(board, words, s2, prune=False)
print("8x8 board, %d words: visits with branch deletion %d, without %d" % (len(words), s1[0], s2[0]))
assert s1[0] <= s2[0]
# max-size edge cases
assert find_words(['a' * 10] * 10, ['a' * 10]) == ['a' * 10]
assert find_words(['a'], ['a']) == ['a']
assert find_words(['ab'], ['abc']) == []
assert find_words(['aa'], ['aaa']) == []                  # a cell may not be reused in one path
assert find_words(['ab', 'cd'], ['abdc', 'acdb', 'ad']) == ['abdc', 'acdb']   # 'ad' is diagonal
print("edge asserts ok")
```

**Output (my run):**
```text
3 prompt examples ok
first example: ['cat', 'cats'] trie visits: 13
visit (0,0) 'c'
visit (0,1) 'a'
visit (0,2) 't'  -> found cat
visit (0,3) 's'  -> found cats
visit (0,2) 't'
visit (0,1) 'a'
visit (0,3) 's'
visit (1,3) 't'
visit (0,2) 't'
visit (0,1) 'a'
visit (1,3) 't'
visit (2,0) 'd'
visit (2,2) 's'
same example, one search per word: calls = 104
400 seeded random boards agree with one single-word search per word
10x10 board, 3000 words: found 2592 words | trie visits 24917 | single-word calls 638891
8x8 board, 153 words: visits with branch deletion 516, without 36796
edge asserts ok
```

**Edge cases:**
- Board 1 x 1: `['a']` with word `a` is found; word `b` gives `[]`.
- A cell may not repeat inside one path: `['aa']` cannot spell `aaa`.
- Diagonal neighbours do not count (`ad` on `['ab','cd']` is not found).
- Two paths for the same word must still report it once: `pop('$')` guarantees it.
- A word that is a prefix of another (`cat`, `cats`) must record both: check `'$'` before going deeper, do not stop at the first one.

**Follow-ups:**
- *Why delete trie nodes?* It makes the cost shrink as words are found; without it the same dead prefixes are walked again from every start cell (516 against 36,796 visits in my run).
- *Memory?* A dict per node is heavy; for 3000 short words it is fine. Q33 measures dict-of-dicts against arrays of 26.
- *Many queries on one board?* Build the trie once per word list; if the board changes and words are fixed, only the DFS repeats.

**Common mistakes:**
- Not unmarking the cell after recursion (a leftover `'#'` breaks later paths).
- Returning duplicates because the word is recorded on every path that spells it.
- Rebuilding the word by string concatenation along the path instead of storing it at the end node.
- Deleting from a dict you are iterating over (here the delete happens after the neighbour loop, which is safe).

---

### Q12 ⭐⭐ 🟢 Power of two and power of four. `n` is an integer with -2^31 <= n < 2^31 (negatives and zero included). Return `[is_power_of_two, is_power_of_four]`, where a power of two is 2^k for some integer k >= 0 (so 1 counts, 0 and negatives do not). Use `n > 0 and n & (n - 1) == 0` for the first, explain why it works (a power of two has exactly one set bit, and `n & (n - 1)` clears it), and add one more mask for the second (the single bit must sit at an even position: `n & 0x55555555 != 0`), justify the mask for the 31-bit range, and say why a loop that divides by 2 works too but costs O(log n). In the answer include a dry run on the first example and a seeded random cross-check of your solution against membership in the explicit sets {2^k} and {4^k} on small inputs. Example: n=16 -> [True, True]; n=8 -> [True, False]; n=0 -> [False, False]; n=-4 -> [False, False]; n=1 -> [True, True]; n=1073741824 -> [True, True].
**Asked at:** Bit manipulation question lists (Techie Delight bit-manipulation list, Interview Cake, a Devinterview GitHub list, Interview Kickstart; search snippets only, not opened)

**Pattern:** Bit manipulation: one-set-bit test with `n & (n - 1)` plus a position mask.

**Say this first (1 line):** "A power of two has exactly one set bit, and `n & (n - 1)` clears the lowest set bit, so it is zero only for powers of two (and 0, which I exclude with `n > 0`); for four, the single bit must sit at an even position: `n & 0x55555555 != 0`."

**Brute force:** Divide by 2 (or 4) while the remainder is 0 and see if you end at 1. Correct, O(log n) steps. Or test membership in the explicit set of 31 powers of two and 16 powers of four (my oracle).

**Optimal:**
- `n > 0`: negatives and 0 are not powers of two. The guard matters only for 0 (`0 & -1 == 0`); a negative number has infinitely many 1 bits in Python, so `n & (n - 1)` is never 0 for it. Observed over -1000..1000: without the guard the test is wrong for exactly `[0]`.
- `n & (n - 1) == 0`: subtracting 1 flips the lowest set bit and every zero below it, so the AND clears that one bit. If it was the only bit, the result is 0.
- Precedence, Python 3.13: `&` binds tighter than `==` and `!=`, so `n & (n - 1) == 0` is `(n & (n - 1)) == 0`. In C it would not be; in Python you do not need extra brackets.
- Power of four: 4^k = 2^(2k), the bit sits at an even position. For 1 <= n < 2^31 the largest power of four is 4^15 = 2^30, positions 0, 2, ..., 30. `0x55555555` is `0101...0101` with set bits at exactly those positions (the code prints and asserts that). So for a power of two, `n & 0x55555555 != 0` says the bit is at an even position.
- The mask alone is not enough: it accepts 3, 5, 6, 7, 9, 11 and so on. You need both tests.
- Outside the stated range the mask breaks: 4^16 = 2^32 has its bit at position 32, which `0x55555555` does not cover. A range-free alternative is `n.bit_length() % 2 == 1` for a power of two (2^k has `bit_length` k + 1); I checked it for k = 0..199.

**Complexity:** O(1) time and space for the bit tests (the word size is fixed by the stated range). The division loop is O(log n) divisions.

**Dry run:** n = 16 = `0b10000`: `n - 1` = `0b01111`, AND is 0, so a power of two. Mask: `16 & 0x55555555` = `0x10` (bit 4, even), non-zero, so a power of four: `[True, True]`. n = 8 = `0b1000`: AND with 7 is 0; `8 & 0x55555555` = 0 (bit 3 is odd), so `[True, False]`. n = 0: `n > 0` fails, `[False, False]`. n = -4: `n > 0` fails.

**Code:**
```python
import random

random.seed(1212)

def power_two_four(n):
    p2 = n > 0 and n & (n - 1) == 0          # '&' binds tighter than '==' in Python, so no extra brackets needed
    p4 = p2 and (n & 0x55555555) != 0
    return [p2, p4]

def power_by_division(n):
    """Loop version, O(log n): keep halving (quartering) while the remainder is zero."""
    def pw(n, base):
        if n <= 0: return False
        while n % base == 0: n //= base
        return n == 1
    return [pw(n, 2), pw(n, 4)]

POW2 = {2 ** k for k in range(31)}
POW4 = {4 ** k for k in range(16)}
def brute(n): return [n in POW2, n in POW4]

for n, want in [(16, [True, True]), (8, [True, False]), (0, [False, False]), (-4, [False, False]), (1, [True, True]),
                (1073741824, [True, True])]:
    assert power_two_four(n) == power_by_division(n) == brute(n) == want, n
print("6 prompt examples ok")

print("dry run n=16:  bin", bin(16), " n-1 =", bin(15), " n & (n-1) =", 16 & 15, " n & 0x55555555 =", hex(16 & 0x55555555))
print("dry run n=8 :  bin", bin(8), " n & (n-1) =", 8 & 7, " n & 0x55555555 =", 8 & 0x55555555)

# the mask: 4^k for k = 0..15 are exactly the powers of two in 1..2^30 at an even bit position
assert {4 ** k for k in range(16)} == {1 << i for i in range(0, 31, 2)}
print("mask 0x55555555 = %s ; its set bits are the even positions 0..30: %s" % (bin(0x55555555), [i for i in range(32) if 0x55555555 >> i & 1] == list(range(0, 32, 2))))

# exhaustive check over a wide window and over every power of two and its neighbours in range
window = list(range(-70000, 70001))
special = [s * (2 ** k + d) for k in range(31) for d in (-1, 0, 1) for s in (1, -1)] + [-2 ** 31, 2 ** 31 - 1]
for n in window + special:
    assert power_two_four(n) == power_by_division(n) == brute(n), n
print("exhaustive: %d values in [-70000, 70000] plus %d special values agree" % (len(window), len(special)))

# seeded random over the full 32-bit signed range
for _ in range(3000):
    n = random.randint(-2 ** 31, 2 ** 31 - 1)
    assert power_two_four(n) == brute(n)
print("3000 seeded random values over the full range agree with the explicit sets")

# why each part of the test is there
no_guard = [n for n in range(-1000, 1001) if (n & (n - 1) == 0) != (n in POW2)]
print("without 'n > 0', n & (n-1) == 0 is wrong for exactly:", no_guard)
mask_only = [n for n in range(1, 200) if bool(n & 0x55555555) != (n in POW4)]
print("mask alone (no power-of-two test) wrongly accepts, e.g.:", mask_only[:6], "-> you need BOTH tests")
print("outside the stated range: 4**16 =", 4 ** 16, "has the single bit at position 32; n & 0x55555555 =", (4 ** 16) & 0x55555555, "-> would report False")
# alternative for the second test that needs no mask and works for any size: a power of two 2^k has bit_length k+1
assert all(power_two_four(2 ** k)[1] == (k % 2 == 0) == ((2 ** k).bit_length() % 2 == 1) for k in range(0, 31))
assert all(((1 << k).bit_length() % 2 == 1) == (k % 2 == 0) for k in range(0, 200))
print("bit_length alternative: 2^k is a power of 4 exactly when its bit_length is odd (checked k = 0..199)")
assert all(((n - 1) % 3 == 0) == (n in POW4) for n in sorted(POW2))
assert all((1 << (n - 1).bit_length()) >= n and (1 << (n - 1).bit_length()) // 2 < n for n in range(1, 5000))
print("follow-up claims ok: (n-1) % 3 == 0 separates 4^k from 2*4^k; 1 << (n-1).bit_length() is the next power of two >= n")
edge = [(2 ** 31 - 1, [False, False]), (-2 ** 31, [False, False]), (2 ** 30, [True, True]), (2 ** 29, [True, False])]
for n, want in edge: assert power_two_four(n) == want
print("edge asserts ok")
```

**Output (my run):**
```text
6 prompt examples ok
dry run n=16:  bin 0b10000  n-1 = 0b1111  n & (n-1) = 0  n & 0x55555555 = 0x10
dry run n=8 :  bin 0b1000  n & (n-1) = 0  n & 0x55555555 = 0
mask 0x55555555 = 0b1010101010101010101010101010101 ; its set bits are the even positions 0..30: True
exhaustive: 140001 values in [-70000, 70000] plus 188 special values agree
3000 seeded random values over the full range agree with the explicit sets
without 'n > 0', n & (n-1) == 0 is wrong for exactly: [0]
mask alone (no power-of-two test) wrongly accepts, e.g.: [3, 5, 6, 7, 9, 11] -> you need BOTH tests
outside the stated range: 4**16 = 4294967296 has the single bit at position 32; n & 0x55555555 = 0 -> would report False
bit_length alternative: 2^k is a power of 4 exactly when its bit_length is odd (checked k = 0..199)
follow-up claims ok: (n-1) % 3 == 0 separates 4^k from 2*4^k; 1 << (n-1).bit_length() is the next power of two >= n
edge asserts ok
```

**Edge cases:**
- 0 and negatives: always `[False, False]`.
- 1 = 2^0 = 4^0: `[True, True]`.
- 2^30 = 1073741824: `[True, True]`; 2^29: `[True, False]`.
- 2^31 - 1 (all ones, not a power) and -2^31 (a negative): `[False, False]`.

**Follow-ups:**
- *Another test for power of four without a mask?* `(n - 1) % 3 == 0` on a power of two (4^k - 1 is divisible by 3, 2 * 4^k - 1 is not); or the `bit_length` parity above.
- *Power of two with a popcount?* `n > 0 and n.bit_count() == 1` (`int.bit_count` needs Python 3.10 or newer, editor knowledge); `bin(n).count('1') == 1` on older versions.
- *Next power of two at or above n?* `1 << (n - 1).bit_length()` for n >= 1.

**Common mistakes:**
- Dropping `n > 0` and returning True for 0.
- Using only the mask for the four test.
- Using `n & (n - 1) == 0` in C-style precedence worries and adding wrong brackets like `n & ((n - 1) == 0)`, which is a different expression.
- Testing the mask on a wider range without widening it.

---

### Q13 ⭐⭐ 🟢 Hamming distance and total Hamming distance. The Hamming distance of two integers is the number of bit positions at which they differ. Given integers `x`, `y` (0 <= x, y < 2^31) and a list `nums` of 2 <= len <= 10^4 integers in 0..2^31 - 1, return `[hamming(x, y), total]` where `total` is the sum of the Hamming distances over all unordered pairs i < j of `nums`. Compute the first as the popcount of `x ^ y`, and the second in O(31 * n) by counting, for each bit position, how many numbers have the bit set (`ones`) and adding `ones * (n - ones)`; explain why that equals the pair count. In the answer include a dry run on the first example and a seeded random cross-check of your solution against comparing every pair bit by bit on small inputs. Example: x=1, y=4, nums=[5, 9, 12, 3] -> [2, 14]; x=0, y=0, nums=[7, 7] -> [0, 0]; x=2147483647, y=0, nums=[0, 2147483647] -> [31, 31]; x=6, y=5, nums=[1, 2, 4] -> [2, 6].
**Asked at:** Bit manipulation question lists (Techie Delight bit-manipulation list, Interview Cake, a Devinterview GitHub list, Interview Kickstart; search snippets only, not opened)

**Pattern:** Bit manipulation, per-bit counting (contribution technique): count pairs by bit position instead of by pair.

**Say this first (1 line):** "Pair distance is popcount of `x ^ y`. For the total over all pairs, for each of the 31 bits count how many numbers have it set, `ones`, and add `ones * (n - ones)`, because only a (1, 0) pair differs at that bit."

**Brute force:** For every unordered pair i < j compare all 31 bits: O(n^2 * 31). With n = 10^4 that is about 50 million pairs times 31, far too slow for Python.

**Optimal:**
- `hamming(x, y) = bin(x ^ y).count('1')`: XOR has a 1 exactly where the bits differ, so its popcount is the distance. (`(x ^ y).bit_count()` also works on Python 3.10 or newer; that version is editor knowledge.)
- Total: the distance of a pair is the sum over bits of "do they differ here". Swap the sums: for each bit, count the pairs that differ at it, then add over bits.
- At bit b let `ones` numbers have 1 and `n - ones` have 0. A pair differs at b exactly when one is from each group, and every such pair is counted once as an unordered pair: `ones * (n - ones)` pairs. Pairs with both 1 or both 0 contribute 0.
- 31 bits because every value is below 2^31 (no sign bit, no masking needed for non-negative inputs).

**Complexity:** Time O(31 * n) for the total, O(1) for the pair; space O(1). For n = 10^4 that is 310,000 bit tests instead of about 50 million pair comparisons. The maximum total is 31 * 5000 * 5000 = 775,000,000 (half 0, half 2^31 - 1); Python ints never overflow, but in a 32-bit language this would be a point to mention.

**Dry run:** `nums = [5, 9, 12, 3]` = `0101, 1001, 1100, 0011`.

| bit | numbers with the bit set | ones | zeros | pairs |
|---|---|---|---|---|
| 0 | 5, 9, 3 | 3 | 1 | 3 |
| 1 | 3 | 1 | 3 | 3 |
| 2 | 5, 12 | 2 | 2 | 4 |
| 3 | 9, 12 | 2 | 2 | 4 |

Total 3 + 3 + 4 + 4 = 14. Bits 4..30 are zero everywhere, so they add 0. Pair part: `1 ^ 4` = `0b101`, popcount 2. Answer `[2, 14]`.

**Code:**
```python
import itertools
import random

random.seed(1213)
BITS = 31

def hamming_pair(x, y):
    return bin(x ^ y).count('1')

def hamming_total(nums):
    n, total = len(nums), 0
    for b in range(BITS):
        ones = sum((v >> b) & 1 for v in nums)
        total += ones * (n - ones)                # pairs that differ at bit b: one with 1, one with 0
    return total

def solve(x, y, nums):
    return [hamming_pair(x, y), hamming_total(nums)]

def brute(x, y, nums):
    h = lambda a, b: sum(1 for i in range(BITS) if ((a >> i) & 1) != ((b >> i) & 1))
    return [h(x, y), sum(h(a, b) for a, b in itertools.combinations(nums, 2))]

for (x, y, nums), want in [((1, 4, [5, 9, 12, 3]), [2, 14]), ((0, 0, [7, 7]), [0, 0]),
                           ((2147483647, 0, [0, 2147483647]), [31, 31]), ((6, 5, [1, 2, 4]), [2, 6])]:
    assert solve(x, y, nums) == brute(x, y, nums) == want, (x, y, nums)
print("4 prompt examples ok")

print("dry run nums = [5, 9, 12, 3]:")
nums = [5, 9, 12, 3]
tot = 0
for b in range(4):
    ones = sum((v >> b) & 1 for v in nums)
    tot += ones * (len(nums) - ones)
    print("  bit %d: set in %s -> ones=%d zeros=%d pairs=%d" % (b, [v for v in nums if v >> b & 1], ones, len(nums) - ones, ones * (len(nums) - ones)))
print("  total", tot, "| popcount(1 ^ 4) = popcount(%s) = %d" % (bin(1 ^ 4), hamming_pair(1, 4)))

for _ in range(500):
    nums = [random.randint(0, 2 ** random.randint(1, 31) - 1) for _ in range(random.randint(2, 8))]
    x, y = random.randint(0, 2 ** 31 - 1), random.randint(0, 2 ** 31 - 1)
    assert solve(x, y, nums) == brute(x, y, nums), (x, y, nums)
print("500 seeded random cases agree with the pairwise bit-by-bit brute force")

# edge / size asserts
assert hamming_total([7, 7, 7]) == 0
assert hamming_total([0, 2 ** 31 - 1]) == 31
assert hamming_total([0] * 5000 + [2 ** 31 - 1] * 5000) == 31 * 5000 * 5000      # n = 10^4, max total
assert solve(0, 0, [0, 0]) == [0, 0]
print("max case n=10^4 total:", hamming_total([0] * 5000 + [2 ** 31 - 1] * 5000), "| fits easily: Python ints do not overflow")
print("edge asserts ok")
```

**Output (my run):**
```text
4 prompt examples ok
dry run nums = [5, 9, 12, 3]:
  bit 0: set in [5, 9, 3] -> ones=3 zeros=1 pairs=3
  bit 1: set in [3] -> ones=1 zeros=3 pairs=3
  bit 2: set in [5, 12] -> ones=2 zeros=2 pairs=4
  bit 3: set in [9, 12] -> ones=2 zeros=2 pairs=4
  total 14 | popcount(1 ^ 4) = popcount(0b101) = 2
500 seeded random cases agree with the pairwise bit-by-bit brute force
max case n=10^4 total: 775000000 | fits easily: Python ints do not overflow
edge asserts ok
```

**Edge cases:**
- All numbers equal: total 0 (every bit has `ones` = 0 or n).
- n = 2 reduces to a single pair distance.
- Values using all 31 bits: `[0, 2147483647]` gives 31.
- x = y gives 0.

**Follow-ups:**
- *Sum over all ordered pairs?* Double the total.
- *Count by character instead of bit (strings of equal length)?* Same idea with 26 counters per position.
- *Hamming weight of one number faster?* Brian Kernighan's `m &= m - 1` loop, one round per set bit (Q2).

**Common mistakes:**
- Using `ones * (n - ones)` and then halving; that formula already counts unordered pairs once.
- Looping over 32 bits and treating bit 31 as a sign bit; the input range stops at bit 30.
- Doing the O(n^2) pair loop and calling it "fine" at n = 10^4.

---

### Q14 ⭐⭐ 🟢 Replace words with their shortest root. `roots` is a list of 1 to 1000 lowercase strings (length 1 to 100) and `sentence` is a string of 1 to 1000 lowercase words separated by single spaces (no leading or trailing space, word length 1 to 100). Replace each word by the shortest root that is a prefix of it; if no root is a prefix, keep the word. Return the new sentence. Build a trie of the roots and walk each word until the first end-of-root flag; explain why the first flag you meet is the shortest root and why duplicate roots do not matter. The same trie shape as Q3. Cost: O(total root length + sentence length). In the answer include a dry run on the first example and a seeded random cross-check of your solution against scanning every root for every word on small inputs. Example: roots=['to', 'tra', 'a'], sentence='tomorrow a train travels to tokyo' -> 'to a tra tra to to'; roots=['ab'], sentence='cab ab abc' -> 'cab ab ab'; roots=['b', 'be'], sentence='best bee ace' -> 'b b ace'.
**Asked at:** Trie pattern guides (techinterview.org trie and prefix-tree interview patterns posts: autocomplete, word search, wildcard, maximum XOR; search snippets only, not opened)

**Pattern:** Trie prefix walk, stopping at the first end-of-word flag.

**Say this first (1 line):** "Insert all roots in a trie with an end flag; for each word walk letter by letter and stop at the first flag, which is the shortest root; if you fall off the trie first, keep the word."

**Brute force:** For each word test every root with `startswith` and keep the shortest hit: O(words * roots * root length). With 1000 words and 1000 roots of length 100 that is about 10^8 character steps in the worst case.

**Optimal:**
- Build the trie: dict per node, `'$'` marks "a root ends here" (`'$'` cannot be a lowercase letter).
- For each word: `nd = root`, `k = 0`; while `k < len(word)`, no flag at `nd`, and `word[k]` is a child: step. Afterwards, if the current node has a flag, the answer is `word[:k]`; otherwise keep the word.
- Why the first flag is the shortest root: the walk visits the prefixes of the word in increasing length, so the first node with a flag is the shortest prefix that is a root. Longer roots below it are never reached.
- Duplicate roots do not matter: inserting the same root twice sets the same flag on the same node.
- Same trie shape as the insert/search/startsWith API of Q3.

**Complexity:** Build O(total root length), at most 1000 * 100 = 100,000 steps. Each word costs at most its own length, so the sentence costs O(total sentence length). Space O(total root length) for the trie nodes. (A word equal to or shorter than a root is simply not replaced.)

**Dry run:** roots `to, tra, a`; trie: `t -> {o*, r -> a*}`, `a*` (a star marks the flag).
- `tomorrow`: `t`, `o` reaches a flag: `to`.
- `a`: `a` has a flag: `a`.
- `train`: `t`, `r`, `a` has a flag: `tra` (the program prints this walk).
- `travels`: same path: `tra`. `to`: `to`. `tokyo`: `to`.
Result `to a tra tra to to`. Second example: roots `ab`, `cab ab abc` gives `cab ab ab`: `cab` starts with `c`, which is not in the trie, so it stays.

**Code:**
```python
import random

random.seed(1214)

def build_trie(roots):
    root = {}
    for w in roots:
        nd = root
        for ch in w:
            nd = nd.setdefault(ch, {})
        nd['$'] = True                               # end-of-root flag ('$' can never be a lowercase letter)
    return root

def replace_words(roots, sentence):
    trie = build_trie(roots)
    out = []
    for word in sentence.split(' '):
        nd, k = trie, 0
        while k < len(word) and '$' not in nd and word[k] in nd:   # stop at the FIRST flag: it is the shortest root
            nd = nd[word[k]]
            k += 1
        out.append(word[:k] if '$' in nd else word)
    return ' '.join(out)

def brute(roots, sentence):
    out = []
    for word in sentence.split(' '):
        c = [r for r in roots if word.startswith(r)]
        out.append(min(c, key=len) if c else word)
    return ' '.join(out)

for roots, s, want in [(['to', 'tra', 'a'], 'tomorrow a train travels to tokyo', 'to a tra tra to to'),
                       (['ab'], 'cab ab abc', 'cab ab ab'), (['b', 'be'], 'best bee ace', 'b b ace')]:
    assert replace_words(roots, s) == brute(roots, s) == want, (roots, s)
print("3 prompt examples ok")

# dry run: roots = ['to','tra','a'], word 'train'
t = build_trie(['to', 'tra', 'a'])
print("trie top level:", sorted(k for k in t), "| under 't':", sorted(k for k in t['t']), "| under 'tr':", sorted(t['t']['r']))
w = 'train'; nd = t; path = ''
for ch in w:
    if '$' in nd or ch not in nd: break
    nd = nd[ch]; path += ch
    print("  read %r -> node for %r, end flag here: %s" % (ch, path, '$' in nd))
print("  result:", path if '$' in nd else w)

for _ in range(500):
    roots = [''.join(random.choice('abc') for _ in range(random.randint(1, 3))) for _ in range(random.randint(1, 6))]
    words = [''.join(random.choice('abc') for _ in range(random.randint(1, 5))) for _ in range(random.randint(1, 8))]
    s = ' '.join(words)
    assert replace_words(roots, s) == brute(roots, s), (roots, s)
print("500 seeded random cases agree with scanning every root for every word")

# duplicate roots and ordering do not matter; a longer root never wins over a shorter prefix root
assert replace_words(['ab', 'ab', 'a'], 'abc') == 'a' == replace_words(['a', 'ab', 'ab'], 'abc')
assert replace_words(['abc'], 'ab') == 'ab'              # root longer than the word: no replacement
assert replace_words(['a'], 'a') == 'a'                  # word equal to a root
assert replace_words(['z'], 'a') == 'a'                  # no root matches
assert replace_words(['a'], 'aaa a aa') == 'a a a'
print("edge asserts ok")

# max-size shape: 1000 roots of length 100 and a 1000-word sentence of length-100 words
roots = [''.join(random.choice('ab') for _ in range(100)) for _ in range(1000)]
sent = ' '.join(''.join(random.choice('ab') for _ in range(100)) for _ in range(1000))
assert replace_words(roots, sent) == brute(roots, sent)
print("max-size shape ok (1000 roots x 100 letters, 1000 words x 100 letters)")
```

**Output (my run):**
```text
3 prompt examples ok
trie top level: ['a', 't'] | under 't': ['o', 'r'] | under 'tr': ['a']
  read 't' -> node for 't', end flag here: False
  read 'r' -> node for 'tr', end flag here: False
  read 'a' -> node for 'tra', end flag here: True
  result: tra
500 seeded random cases agree with scanning every root for every word
edge asserts ok
max-size shape ok (1000 roots x 100 letters, 1000 words x 100 letters)
```

**Edge cases:**
- Word equal to a root: unchanged.
- Root longer than the word: no flag reached, word kept.
- No root matches: word kept.
- Roots `['ab', 'a']` and word `abc`: `a` wins (shortest), whatever the insert order.
- One word only; single-letter roots.

**Follow-ups:**
- *Why not a set of roots and test every prefix of the word?* Works: for each word build prefixes of length 1, 2, ... and look up in a set, stopping at the first hit. Cost is O(L^2) per word because each prefix slice and hash costs O(L); the trie walk is O(L).
- *Longest root instead of shortest?* Keep walking and remember the last flag.
- *Memory of the trie?* Up to one dict per root character (100,000 nodes here); a sorted list of roots with `bisect` is a lighter alternative (Part 3 Q36 compares the two at concept level).

**Common mistakes:**
- Checking the flag after stepping past it, so the walk continues into longer roots and returns the longest.
- Using `str.replace`, which replaces anywhere in the word, not only at the start.
- Splitting with `split()` and rejoining with single spaces when the problem fixes single spaces (here `split(' ')` matches the input format exactly).

---

### Q15 ⭐⭐ 🟡 Repeated and missing number by XOR. `nums` has n integers (2 <= n <= 10^5) from 1..n in which exactly one value appears twice and exactly one value of 1..n is absent. Return `[duplicate, missing]`. Solve it in O(n) time and O(1) extra space with XOR: XOR every `nums[i]` with every `i` from 1..n to get `duplicate ^ missing`, take its lowest set bit with `x & -x`, split all numbers and indices into two groups by that bit, and XOR within each group; then decide which of the two results is the duplicate. Explain why the two values must differ in some bit and why the groups separate them. Also show the XOR swap `a ^= b; b ^= a; a ^= b` and say why `a, b = b, a` is what you write in Python (and why the XOR swap breaks if both names point at the same list slot). The single-missing-number version (hash set, sorted, sum) is Part 1 Q8. In the answer include a dry run on the first example and a seeded random cross-check of your solution against a Counter and a membership scan on small inputs. Example: nums=[1, 3, 3, 4] -> [3, 2]; nums=[2, 2] -> [2, 1]; nums=[1, 1, 3, 4, 5] -> [1, 2]; nums=[3, 1, 2, 5, 5] -> [5, 4].
**Asked at:** Bit manipulation question lists (Techie Delight bit-manipulation list, Interview Cake, a Devinterview GitHub list, Interview Kickstart; search snippets only, not opened)

**Pattern:** XOR cancellation plus partition by a differing bit (`x & -x`).

**Say this first (1 line):** "XOR all numbers with all indices 1..n: everything cancels except `duplicate ^ missing`; take its lowest set bit, split numbers and indices by that bit, XOR inside each group, and one scan tells you which result is the duplicate."

**Brute force:** A `Counter` for the value seen twice, then a scan of 1..n for the absent one. O(n) time but O(n) space. Or sort and compare neighbours: O(n log n), and it changes the input.

**Optimal:**
- Consider the multiset `nums` plus the indices 1..n. A normal value appears once in each: twice in total, it cancels. The duplicate appears three times (twice in `nums`, once as an index): it survives. The missing value appears once (only as an index): it survives. So `x = duplicate ^ missing`.
- `x != 0` because the duplicate is present and the missing value is absent, so they are different numbers. Different numbers differ in some bit.
- `low = x & -x` is the lowest set bit of `x`, a bit where the two differ.
- Split every number and every index into two groups by `value & low`. The duplicate and the missing value land in different groups. Inside each group every other value still shows up an even number of times (once as a number, once as an index, or twice as the duplicate's pair), so it cancels. One group XORs to the duplicate (it has 3 copies), the other to the missing value (1 copy).
- Which is which: one more pass, `nums.count(a) == 2`, decides. That is one O(n) scan and O(1) space.
- XOR swap: `a ^= b; b ^= a; a ^= b` swaps two ints without a temporary. In Python you write `a, b = b, a`: it is clearer, works for any type, and needs no trick. The XOR swap breaks when both names refer to the same slot: `lst[i] ^= lst[j]` with `i == j` makes the slot 0 (a ^ a = 0), and the value is lost. (Two separate variables that merely hold equal numbers swap fine.)

**Complexity:** Time O(n): one pass for `x`, one for the groups, one `count`. Space O(1). Input values and indices are at most 10^5, so no masking is needed; all values are positive.

**Dry run:** `nums = [1, 3, 3, 4]`, n = 4. `x` = (1^1) ^ (2^3) ^ (3^3) ^ (4^4) = 2 ^ 3 = 1 (binary `1`), so `low = 1` (the program prints `x`).
- Bit-set group (odd): numbers `1, 3, 3`, indices `1, 3`: 1 ^ 3 ^ 3 ^ 1 ^ 3 = 3.
- Bit-clear group (even): numbers `4`, indices `2, 4`: 4 ^ 2 ^ 4 = 2.
- `nums.count(3) == 2`, so the duplicate is 3 and the missing value is 2: `[3, 2]`.

**Code:**
```python
import collections
import random

random.seed(1215)

def dup_missing(nums):
    n = len(nums)
    x = 0
    for i, v in enumerate(nums, 1):          # x = dup ^ missing: every value that is both present and in 1..n cancels
        x ^= i ^ v
    low = x & -x                              # a bit where dup and missing differ (x != 0 because dup != missing)
    a = b = 0
    for i, v in enumerate(nums, 1):
        if i & low: a ^= i
        else: b ^= i
        if v & low: a ^= v
        else: b ^= v
    # a and b are {dup, missing} in some order; one more O(n) pass tells which is which
    return [a, b] if nums.count(a) == 2 else [b, a]

def brute(nums):
    c = collections.Counter(nums)
    return [[k for k, v in c.items() if v == 2][0], [i for i in range(1, len(nums) + 1) if i not in c][0]]

for nums, want in [([1, 3, 3, 4], [3, 2]), ([2, 2], [2, 1]), ([1, 1, 3, 4, 5], [1, 2]), ([3, 1, 2, 5, 5], [5, 4])]:
    assert dup_missing(nums) == brute(nums) == want, nums
print("4 prompt examples ok")

# dry run [1, 3, 3, 4]
nums = [1, 3, 3, 4]
x = 0
for i, v in enumerate(nums, 1): x ^= i ^ v
low = x & -x
print("dry run [1,3,3,4]: x = dup ^ missing =", x, bin(x), "| low bit =", low)
print("  group with bit set   : numbers", [v for v in nums if v & low], "indices", [i for i in range(1, 5) if i & low])
print("  group with bit clear : numbers", [v for v in nums if not v & low], "indices", [i for i in range(1, 5) if not i & low])
print("  results:", dup_missing(nums), "(duplicate, missing)")

for _ in range(500):
    n = random.randint(2, 12)
    dup, miss = random.sample(range(1, n + 1), 2)
    nums = [v for v in range(1, n + 1) if v != miss] + [dup]
    random.shuffle(nums)
    assert dup_missing(nums) == brute(nums) == [dup, miss], nums
print("500 seeded random cases agree with Counter + membership scan")
# every possible (dup, missing) pair for n = 2..7, exhaustively
for n in range(2, 8):
    for dup in range(1, n + 1):
        for miss in range(1, n + 1):
            if dup == miss: continue
            nums = [v for v in range(1, n + 1) if v != miss] + [dup]
            assert dup_missing(nums) == [dup, miss]
print("exhaustive: every (duplicate, missing) pair for n = 2..7 correct")

# XOR swap
a, b = 5, 9
a ^= b; b ^= a; a ^= b
assert (a, b) == (9, 5)
lst = [4, 7]
i = j = 0                                     # both names point at the same slot
lst[i] ^= lst[j]; lst[j] ^= lst[i]; lst[i] ^= lst[j]
print("XOR swap on 5, 9 ->", (a, b), "| same slot [4, 7] with i == j ->", lst, "(slot zeroed, value lost)")
assert lst == [0, 7]
# edge asserts
assert dup_missing([2, 2]) == [2, 1]
assert dup_missing([1, 1]) == [1, 2]
assert dup_missing([2, 3, 3]) == [3, 1]
n = 10 ** 5
big = list(range(1, n + 1)); big[-1] = 1                  # drop n, duplicate 1
assert dup_missing(big) == [1, n]
print("edge asserts ok (including n = 10^5)")
```

**Output (my run):**
```text
4 prompt examples ok
dry run [1,3,3,4]: x = dup ^ missing = 1 0b1 | low bit = 1
  group with bit set   : numbers [1, 3, 3] indices [1, 3]
  group with bit clear : numbers [4] indices [2, 4]
  results: [3, 2] (duplicate, missing)
500 seeded random cases agree with Counter + membership scan
exhaustive: every (duplicate, missing) pair for n = 2..7 correct
XOR swap on 5, 9 -> (9, 5) | same slot [4, 7] with i == j -> [0, 7] (slot zeroed, value lost)
edge asserts ok (including n = 10^5)
```

**Edge cases:**
- n = 2, `[2, 2]` gives `[2, 1]`; `[1, 1]` gives `[1, 2]`.
- Missing value is n: the largest index only appears once.
- Duplicate is 1 and missing is n at n = 10^5: checked.
- Do not rely on the sum trick for both numbers at once (it gives only two equations; sum and sum of squares works but can get large; XOR avoids that).

**Follow-ups:**
- *Why not in-place sign marking?* It also gives O(1) space but it mutates (or temporarily corrupts) the input; XOR leaves it untouched.
- *Single missing number?* XOR of all values and indices, or the sum formula; see Part 1 Q8 for the hash-set, sort and sum versions.
- *Three differing values?* XOR alone is not enough; use counting or sorting.

**Common mistakes:**
- Forgetting to XOR in the indices 1..n (then the missing value is not in the XOR).
- Reporting `[a, b]` without the final check and getting the pair the wrong way round half the time.
- Using the XOR swap on two list slots that may be the same slot.
- Computing `x & -x` and then comparing with `== 1` instead of testing `value & low`.

---

### Q16 ⭐⭐ 🟡 Single number III. `nums` has 2 <= len <= 10^5 integers (any sign, |value| < 2^31): exactly two values appear once and every other value appears exactly twice. Return the two single values as a list sorted ascending. Use O(n) time and O(1) extra space: XOR everything to get `a ^ b`, isolate one bit in which they differ with `x & -x`, and XOR separately the numbers that have that bit. Show that `x & -x` also works for a NEGATIVE `x` in Python (integers behave as two's complement with infinitely many sign bits; the result is the lowest set bit), and give a small case where `a ^ b` is negative. In the answer include a dry run on the first example and a seeded random cross-check of your solution against a Counter on small inputs. Example: nums=[4, 9, 4, -6, 2, 9] -> [-6, 2]; nums=[1, 2] -> [1, 2]; nums=[-1, 1, 3, 3] -> [-1, 1]; nums=[0, 5, 0, 7, 7, -2] -> [-2, 5].
**Asked at:** Bit manipulation question lists (Techie Delight bit-manipulation list, Interview Cake, a Devinterview GitHub list, Interview Kickstart; search snippets only, not opened)

**Pattern:** XOR cancellation plus partition by a differing bit; the lowest set bit via `x & -x`.

**Say this first (1 line):** "XOR everything to get `a ^ b`; it is non-zero, so take its lowest set bit `x & -x`; numbers with that bit set go to one group, the rest to the other; pairs stay together and cancel, each group leaves one single."

**Brute force:** `Counter` and keep the two keys with count 1: O(n) time, O(n) space. Sorting also works but is O(n log n).

**Optimal:**
- XOR of all numbers: pairs cancel (`a ^ a = 0`), leaving `x = a ^ b` where `a` and `b` are the singles. `a != b` so `x != 0`.
- Pick any set bit of `x`, here the lowest, `low = x & -x`. At that bit `a` and `b` differ.
- Split by `v & low`. Two equal numbers have the same bit, so each pair lands in the same group and cancels there. `a` and `b` land in different groups.
- XOR the group with the bit set to get one single, `a`. The other is `x ^ a`. Sort the pair for the required output order.
- `x & -x` for a NEGATIVE `x` in Python 3.13 (observed): Python integers behave as two's complement with infinitely many sign bits, and `-x == ~x + 1`. Above the lowest set bit `-x` is the complement of `x`, at and below it they agree, so the AND keeps only the lowest set bit. The output shows `-12 & 12`, i.e. `x & -x` is 4 for both 12 and -12, and a loop over every non-zero x in [-2000, 2000] confirms the result is a positive power of two equal to the lowest set bit.
- Small case with a negative `a ^ b`: in `[4, 9, 4, -6, 2, 9]` the singles -6 and 2 give `-6 ^ 2 = -8`; in `[-1, 1, 3, 3]` the singles give `-1 ^ 1 = -2`. Python needs no masking here: values are below 2^31 in absolute value, so the XOR of two of them stays in the signed 32-bit range, and `x & -x` is exact.

**Complexity:** Time O(n) (two passes). Space O(1). No hash table.

**Dry run:** `nums = [4, 9, 4, -6, 2, 9]`. XOR of all: 4^9^4^(-6)^2^9 = (-6) ^ 2 = -8 (`...11111000`). `low = -8 & 8 = 8`. Numbers with bit 8 set: 9, -6, 9 (-6 is `...11111010`, bit 3 is 1): XOR = -6. Numbers with it clear: 4, 4, 2: XOR = 2. Answer sorted: `[-6, 2]`.

**Code:**
```python
import collections
import functools
import random

random.seed(1216)

def single_number_iii(nums):
    x = 0
    for v in nums:
        x ^= v                                # x = a ^ b: all pairs cancel
    low = x & -x                              # lowest set bit of x; x != 0 because a != b
    a = 0
    for v in nums:
        if v & low:                           # group 1: numbers with that bit set (a pair always lands in one group together)
            a ^= v
    return sorted([a, x ^ a])

def brute(nums):
    return sorted(k for k, v in collections.Counter(nums).items() if v == 1)

for nums, want in [([4, 9, 4, -6, 2, 9], [-6, 2]), ([1, 2], [1, 2]), ([-1, 1, 3, 3], [-1, 1]), ([0, 5, 0, 7, 7, -2], [-2, 5])]:
    assert single_number_iii(nums) == brute(nums) == want, nums
print("4 prompt examples ok")

# dry run [4, 9, 4, -6, 2, 9]
nums = [4, 9, 4, -6, 2, 9]
x = 0
for v in nums: x ^= v
low = x & -x
print("dry run:", nums)
print("  x = a ^ b =", x, "(-6 ^ 2) | low = x & -x =", low, bin(low))
print("  numbers with that bit set  :", [v for v in nums if v & low], "-> XOR =", functools.reduce(lambda p, q: p ^ q, [v for v in nums if v & low]))
print("  numbers with that bit clear:", [v for v in nums if not v & low], "-> XOR =", functools.reduce(lambda p, q: p ^ q, [v for v in nums if not v & low]))
print("  answer:", single_number_iii(nums))

# Python 3.13 behaviour with negatives, as observed
print("--- negatives in Python 3.13 (observed) ---")
for v in (12, -12, -2, -1, -8):
    print("x = %3d  -x = %3d  x & -x = %2d  ~x + 1 = %3d  bin(x & -x) = %s" % (v, -v, v & -v, ~v + 1, bin(v & -v)))
print("-6 ^ 2 =", -6 ^ 2, "(a negative XOR: the two singles have different signs, so the sign 'bit' differs)")
print("-1 ^ 1 =", -1 ^ 1, "| (-1 ^ 1) & -(-1 ^ 1) =", (-1 ^ 1) & -(-1 ^ 1))
for v in range(-2000, 2001):
    if v:
        low = v & -v
        assert low > 0 and low & (low - 1) == 0 and v & (low - 1) == 0 and v & low        # power of two, and the lowest set bit of v
print("x & -x is the lowest set bit (a positive power of two) for every nonzero x in [-2000, 2000]")

# seeded random cross-check, values of both signs up to 2^31
for _ in range(500):
    k = random.randint(2, 7)
    vals = random.sample(range(-2 ** 31 + 1, 2 ** 31), k)
    singles, pairs = vals[:2], vals[2:]
    nums = singles + [p for p in pairs for _ in range(2)]
    random.shuffle(nums)
    assert single_number_iii(nums) == brute(nums) == sorted(singles), nums
print("500 seeded random cases (values of both signs) agree with Counter")
# exhaustive: every pair of distinct singles in -4..4 with one extra pair value
for a in range(-4, 5):
    for b in range(-4, 5):
        if a >= b: continue
        for p in range(-4, 5):
            if p in (a, b): continue
            assert single_number_iii([p, a, p, b]) == [a, b]
print("exhaustive small values ok")
# edge asserts
assert single_number_iii([0, 1]) == [0, 1]
assert single_number_iii([-2 ** 31 + 1, 2 ** 31 - 1]) == [-2 ** 31 + 1, 2 ** 31 - 1]
big = [1, 2] + [v for v in range(3, 50003) for _ in range(2)]
assert single_number_iii(big) == [1, 2]
print("edge asserts ok (including 10^5 numbers)")
```

**Output (my run):**
```text
4 prompt examples ok
dry run: [4, 9, 4, -6, 2, 9]
  x = a ^ b = -8 (-6 ^ 2) | low = x & -x = 8 0b1000
  numbers with that bit set  : [9, -6, 9] -> XOR = -6
  numbers with that bit clear: [4, 4, 2] -> XOR = 2
  answer: [-6, 2]
--- negatives in Python 3.13 (observed) ---
x =  12  -x = -12  x & -x =  4  ~x + 1 = -12  bin(x & -x) = 0b100
x = -12  -x =  12  x & -x =  4  ~x + 1 =  12  bin(x & -x) = 0b100
x =  -2  -x =   2  x & -x =  2  ~x + 1 =   2  bin(x & -x) = 0b10
x =  -1  -x =   1  x & -x =  1  ~x + 1 =   1  bin(x & -x) = 0b1
x =  -8  -x =   8  x & -x =  8  ~x + 1 =   8  bin(x & -x) = 0b1000
-6 ^ 2 = -8 (a negative XOR: the two singles have different signs, so the sign 'bit' differs)
-1 ^ 1 = -2 | (-1 ^ 1) & -(-1 ^ 1) = 2
x & -x is the lowest set bit (a positive power of two) for every nonzero x in [-2000, 2000]
500 seeded random cases (values of both signs) agree with Counter
exhaustive small values ok
edge asserts ok (including 10^5 numbers)
```

**Edge cases:**
- `[1, 2]`: no pairs at all; the answer is the sorted pair.
- A single equal to 0: `[0, 1]`; the XOR is non-zero because the singles differ.
- Singles of opposite sign: `a ^ b` is negative; works unchanged.
- Extremes `-2^31 + 1` and `2^31 - 1`: checked, as is a 10^5-element input.

**Follow-ups:**
- *Why does the lowest bit work and not any bit?* Any set bit of `x` works. The lowest is convenient: `x & -x`.
- *Every other number three times and one single?* Q28: count bits modulo 3.
- *In a fixed-width language?* `x & -x` can overflow for `INT_MIN` in C; Python has no such case.

**Common mistakes:**
- Splitting by `v > something` instead of by a bit.
- Forgetting to sort the pair when the order is specified.
- Believing `x & -x` fails for negatives in Python; it does not, as shown.
- Writing the lowest-bit trick as `x & ~x + 1` and being surprised: `+` binds tighter than `&`, so it parses as `x & ((~x) + 1)`, which equals `x & -x`. Fine, but write `x & -x`.

---

### Q17 ⭐⭐ 🟡 Reverse bits of a 32-bit integer. `n` is an integer with -2^31 <= n < 2^32. Treat it as a 32-bit pattern (a negative `n` is read as its two's-complement pattern, so -1 is 32 ones and -2^31 is a one followed by 31 zeros), reverse the order of the 32 bits and return the result as a non-negative integer in 0..2^32 - 1. Python integers have no fixed width, so mask explicitly with `n & 0xFFFFFFFF` before looping and explain what goes wrong without the mask (a negative n never becomes 0 under `n >>= 1`; it stays -1, so a loop that waits for zero never ends). Give the 32-step loop, and the divide-and-conquer version that swaps halves with masks (16, 8, 4, 2, 1 bit groups) in five steps. In the answer include a dry run on the first example and a seeded random cross-check of your solution against reversing the 32-character binary string on small inputs. Example: n=1 -> 2147483648; n=6 -> 1610612736; n=-1 -> 4294967295; n=-2147483648 -> 1; n=0 -> 0; n=4294967295 -> 4294967295.
**Asked at:** Bit manipulation question lists (Techie Delight bit-manipulation list, Interview Cake, a Devinterview GitHub list, Interview Kickstart; search snippets only, not opened) | Python integer documentation (docs.python.org fetch failed, not opened; behaviour verified by running Python 3.13; the version in which int.bit_count appeared is editor knowledge, not checked against a page)

**Pattern:** Bit manipulation with an explicit 32-bit mask (Python has no fixed width).

**Say this first (1 line):** "Mask to 32 bits first, `n & 0xFFFFFFFF`, then 32 times: shift the result left, append the lowest bit of `n`, shift `n` right. The mask matters because Python's negative integers never reach 0 under `>>`."

**Brute force:** Format as a 32-character binary string with `format(n & 0xFFFFFFFF, '032b')`, reverse it, parse with `int(s, 2)`. Correct and short (my oracle), but it builds strings; interviewers usually want the bit loop.

**Optimal:**
- Loop version: `n &= M32`; repeat 32 times `r = (r << 1) | (n & 1); n >>= 1`. Fixed 32 rounds, so leading zeros of `n` become trailing zeros of the result, as the problem wants.
- Mask, Python 3.13 as observed: `-1 & 0xFFFFFFFF` is 4294967295 and `-2147483648 & 0xFFFFFFFF` is 2147483648, i.e. the two's-complement 32-bit pattern as a non-negative number. That also gives the required reading of negative inputs.
- Without the mask: `-1 >> 1` is -1, and `-1 >> 100` is -1. Every negative number ends at -1 under repeated `>>=` and never reaches 0 (the code checks every n in [-3000, -1]), so a loop `while n:` never ends. A fixed 32-round loop with no mask does still stop and, observed, gives the right answer for negatives (`n & 1` and `>>` are arithmetic on the infinite two's-complement form), but it hides the fact that you rely on that; the mask makes the 32-bit reading explicit, and the five-step version needs it for real.
- Divide and conquer in five steps (swap 16-bit halves, then bytes, nibbles, bit pairs, single bits): `((n >> 16) | (n << 16)) & M32`, then `((n & 0xFF00FF00) >> 8) | ((n & 0x00FF00FF) << 8)`, then the same with `0xF0F0F0F0 / 0x0F0F0F0F` and shift 4, `0xCCCCCCCC / 0x33333333` and shift 2, `0xAAAAAAAA / 0x55555555` and shift 1. The first step needs the `& M32` because `n << 16` grows past 32 bits in Python (no overflow); the later steps stay inside 32 bits by construction.
- Result is always in 0..2^32 - 1, a non-negative int. Reversing twice returns the masked pattern (checked on 500 random values).

**Complexity:** Time O(32) = O(1) for the loop, 5 steps for the mask version. Space O(1).

**Dry run:** `n = 6` = `00000000000000000000000000000110`. The loop reads bits 0, 1, 2, ... = 0, 1, 1, 0, 0, ... and pushes them in front-first, so the result is `01100000000000000000000000000000` = 1610612736. Mask version, hex after each step: `00060000`, `06000000`, `60000000`, `90000000`, `60000000` = 1610612736.

**Code:**
```python
import random

random.seed(1217)
M32 = 0xFFFFFFFF

def reverse_loop(n):
    n &= M32                                  # read the 32-bit two's-complement pattern; makes n non-negative
    r = 0
    for _ in range(32):
        r = (r << 1) | (n & 1)                # append the lowest bit of n to r
        n >>= 1
    return r

def reverse_dc(n):
    n &= M32
    n = ((n >> 16) | (n << 16)) & M32                                   # swap 16-bit halves (mask: << 16 grows past 32 bits)
    n = ((n & 0xFF00FF00) >> 8) | ((n & 0x00FF00FF) << 8)               # swap bytes in each half
    n = ((n & 0xF0F0F0F0) >> 4) | ((n & 0x0F0F0F0F) << 4)               # swap nibbles
    n = ((n & 0xCCCCCCCC) >> 2) | ((n & 0x33333333) << 2)               # swap bit pairs
    n = ((n & 0xAAAAAAAA) >> 1) | ((n & 0x55555555) << 1)               # swap adjacent bits
    return n

def brute(n):
    return int(format(n & M32, '032b')[::-1], 2)

for n, want in [(1, 2147483648), (6, 1610612736), (-1, 4294967295), (-2147483648, 1), (0, 0), (4294967295, 4294967295)]:
    assert reverse_loop(n) == reverse_dc(n) == brute(n) == want, n
print("6 prompt examples ok")

print("dry run n=6 as 32 bits:", format(6, '032b'))
print("  reversed             :", format(reverse_loop(6), '032b'), "=", reverse_loop(6))
print("divide-and-conquer on n=6, value after each of the five steps (32-bit hex):")
n = 6 & M32
steps = []
n = ((n >> 16) | (n << 16)) & M32; steps.append(n)
n = ((n & 0xFF00FF00) >> 8) | ((n & 0x00FF00FF) << 8); steps.append(n)
n = ((n & 0xF0F0F0F0) >> 4) | ((n & 0x0F0F0F0F) << 4); steps.append(n)
n = ((n & 0xCCCCCCCC) >> 2) | ((n & 0x33333333) << 2); steps.append(n)
n = ((n & 0xAAAAAAAA) >> 1) | ((n & 0x55555555) << 1); steps.append(n)
print("  ", ["%08x" % s for s in steps], "-> final", n)
assert n == 1610612736

# Python 3.13 behaviour without the mask (observed)
print("--- why the mask (Python 3.13, observed) ---")
print("-1 >> 1 =", -1 >> 1, "| -1 >> 100 =", -1 >> 100, "| -2147483648 >> 40 =", -2147483648 >> 40)
def reverse_no_mask_while(n, cap=40):
    steps = 0
    while n and steps < cap:                  # 'while n:' style loop on a negative n; capped so this demo stops
        n >>= 1; steps += 1
    return steps
print("loop 'while n: n >>= 1' on n=-1 stopped only because of the cap of 40 steps; after the cap n is still", end=' ')
m = -1
for _ in range(40): m >>= 1
print(m)
print("without the mask, -1 << 16 =", -1 << 16, "(no 32-bit wrap) ; with the mask, (-1 << 16) & 0xFFFFFFFF =", (-1 << 16) & M32)
print("-1 & 0xFFFFFFFF =", -1 & M32, "| -2147483648 & 0xFFFFFFFF =", -2147483648 & M32)

for n in range(-3000, 0):
    m = n
    for _ in range(64): m >>= 1
    assert m == -1                              # every negative n ends at -1, never at 0
print("every negative n in [-3000, -1] is -1 after 64 shifts: a 'while n' loop would never end")
def reverse_loop_nomask(n):
    r = 0
    for _ in range(32):
        r = (r << 1) | (n & 1); n >>= 1
    return r
assert all(reverse_loop_nomask(n) == brute(n) for n in range(-5000, 5000))
print("a fixed 32-round loop with no mask also gives the right answer on [-5000, 5000] (n & 1 and >> are arithmetic); the mask makes it explicit")
# seeded random + exhaustive-style checks
for _ in range(2000):
    n = random.choice([random.randint(-2 ** 31, 2 ** 32 - 1), random.randint(-8, 8), 1 << random.randint(0, 31)])
    assert reverse_loop(n) == reverse_dc(n) == brute(n), n
print("2000 seeded random values agree with the string-reversal oracle")
for n in range(-3000, 3001):
    assert reverse_loop(n) == reverse_dc(n) == brute(n)
for n in range(0, 2 ** 32, 2 ** 32 // 1000 + 1):
    assert reverse_loop(n) == reverse_dc(n) == brute(n)
print("exhaustive window [-3000, 3000] and a 1000-point sweep of 0..2^32 agree")
# involution and range
for _ in range(500):
    n = random.randint(0, M32)
    assert reverse_loop(reverse_loop(n)) == n and 0 <= reverse_loop(n) <= M32
print("reversing twice gives the original pattern (500 random), result always in 0..2^32-1")
# edge asserts
assert reverse_loop(2 ** 31) == 1 and reverse_loop(0) == 0 and reverse_dc(-1) == M32
assert reverse_loop(-2 ** 31) == 1
print("edge asserts ok")
```

**Output (my run):**
```text
6 prompt examples ok
dry run n=6 as 32 bits: 00000000000000000000000000000110
  reversed             : 01100000000000000000000000000000 = 1610612736
divide-and-conquer on n=6, value after each of the five steps (32-bit hex):
   ['00060000', '06000000', '60000000', '90000000', '60000000'] -> final 1610612736
--- why the mask (Python 3.13, observed) ---
-1 >> 1 = -1 | -1 >> 100 = -1 | -2147483648 >> 40 = -1
loop 'while n: n >>= 1' on n=-1 stopped only because of the cap of 40 steps; after the cap n is still -1
without the mask, -1 << 16 = -65536 (no 32-bit wrap) ; with the mask, (-1 << 16) & 0xFFFFFFFF = 4294901760
-1 & 0xFFFFFFFF = 4294967295 | -2147483648 & 0xFFFFFFFF = 2147483648
every negative n in [-3000, -1] is -1 after 64 shifts: a 'while n' loop would never end
a fixed 32-round loop with no mask also gives the right answer on [-5000, 5000] (n & 1 and >> are arithmetic); the mask makes it explicit
2000 seeded random values agree with the string-reversal oracle
exhaustive window [-3000, 3000] and a 1000-point sweep of 0..2^32 agree
reversing twice gives the original pattern (500 random), result always in 0..2^32-1
edge asserts ok
```

**Edge cases:**
- `n = -1` reads as 32 ones: result 4294967295.
- `n = -2147483648` reads as `1` followed by 31 zeros: result 1.
- `n = 0` gives 0; `n = 4294967295` gives itself.
- `n = 1` gives 2^31 = 2147483648, which is NOT a negative number here: the answer is unsigned.

**Follow-ups:**
- *Called millions of times?* Precompute the reversal of every byte (256 entries) and combine four lookups with shifts.
- *Reverse only the used bits (not 32)?* Use `n.bit_length()` rounds; that is a different question.
- *Return a signed 32-bit result?* Convert: `r - (1 << 32) if r >= 1 << 31 else r`.

**Common mistakes:**
- No mask on a negative input with a `while n:` loop (never ends), or with the five-step version (wider than 32 bits).
- Stopping the loop when `n == 0`: the trailing zeros must still be shifted in. 32 rounds always.
- Forgetting `& M32` after `n << 16` in the mask version.
- Treating the output as signed.

---

### Q18 ⭐⭐ 🟡 Subsets with duplicates. `nums` has 0 <= len <= 10 integers and may repeat values. Return every DISTINCT subset (as a multiset: [1, 2] and [2, 1] are the same subset, and two subsets with the same values are the same subset) once. Each subset is a list in ascending order and the outer list is sorted ascending with Python's list comparison; `nums = []` returns `[[]]`. Sort first and skip a value equal to its left neighbour when it is at the same recursion level (`i > start and a[i] == a[i-1]`); explain why the skip must test `i > start` and not `i > 0`, with a small case where `i > 0` loses a subset. The distinct-values version is Q4. Recursion depth is at most the input size limit stated above (far below CPython's default recursion limit of 1000), so a recursive solution is fine. In the answer include a dry run on the first example and a seeded random cross-check of your solution against the set of sorted tuples from a bitmask loop on small inputs. Example: nums=[3, 1, 3] -> [[], [1], [1, 3], [1, 3, 3], [3], [3, 3]]; nums=[] -> [[]]; nums=[2, 2, 2] -> [[], [2], [2, 2], [2, 2, 2]]; nums=[1, 2, 2, 1] -> [[], [1], [1, 1], [1, 1, 2], [1, 1, 2, 2], [1, 2], [1, 2, 2], [2], [2, 2]].
**Asked at:** Backtracking pattern guides and lists (techinterview.org backtracking and recursion patterns posts, designgurus backtracking interview questions, a DEV Community backtracking-patterns post; search snippets only, not opened)

**Pattern:** Backtracking with a start index (subsets) and a sort-then-skip rule for duplicates.

**Say this first (1 line):** "Sort, then loop from `start`; every call is one answer; skip `a[i]` when `i > start` and it equals `a[i - 1]`, because that value was already tried as the next pick at this level."

**Brute force:** Enumerate all 2^n bitmasks, build each subset of the sorted input as a tuple, put them in a set to drop repeats, then sort. Correct (my oracle) but always does 2^n work even when there are few distinct subsets: `[2, 2, 2, 2, 2, 2]` has only 7 distinct subsets and 64 masks.

**Optimal:**
- Sort a copy of `nums` so equal values are neighbours and each subset comes out in ascending order.
- `go(start)`: append a copy of `cur` (every node of the tree is an answer), then for `i` in `start..n-1` add `a[i]`, recurse with `i + 1`, remove it.
- Skip rule: `if i > start and a[i] == a[i - 1]: continue`. At one level of the tree the loop chooses "which value is the next element". Picking the second `2` after the first `2` at the same level would just produce the same set again.
- Why `i > start` and not `i > 0`: when `i == start`, `a[i - 1]` is the element already chosen at the PARENT level (it is in `cur`), so using an equal `a[i]` is allowed and is how `[2, 2]` is built. `i > 0` wrongly skips it. On `[1, 2, 2]` it loses `[1, 2, 2]` and `[2, 2]`, and on 300 seeded random inputs it is wrong 178 times (output below).
- Output order: the DFS visits a node before its children and siblings in ascending order, which is exactly Python's list comparison order (a prefix comes before its extensions). The code asserts the raw list is already sorted. `nums = []` returns `[[]]`.
- Recursion depth is at most 10 (the number of elements), far below 1000.
- The distinct-values version is Q4.

**Complexity:** Time O(n * D) where D is the number of distinct subsets (each is copied, up to n items): at most O(n * 2^n), about 10 * 1024 steps for n = 10. D equals the product over distinct values of (count + 1); the code checks it. Space O(n) recursion plus the output. Node visits: the skip version makes exactly D calls (one per answer, no wasted calls); the no-skip version makes 2^n calls and dedupes at the end.

**Dry run:** `[1, 2, 2]`, tree (each line is a call and an answer):
```
[]
  [1]
    [1, 2]
      [1, 2, 2]
    skip index 2 (second 2 at this level)
  [2]
    [2, 2]
  skip index 2 (second 2 at this level)
```
6 calls, 6 subsets. Without the skip there would be 8 calls and `[1, 2]` and `[2]` would appear twice. For `[3, 1, 3]` the sorted input is `[1, 3, 3]` and the answer is `[[], [1], [1, 3], [1, 3, 3], [3], [3, 3]]`.

**Code:**
```python
import random

random.seed(1218)

def subsets_dup(nums, stats=None):
    """Sort, then loop from `start`; skip a value equal to its left neighbour at the SAME level (i > start)."""
    a = sorted(nums)
    out, cur = [], []
    calls = 0
    def go(start):
        nonlocal calls
        calls += 1
        out.append(cur[:])                      # every node of this tree is one answer
        for i in range(start, len(a)):
            if i > start and a[i] == a[i - 1]:
                continue                        # same value already tried as the next element at this level
            cur.append(a[i]); go(i + 1); cur.pop()
    go(0)
    if stats is not None: stats.append(calls)
    assert out == sorted(out)                   # the DFS preorder is already the required order (prefix before extension, siblings ascending)
    return out

def subsets_no_skip(nums):
    """Same tree without the skip: 2^n calls, then dedupe at the end. Shows the waste."""
    a = sorted(nums)
    out, cur = [], []
    calls = 0
    def go(start):
        nonlocal calls
        calls += 1
        out.append(tuple(cur))
        for i in range(start, len(a)):
            cur.append(a[i]); go(i + 1); cur.pop()
    go(0)
    return sorted(map(list, set(out))), calls

def subsets_wrong_skip(nums):
    """WRONG on purpose: i > 0 instead of i > start."""
    a = sorted(nums)
    out, cur = [], []
    def go(start):
        out.append(cur[:])
        for i in range(start, len(a)):
            if i > 0 and a[i] == a[i - 1]:
                continue
            cur.append(a[i]); go(i + 1); cur.pop()
    go(0)
    return sorted(out)

def brute(nums):
    n = len(nums)
    return sorted(map(list, {tuple(sorted(nums[i] for i in range(n) if m >> i & 1)) for m in range(1 << n)}))

for nums, want in [([3, 1, 3], [[], [1], [1, 3], [1, 3, 3], [3], [3, 3]]), ([], [[]]),
                   ([2, 2, 2], [[], [2], [2, 2], [2, 2, 2]]),
                   ([1, 2, 2, 1], [[], [1], [1, 1], [1, 1, 2], [1, 1, 2, 2], [1, 2], [1, 2, 2], [2], [2, 2]])]:
    assert subsets_dup(nums) == brute(nums) == want, nums
print("4 prompt examples ok")

# decision tree on [1, 2, 2]
print("--- decision tree for [1, 2, 2] (a node = a call = one answer) ---")
a = [1, 2, 2]
def show(start, cur, depth):
    print("  " * depth + str(cur))
    for i in range(start, len(a)):
        if i > start and a[i] == a[i - 1]:
            print("  " * (depth + 1) + "skip index %d (value %d equals its left neighbour at this level)" % (i, a[i]))
            continue
        show(i + 1, cur + [a[i]], depth + 1)
show(0, [], 0)

# the wrong skip
print("--- i > 0 instead of i > start ---")
good, bad = subsets_dup([1, 2, 2]), subsets_wrong_skip([1, 2, 2])
print("correct:", good)
print("i > 0  :", bad, "| lost:", [s for s in good if s not in bad])
wrong_cases = 0
for _ in range(300):
    nums = [random.randint(1, 3) for _ in range(random.randint(0, 6))]
    if subsets_wrong_skip(nums) != brute(nums): wrong_cases += 1
print("i > 0 wrong on", wrong_cases, "of 300 seeded random inputs")
assert wrong_cases > 0

# node counts
print("--- calls (nodes) ---")
for nums in ([1, 2, 2], [1, 2, 2, 1], [2, 2, 2, 2, 2, 2], [1, 1, 2, 2, 3, 3, 4, 4], list(range(8))):
    st = []
    res = subsets_dup(nums, st)
    _, plain = subsets_no_skip(nums)
    print("%-26s distinct=%3d calls with skip=%3d calls without skip=%3d" % (nums, len(res), st[0], plain))
    assert st[0] == len(res)

# seeded random cross-check
for _ in range(300):
    nums = [random.randint(-3, 3) for _ in range(random.randint(0, 8))]
    assert subsets_dup(nums) == brute(nums) == subsets_no_skip(nums)[0], nums
print("300 seeded random inputs agree with the bitmask-set oracle")
# the count of distinct subsets is the product of (multiplicity + 1)
import collections, math
for _ in range(200):
    nums = [random.randint(1, 4) for _ in range(random.randint(0, 9))]
    assert len(subsets_dup(nums)) == math.prod(c + 1 for c in collections.Counter(nums).values())
print("200 seeded random inputs: number of distinct subsets = product of (multiplicity + 1)")
# edge asserts
assert subsets_dup([]) == [[]]
assert subsets_dup([5]) == [[], [5]]
assert len(subsets_dup(list(range(10)))) == 1024
assert len(subsets_dup([7] * 10)) == 11
x = [3, 1, 3]; subsets_dup(x); assert x == [3, 1, 3]       # input not mutated (we sort a copy)
print("edge asserts ok")
```

**Output (my run):**
```text
4 prompt examples ok
--- decision tree for [1, 2, 2] (a node = a call = one answer) ---
[]
  [1]
    [1, 2]
      [1, 2, 2]
    skip index 2 (value 2 equals its left neighbour at this level)
  [2]
    [2, 2]
  skip index 2 (value 2 equals its left neighbour at this level)
--- i > 0 instead of i > start ---
correct: [[], [1], [1, 2], [1, 2, 2], [2], [2, 2]]
i > 0  : [[], [1], [1, 2], [2]] | lost: [[1, 2, 2], [2, 2]]
i > 0 wrong on 178 of 300 seeded random inputs
--- calls (nodes) ---
[1, 2, 2]                  distinct=  6 calls with skip=  6 calls without skip=  8
[1, 2, 2, 1]               distinct=  9 calls with skip=  9 calls without skip= 16
[2, 2, 2, 2, 2, 2]         distinct=  7 calls with skip=  7 calls without skip= 64
[1, 1, 2, 2, 3, 3, 4, 4]   distinct= 81 calls with skip= 81 calls without skip=256
[0, 1, 2, 3, 4, 5, 6, 7]   distinct=256 calls with skip=256 calls without skip=256
300 seeded random inputs agree with the bitmask-set oracle
200 seeded random inputs: number of distinct subsets = product of (multiplicity + 1)
edge asserts ok
```

**Edge cases:**
- `[]` gives `[[]]`; one element gives `[[], [x]]`.
- All equal (`[2, 2, 2]`): n + 1 subsets.
- All distinct: 2^n subsets, and the skip never fires (256 calls for 8 distinct values, same as without it).
- The input list must not be mutated: sort a copy (checked).

**Follow-ups:**
- *Iterative version?* Start with `[[]]`; for each distinct value with count c, extend every existing subset with 1..c copies. Same output set; sort at the end if the order must match.
- *Permutations with duplicates?* Different skip rule; see Q19 (the skip rule there is about a used array, not a start index).
- *Count only?* Multiply (count + 1) over distinct values; no enumeration needed (the code checks this identity).

**Common mistakes:**
- Using `i > 0` instead of `i > start`.
- Not sorting first, so equal values are not neighbours and the skip does nothing.
- Appending `cur` instead of `cur[:]`, so every answer ends up the same empty list.
- Returning duplicates and "fixing" it with a set of lists (lists are unhashable; convert to tuples) instead of preventing them.

---
