### Q9 ⭐⭐⭐ 🟡 Word search in a grid. `board` is a list of 1 to 6 strings of equal length 1 to 6 (letters), and `word` is a string of 1 to 12 letters. Return True if `word` can be spelled by walking to horizontally or vertically adjacent cells, never using the same cell twice in one spelling. Mark a cell as used while it is on the current path and restore it on the way back (state exactly where the undo goes). Say why the worst case is about R * C * 3^(L-1) and why the check `board[r][c] != word[k]` first prunes almost everything on real inputs. Backtracking depth is at most the word length L <= 12. Q32 revisits this with a word length that no longer fits in the recursion limit. In the answer include a dry run on the first example and a seeded random cross-check of your solution against a recursion that carries the visited cells as an immutable tuple on small inputs. Example: board=['CATS', 'OXAT', 'DOGS'], word='CATS' -> True; board=['CATS', 'OXAT', 'DOGS'], word='TACO' -> True; board=['CATS', 'OXAT', 'DOGS'], word='SAT' -> False; board=['AA'], word='AAA' -> False; board=['Z'], word='Z' -> True.
**Asked at:** Backtracking pattern guides and lists (techinterview.org backtracking and recursion patterns posts, designgurus backtracking interview questions, a DEV Community backtracking-patterns post; search snippets only, not opened)

**Pattern:** Backtracking on a grid (DFS with a visited mark): choose a neighbour, explore, undo the mark.

**Say this first (1 line):** "Try every cell as the start. From a cell, if the letter does not match word[k], stop; if it is the last letter, success; otherwise mark the cell as used, try the four neighbours, and restore the cell after all four have been tried."

**Brute force:** Carry the visited cells as an immutable tuple (copied per step) so nothing needs undoing. Same search, O(L) extra work per step for the tuple. It is the oracle in the cross-check.

**Optimal:**
- Copy the board into lists (strings are immutable), loop over every cell as a start.
- `go(r, c, k)`: if `g[r][c] != word[k]` return False (this also rejects a cell currently marked '#', since the board has only letters). If `k == L - 1` return True. Set `saved = g[r][c]`, mark `g[r][c] = '#'`, try the four neighbours, then restore `g[r][c] = saved`.
- Where the undo goes: after the loop over all four neighbours, and it must run on every way out of the function except the success return (which ends the search; the board is a copy so nothing leaks). If you restore too early, the cell is free while its descendants are still running, and the path can reuse it. If you never restore, other paths see a blocked cell. In the cross-check, the never-restore version gave a wrong answer on 95 of 2000 seeded random boards (boards up to 4 x 4 over 'a','b').
- Why about R * C * 3^(L-1): R * C choices of start, then at most 3 moves per step (one of the four neighbours is the cell you came from, which is marked). Worst case is a board of all 'A' and a word of 'A's ending in a missing letter, where no letter prunes early. On 6 x 6 all 'A' with `'A' * 11 + 'B'` the search made 1,069,612 calls (every attempt counted, including those rejected at once), under the bound 36 * 3^11 = 6,377,292.
- Why the letter check prunes almost everything on real boards: a cell survives a step only if it equals the next letter. On 'CATS/OXAT/DOGS' with 'SAT' the search made 16 calls against 114 for a letter-blind walk of all self-avoiding paths of 3 cells; for 'CATSX' 22 against 472.
- Recursion depth is L <= 12, far below 1000. (Q32 handles a word too long for recursion.)

**Complexity:** Time O(R * C * 3^(L-1)) worst case, typically far less because of the letter check. Space O(L) for the recursion, plus O(R * C) for the board copy (the mark is in place, no visited set). The counts above are calls, not timings.

**Dry run:** `CATS/OXAT/DOGS`, word `TACO`. Start at (0,2) 'T' (matches). Neighbour (1,2) 'A' matches word[1]; its neighbours (2,2) 'G', (1,3) 'T', (1,1) 'X' are not 'C': pruned. Back to (0,2): (0,3) 'S' is not 'A': pruned; (0,1) 'A' matches; (1,1) 'X' is not 'C'; (0,0) 'C' matches word[2]; (1,0) 'O' matches word[3], the last letter: True. The program prints this trace. 'SAT' is False: the S cells (0,3) and (2,3) have neighbours T, T and T, G, so no S touches an A. `['AA']`, `'AAA'` is False: only two cells.

**Code:**
```python
import random

random.seed(1209)

def exists(board, word, stats=None):
    """Grid backtracking. The mark '#' is safe because boards hold letters only."""
    g = [list(r) for r in board]            # strings are immutable: work on a copy
    R, C = len(g), len(g[0])
    if stats is None:
        stats = {}
    stats['calls'] = 0
    def go(r, c, k):
        stats['calls'] += 1
        if g[r][c] != word[k]:              # prune first: wrong letter (or the '#' mark) ends this branch
            return False
        if k == len(word) - 1:
            return True
        saved, g[r][c] = g[r][c], '#'       # choose: mark the cell as on the current path
        found = False
        for dr, dc in ((1, 0), (-1, 0), (0, 1), (0, -1)):
            nr, nc = r + dr, c + dc
            if 0 <= nr < R and 0 <= nc < C and go(nr, nc, k + 1):
                found = True
                break
        g[r][c] = saved                     # undo: restore on EVERY way out, after the neighbours were tried
        return found
    return any(go(r, c, 0) for r in range(R) for c in range(C))

def exists_no_restore(board, word):
    """WRONG on purpose: the cell is marked and never restored."""
    g = [list(r) for r in board]; R, C = len(g), len(g[0])
    def go(r, c, k):
        if g[r][c] != word[k]: return False
        if k == len(word) - 1: return True
        g[r][c] = '#'
        for dr, dc in ((1, 0), (-1, 0), (0, 1), (0, -1)):
            nr, nc = r + dr, c + dc
            if 0 <= nr < R and 0 <= nc < C and go(nr, nc, k + 1): return True
        return False                                # the undo line is missing
    return any(go(r, c, 0) for r in range(R) for c in range(C))

def brute(board, word):
    """Visited cells carried as an immutable tuple; nothing to undo."""
    R, C = len(board), len(board[0])
    def go(r, c, k, seen):
        if board[r][c] != word[k] or (r, c) in seen: return False
        if k == len(word) - 1: return True
        seen = seen + ((r, c),)
        return any(0 <= r + dr < R and 0 <= c + dc < C and go(r + dr, c + dc, k + 1, seen)
                   for dr, dc in ((1, 0), (-1, 0), (0, 1), (0, -1)))
    return any(go(r, c, 0, ()) for r in range(R) for c in range(C))

B0 = ['CATS', 'OXAT', 'DOGS']
examples = [(B0, 'CATS', True), (B0, 'TACO', True), (B0, 'SAT', False), (['AA'], 'AAA', False), (['Z'], 'Z', True)]
for b, w, want in examples:
    assert exists(b, w) == want == brute(b, w)
    print(b, repr(w), '->', exists(b, w))

# decision tree for TACO on B0: starting cells that pass the first-letter check, then the path
def trace(board, word):
    g = [list(r) for r in board]; R, C = len(g), len(g[0])
    def go(r, c, k, d):
        if g[r][c] != word[k]:
            print('  ' * d + f'({r},{c}) {g[r][c]!r} != {word[k]!r}: prune'); return False
        print('  ' * d + f'({r},{c}) {g[r][c]!r} matches word[{k}]')
        if k == len(word) - 1: return True
        g[r][c] = '#'
        for dr, dc in ((1, 0), (-1, 0), (0, 1), (0, -1)):
            nr, nc = r + dr, c + dc
            if 0 <= nr < R and 0 <= nc < C and g[nr][nc] != '#':
                if go(nr, nc, k + 1, d + 1): return True
        g[r][c] = board[r][c]
        return False
    for r in range(R):
        for c in range(C):
            if board[r][c] == word[0]:
                print(f'start ({r},{c})')
                if go(r, c, 0, 1): return True
    return False
print('found:', trace(B0, 'TACO'))

# calls with the first-letter check vs searching every self-avoiding path without any letter pruning
def count_paths(R, C, L):
    """Number of calls if letters are ignored: every self-avoiding walk of up to L cells is expanded."""
    seen = [[False] * C for _ in range(R)]; tot = [0]
    def go(r, c, k):
        tot[0] += 1
        if k == L - 1: return
        seen[r][c] = True
        for dr, dc in ((1, 0), (-1, 0), (0, 1), (0, -1)):
            nr, nc = r + dr, c + dc
            if 0 <= nr < R and 0 <= nc < C and not seen[nr][nc]: go(nr, nc, k + 1)
        seen[r][c] = False
    for r in range(R):
        for c in range(C): go(r, c, 0)
    return tot[0]
st = {}
exists(B0, 'SAT', st); print('SAT on 3x4: pruned calls', st['calls'], ' letter-blind calls', count_paths(3, 4, 3))
exists(B0, 'CATSX', st); print('CATSX on 3x4: pruned calls', st['calls'], ' letter-blind calls', count_paths(3, 4, 5))
# adversarial: all 'A' and a word that ends in a letter that never appears: no letter prunes anything until the very end
st = {}
b6 = ['A' * 6] * 6
assert exists(b6, 'A' * 11 + 'B', st) is False
bound = 36 * 3 ** 11
print('worst-ish 6x6 all A, L=12: calls', st['calls'], ' R*C*3^(L-1) =', bound, ' within bound:', st['calls'] <= bound)

# seeded cross-check, and how often forgetting the undo is wrong
def rand_board():
    C = random.randint(1, 4)
    return [''.join(random.choice('ab') for _ in range(C)) for _ in range(random.randint(1, 4))]
bad = 0
for _ in range(2000):
    b = rand_board(); w = ''.join(random.choice('ab') for _ in range(random.randint(1, 7)))
    r = exists(b, w); assert r == brute(b, w)
    bad += exists_no_restore(b, w) != r
print('random cross-check ok: 2000 cases; no-restore variant wrong on', bad, 'of them')

# edge asserts
assert exists(['A'], 'AA') is False and exists(['AB'], 'BA') is True and exists(['A', 'B'], 'BA') is True
assert exists(['ABA'], 'ABA') is True and exists(['AB'], 'ABA') is False   # no cell reuse
assert exists(['ABCDEF'] * 1, 'F') and exists(['AAAAAA'] * 6, 'A' * 12) is True
print('edge asserts ok')
```

**Output (my run):**
```
['CATS', 'OXAT', 'DOGS'] 'CATS' -> True
['CATS', 'OXAT', 'DOGS'] 'TACO' -> True
['CATS', 'OXAT', 'DOGS'] 'SAT' -> False
['AA'] 'AAA' -> False
['Z'] 'Z' -> True
start (0,2)
  (0,2) 'T' matches word[0]
    (1,2) 'A' matches word[1]
      (2,2) 'G' != 'C': prune
      (1,3) 'T' != 'C': prune
      (1,1) 'X' != 'C': prune
    (0,3) 'S' != 'A': prune
    (0,1) 'A' matches word[1]
      (1,1) 'X' != 'C': prune
      (0,0) 'C' matches word[2]
        (1,0) 'O' matches word[3]
found: True
SAT on 3x4: pruned calls 16  letter-blind calls 114
CATSX on 3x4: pruned calls 22  letter-blind calls 472
worst-ish 6x6 all A, L=12: calls 1069612  R*C*3^(L-1) = 6377292  within bound: True
random cross-check ok: 2000 cases; no-restore variant wrong on 95 of them
edge asserts ok
```

**Edge cases:**
- 1 x 1 board: `['Z']`, 'Z' is True; word longer than the number of cells is False (`['AA']`, 'AAA').
- A path may go in any of the four directions, including up and left.
- No cell reuse in one spelling (`['ABA']` with 'ABA' is True, `['AB']` with 'ABA' is False), but every start cell is a fresh search because the mark is restored.
- All-same-letter boards are the slow case.

**Follow-ups:**
- Many words at once: put the words in a trie and walk it during one DFS (Q11).
- Word longer than the recursion limit: explicit stack (Q32).
- Cheap speed-ups: if the board's letter counts cannot cover the word, answer False; search from the rarer end of the word.

**Common mistakes:**
- Not restoring the cell (or restoring before the neighbours are tried).
- Marking with a character that can occur on the board.
- Checking the bounds after indexing (negative indexes wrap around in Python: `g[-1][c]` silently reads the last row).
- Starting the search from only (0, 0).
