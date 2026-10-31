### Q8 ⭐⭐⭐ 🟡 Combination sum with unlimited reuse. `candidates` has 1 <= len <= 8 distinct positive integers (each <= 40) and `target` is 1 <= target <= 40. Return every combination of candidates (each candidate may be used any number of times) that sums to `target`. A combination is a list in non-decreasing order, two combinations that contain the same numbers the same number of times are the same one (list it once), and the outer list is sorted ascending with Python's list comparison. Return an empty list if none exists. Explain the start-index trick that prevents permutations of the same combination (recurse with the same index, not index + 1) and the sort-then-break pruning. Counting instead of listing is the coin-change-II DP of Part 10 Q10. Recursion depth is at most the input size limit stated above (far below CPython's default recursion limit of 1000), so a recursive solution is fine. In the answer include a dry run on the first example and a seeded random cross-check of your solution against itertools.combinations_with_replacement over every length on small inputs. Example: candidates=[3, 4, 5], target=12 -> [[3, 3, 3, 3], [3, 4, 5], [4, 4, 4]]; candidates=[3, 5], target=2 -> []; candidates=[2], target=8 -> [[2, 2, 2, 2]]; candidates=[1], target=3 -> [[1, 1, 1]]; candidates=[7, 2, 4], target=11 -> [[2, 2, 7], [4, 7]].
**Asked at:** Backtracking pattern guides and lists (techinterview.org backtracking and recursion patterns posts, designgurus backtracking interview questions, a DEV Community backtracking-patterns post; search snippets only, not opened)

**Pattern:** Backtracking over combinations with reuse: a start index stops permutations, sorting plus break stops overshoot.

**Say this first (1 line):** "Sort the candidates. Recurse with the remaining sum and a start index. Pick candidate i, then recurse with the same i (reuse is allowed) so order is always non-decreasing and a combination appears once. Break as soon as a candidate exceeds what is left."

**Brute force:** `itertools.combinations_with_replacement` over every length 1..target / min(candidates), keep those that sum to the target. Exponential, and it generates many sums that overshoot. Or the version without a start index that tries every order (compositions) and deduplicates by sorting at the end: for `[1, 2]`, target 12 it makes 753 calls against 49.

**Optimal:**
- `go(start, remain)`: if `remain == 0`, record `cur[:]`. Else for `i` from `start`: if `cs[i] > remain`, break; push `cs[i]`, `go(i, remain - cs[i])`, pop.
- Start-index trick: passing `i` (not `0`, and not `i + 1`) means the next pick is `cs[i]` or a larger candidate. Same index gives reuse; never going back gives each multiset exactly once, in non-decreasing order. Without it `[3, 4, 5]`, 12 would reach `[4, 3, 5]` and `[5, 4, 3]` as well.
- Sort-then-break: the candidates are ascending, so once `cs[i] > remain` every later candidate is too big too: break, not continue. Without the break the code makes a call that returns at once on an overshoot: 28 calls against 17 for `[3, 4, 5]`, target 12 (measured below).
- Recursion depth: the most numbers in one combination is target / min = 40 (candidate 1, target 40), so at most 41 frames: far below 1000 (checked: depth 40 for `[1..8]`, target 40; that case has 9749 answers and 73056 calls).
- Counting instead of listing is the coin-change-II DP (Part 10 Q10).

**Complexity:** Let T be the target and m the smallest candidate. Depth is at most T/m. The number of nodes is bounded by the number of non-decreasing sequences with sum at most T; there is no neat closed form. A loose bound is O(n^(T/m)) calls, each answer costs O(T/m) to copy. Space O(T/m) for the recursion plus the output. I give this as a bound from reasoning, not a tight one; the measured counts show how much the break and the start index cut.

**Dry run:** `[2, 3]`, target 5 (the program prints this tree).
- take 2 (remain 3), take 2 (remain 1): 2 > 1 so break.
- back at remain 3: take 3 (remain 0): answer `[2, 3]`.
- back at the root: take 3 (remain 2): 3 > 2, break.
So one answer `[2, 3]`. For the first example `[3, 4, 5]`, 12: `[3, 3, 3, 3]`, `[3, 4, 5]`, `[4, 4, 4]`.

**Code:**
```python
import itertools
import random

random.seed(1208)

def comb_sum(candidates, target):
    """Sorted candidates, start index, break when too big. Returns (list, calls, max depth)."""
    cs = sorted(candidates)
    out, cur, st = [], [], {'calls': 0, 'depth': 0}
    def go(start, remain):
        st['calls'] += 1
        st['depth'] = max(st['depth'], len(cur))
        if remain == 0:
            out.append(cur[:]); return
        for i in range(start, len(cs)):
            if cs[i] > remain:
                break                       # sorted: every later candidate is too big as well
            cur.append(cs[i])               # choose
            go(i, remain - cs[i])           # explore: SAME index i => reuse allowed, no reordering
            cur.pop()                       # undo
    go(0, target)
    return sorted(out), st['calls'], st['depth']

def comb_sum_no_break(candidates, target):
    """Start index but no break: overshoots are visited and rejected one call later."""
    cs = sorted(candidates); out, cur, calls = [], [], [0]
    def go(start, remain):
        calls[0] += 1
        if remain < 0:
            return
        if remain == 0:
            out.append(cur[:]); return
        for i in range(start, len(cs)):
            cur.append(cs[i]); go(i, remain - cs[i]); cur.pop()
    go(0, target)
    return sorted(out), calls[0]

def comb_sum_ordered(candidates, target):
    """No start index: every ORDER is explored (permutations); dedupe by sorting at the end."""
    cs = sorted(candidates); out, cur, calls = set(), [], [0]
    def go(remain):
        calls[0] += 1
        if remain < 0:
            return
        if remain == 0:
            out.add(tuple(sorted(cur))); return
        for v in cs:
            cur.append(v); go(remain - v); cur.pop()
    go(target)
    return sorted(map(list, out)), calls[0]

def brute(candidates, target):
    out = set()
    for length in range(1, target // min(candidates) + 1):
        for combo in itertools.combinations_with_replacement(sorted(candidates), length):
            if sum(combo) == target:
                out.add(combo)
    return sorted(map(list, out))

examples = [(([3, 4, 5], 12), [[3, 3, 3, 3], [3, 4, 5], [4, 4, 4]]), (([3, 5], 2), []), (([2], 8), [[2, 2, 2, 2]]),
            (([1], 3), [[1, 1, 1]]), (([7, 2, 4], 11), [[2, 2, 7], [4, 7]])]
for (c, t), want in examples:
    assert comb_sum(c, t)[0] == want == brute(c, t) == comb_sum_no_break(c, t)[0] == comb_sum_ordered(c, t)[0]
    print(c, t, '->', comb_sum(c, t)[0])

# decision tree for candidates [2, 3], target 5 (sorted). 'X' = pruned by the break
def tree(cs, start, remain, d, cur):
    if remain == 0:
        print('  ' * d + f'{cur} sum hit: answer'); return
    for i in range(start, len(cs)):
        if cs[i] > remain:
            print('  ' * d + f'{cs[i]} > remain {remain}: break'); break
        print('  ' * d + f'take {cs[i]} (remain {remain - cs[i]}, next index {i})')
        tree(cs, i, remain - cs[i], d + 1, cur + [cs[i]])
tree([2, 3], 0, 5, 0, [])

# calls: break vs no break vs no start index (small cases; the ordered version explodes)
print('case                      answers  break  no-break  ordered')
for c, t in [([3, 4, 5], 12), ([2, 3, 6, 7], 7), ([2, 3, 5], 10), ([1, 2], 12)]:
    a, ca, _ = comb_sum(c, t); b, cb = comb_sum_no_break(c, t); o, co = comb_sum_ordered(c, t)
    assert a == b == o
    print(f'{str(c):12} t={t:<3}        {len(a):7} {ca:6} {cb:9} {co:8}')

# seeded cross-check
for _ in range(1500):
    c = random.sample(range(1, 13), random.randint(1, 5)); t = random.randint(1, 20)
    assert comb_sum(c, t)[0] == brute(c, t)
print('random cross-check ok: 1500 cases')

# edge: depth bound. candidate 1, target 40 -> 40 chosen numbers, 41 frames: far below the recursion limit of 1000
r, calls, depth = comb_sum([1], 40)
assert r == [[1] * 40] and depth == 40
r2, calls2, depth2 = comb_sum([1, 2, 3, 4, 5, 6, 7, 8], 40)
assert depth2 == 40 and all(sum(x) == 40 and x == sorted(x) for x in r2)
print('max depth (chosen numbers):', depth2, ' answers for [1..8], 40:', len(r2), ' calls:', calls2)
assert comb_sum([5], 3)[0] == [] and comb_sum([40], 40)[0] == [[40]]
print('edge asserts ok')
```

**Output (my run):**
```
[3, 4, 5] 12 -> [[3, 3, 3, 3], [3, 4, 5], [4, 4, 4]]
[3, 5] 2 -> []
[2] 8 -> [[2, 2, 2, 2]]
[1] 3 -> [[1, 1, 1]]
[7, 2, 4] 11 -> [[2, 2, 7], [4, 7]]
take 2 (remain 3, next index 0)
  take 2 (remain 1, next index 0)
    2 > remain 1: break
  take 3 (remain 0, next index 1)
    [2, 3] sum hit: answer
take 3 (remain 2, next index 1)
  3 > remain 2: break
case                      answers  break  no-break  ordered
[3, 4, 5]    t=12               3     17        28       70
[2, 3, 6, 7] t=7                2     10        28       37
[2, 3, 5]    t=10               4     20        34       85
[1, 2]       t=12               7     49        55      753
random cross-check ok: 1500 cases
max depth (chosen numbers): 40  answers for [1..8], 40: 9749  calls: 73056
edge asserts ok
```

**Edge cases:**
- No combination: `[3, 5]`, target 2 returns `[]`.
- Candidate equal to target: `[40]`, 40 returns `[[40]]`.
- A candidate larger than the target: skipped by the break.
- Candidate 1 with target 40: depth 40, one answer `[1] * 40`.
- The input need not be sorted (`[7, 2, 4]`): sort first.

**Follow-ups:**
- Each number used once, duplicates in input (Q21): recurse with `i + 1` and skip equal neighbours at the same level.
- Count the ways: DP over coins (Part 10 Q10).
- Fewest numbers: coin change minimum (a DP, not enumeration).

**Common mistakes:**
- Recursing with `0` instead of `i`: you get permutations of the same combination.
- Recursing with `i + 1`: no reuse.
- Using `continue` instead of `break` (correct but slower), or not sorting and then using `break` (wrong answers).
- Appending `cur` instead of a copy.
