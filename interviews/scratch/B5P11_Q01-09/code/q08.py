import itertools
import random
import sys
from collections import deque
from functools import lru_cache

random.seed(1108)

def edit_table(a, b):
    """dp[i][j] = min edits to turn a[:i] into b[:j]."""
    m, n = len(a), len(b)
    dp = [[0] * (n + 1) for _ in range(m + 1)]
    for i in range(m + 1):
        dp[i][0] = i                              # delete i letters
    for j in range(n + 1):
        dp[0][j] = j                              # insert j letters
    for i in range(1, m + 1):
        for j in range(1, n + 1):
            if a[i - 1] == b[j - 1]:
                dp[i][j] = dp[i - 1][j - 1]
            else:
                dp[i][j] = 1 + min(dp[i - 1][j - 1],   # replace
                                   dp[i - 1][j],       # delete a[i-1]
                                   dp[i][j - 1])       # insert b[j-1]
    return dp

def edit_two_rows(a, b):
    """Two rows over the shorter string (edit distance is symmetric, so swapping is safe)."""
    if len(b) > len(a):
        a, b = b, a
    prev = list(range(len(b) + 1))                # row i = 0
    for i, ca in enumerate(a, 1):
        cur = [i] + [0] * len(b)
        for j, cb in enumerate(b, 1):
            cur[j] = prev[j - 1] if ca == cb else 1 + min(prev[j - 1], prev[j], cur[j - 1])
        prev = cur
    return prev[-1]

def edit_plain(a, b):
    """Oracle: plain recursion on suffixes, no memo."""
    def f(i, j):
        if i == len(a):
            return len(b) - j
        if j == len(b):
            return len(a) - i
        if a[i] == b[j]:
            return f(i + 1, j + 1)
        return 1 + min(f(i + 1, j), f(i, j + 1), f(i + 1, j + 1))
    return f(0, 0)

def edit_memo(a, b):
    @lru_cache(maxsize=None)
    def f(i, j):
        if i == len(a):
            return len(b) - j
        if j == len(b):
            return len(a) - i
        if a[i] == b[j]:
            return f(i + 1, j + 1)
        return 1 + min(f(i + 1, j), f(i, j + 1), f(i + 1, j + 1))
    return f(0, 0)

def edit_bfs(a, b, alpha='ab'):
    """Independent oracle: breadth-first search over strings, one edit per step. Tiny inputs only."""
    seen = {a}
    q = deque([(a, 0)])
    while q:
        s, d = q.popleft()
        if s == b:
            return d
        nxt = set()
        for i in range(len(s) + 1):
            for c in alpha:
                nxt.add(s[:i] + c + s[i:])                    # insert
        for i in range(len(s)):
            nxt.add(s[:i] + s[i + 1:])                        # delete
            for c in alpha:
                nxt.add(s[:i] + c + s[i + 1:])                # replace
        for t in nxt:
            if t not in seen and len(t) <= len(a) + len(b):
                seen.add(t)
                q.append((t, d + 1))

for (a, b), want in [(('horse', 'ros'), 3), (('intention', 'execution'), 5), (('', 'abc'), 3), (('same', 'same'), 0), (('a', 'b'), 1)]:
    assert edit_two_rows(a, b) == edit_table(a, b)[-1][-1] == edit_plain(a, b) == edit_memo(a, b) == want, (a, b)
print("5 prompt examples ok")

a, b = 'horse', 'ros'
print("walk-through a =", a, " b =", b, "(rows = prefixes of a, columns = prefixes of b)")
print("        ", ["''"] + list(b))
for i, r in enumerate(edit_table(a, b)):
    print("  ", ("'" + a[:i] + "'").ljust(8), r)

cnt = 0
for la in range(6):
    for lb in range(6):
        for x in itertools.product('ab', repeat=la):
            for y in itertools.product('ab', repeat=lb):
                x_, y_ = ''.join(x), ''.join(y)
                d = edit_two_rows(x_, y_)
                assert d == edit_plain(x_, y_) == edit_table(x_, y_)[-1][-1] == edit_two_rows(y_, x_), (x_, y_)
                cnt += 1
print("exhaustive over {a,b}, lengths 0..5:", cnt, "pairs: two rows == table == plain recursion; symmetric")
cnt = 0
for la in range(4):
    for lb in range(4):
        for x in itertools.product('ab', repeat=la):
            for y in itertools.product('ab', repeat=lb):
                x_, y_ = ''.join(x), ''.join(y)
                assert edit_bfs(x_, y_) == edit_two_rows(x_, y_), (x_, y_)
                cnt += 1
print("independent BFS over strings (insert/delete/replace one letter per step), lengths 0..3 over {a,b}:", cnt, "pairs agree")
for _ in range(500):
    x = ''.join(random.choice('abcd') for _ in range(random.randint(0, 7)))
    y = ''.join(random.choice('abcd') for _ in range(random.randint(0, 7)))
    assert edit_two_rows(x, y) == edit_plain(x, y) == edit_table(x, y)[-1][-1] == edit_memo(x, y)
    assert abs(len(x) - len(y)) <= edit_two_rows(x, y) <= max(len(x), len(y))   # bounds
print("500 seeded random pairs (len <= 7, alphabet abcd): ok; |len diff| <= dist <= max len holds")

A = ''.join(random.choice('abcdefghijklmnopqrstuvwxyz') for _ in range(1000))
B = ''.join(random.choice('abcdefghijklmnopqrstuvwxyz') for _ in range(1000))
v = edit_two_rows(A, B)
assert v == edit_table(A, B)[-1][-1]
print("1000 x 1000 random letters: distance =", v, "(two rows == full table)")
print("recursion limit:", sys.getrecursionlimit())
def memo_outcome(x, y):
    try:
        return "ok" if edit_memo(x, y) == edit_two_rows(x, y) else "WRONG"
    except RecursionError:
        return "RecursionError"
print("memoised recursion on disjoint strings (a's vs b's, depth about 2n):")
for n in (100, 300, 400, 1000):
    print("   n = %4d each: %s" % (n, memo_outcome('a' * n, 'b' * n)))
print("memoised recursion, 1000 x 1000 random letters:", memo_outcome(A, B))
