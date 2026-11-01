import random
import sys

random.seed(3201)
DIRS = [(0, 1), (1, 0), (0, -1), (-1, 0)]          # right, down, left, up


def exist_iter(board, word, trace=None):
    """Iterative word search. path = list of cells, nxt = next direction index per frame, on_path = set."""
    R, C, L = len(board), len(board[0]), len(word)
    if L > R * C:
        return False
    for sr in range(R):
        for sc in range(C):
            if board[sr][sc] != word[0]:
                continue
            path, nxt, on_path = [(sr, sc)], [0], {(sr, sc)}
            if trace is not None:
                trace.append(f"start {path[0]}")
            while path:
                if len(path) == L:
                    return True
                r, c = path[-1]
                d = nxt[-1]
                if d == 4:                           # all four directions tried: undo this cell
                    path.pop()
                    nxt.pop()
                    on_path.discard((r, c))
                    if trace is not None:
                        trace.append(f"pop {(r, c)}")
                    continue
                nxt[-1] += 1
                nr, nc = r + DIRS[d][0], c + DIRS[d][1]
                if 0 <= nr < R and 0 <= nc < C and (nr, nc) not in on_path and board[nr][nc] == word[len(path)]:
                    path.append((nr, nc))
                    nxt.append(0)
                    on_path.add((nr, nc))
                    if trace is not None:
                        trace.append(f"push {(nr, nc)} for '{word[len(path) - 1]}'")
    return False


def exist_rec(board, word):
    """The Q9 style recursion: one frame per letter."""
    R, C = len(board), len(board[0])
    on_path = set()

    def go(r, c, k):
        if board[r][c] != word[k] or (r, c) in on_path:
            return False
        if k == len(word) - 1:
            return True
        on_path.add((r, c))
        for dr, dc in DIRS:
            nr, nc = r + dr, c + dc
            if 0 <= nr < R and 0 <= nc < C and go(nr, nc, k + 1):
                return True
        on_path.discard((r, c))                       # undo on the way back
        return False

    return any(go(r, c, 0) for r in range(R) for c in range(C))


def serpentine(rows_of_a, width):
    """One-cell-wide winding corridor of 'a' inside a border of 'b'. Returns (board, number of a cells)."""
    rows = []
    for i in range(2 * rows_of_a - 1):
        if i % 2 == 0:
            rows.append("a" * width)
        elif (i // 2) % 2 == 0:
            rows.append("b" * (width - 1) + "a")
        else:
            rows.append("a" + "b" * (width - 1))
    return rows, sum(r.count("a") for r in rows)


# dry run
tr = []
print("dry run board=['aab','bba'] word='aba':", exist_iter(["aab", "bba"], "aba", tr))
print("\n".join("  " + t for t in tr))

for b, w, want in [(["aab", "bba"], "aba", True), (["abc"], "cba", True), (["abc"], "abca", False),
                   (["aaaa"], "aaaa", True), (["ab", "ca"], "acb", False)]:
    assert exist_iter(b, w) == exist_rec(b, w) == want, (b, w)
    print(b, w, "->", exist_iter(b, w))

# the recursion limit, observed on this machine (Python %s)
print("python", sys.version.split()[0], "default recursion limit", sys.getrecursionlimit())
row = ["a" * 1500]
try:
    exist_rec(row, "a" * 1500)
except RecursionError as e:
    print("recursive, 1 x 1500:", type(e).__name__ + ":", e)
print("recursive, 1 x 300:", exist_rec(["a" * 300], "a" * 300))
print("iterative, 1 x 1500:", exist_iter(row, "a" * 1500), "| 1 x 1500 word of 1501:", exist_iter(row, "a" * 1501))

board, n_a = serpentine(25, 40)
cells = len(board) * len(board[0])
print(f"serpentine {len(board)} x {len(board[0])} = {cells} cells, {n_a} cells of 'a'")
print("iterative, word = 'a' * %d:" % n_a, exist_iter(board, "a" * n_a), "| word = 'a' * %d:" % (n_a + 1), exist_iter(board, "a" * (n_a + 1)))
assert exist_iter(board, "a" * n_a) is True and exist_iter(board, "a" * (n_a + 1)) is False
try:
    exist_rec(board, "a" * n_a)
except RecursionError:
    print("recursive on the same corridor: RecursionError")

# raising the limit: an observation about this machine and version, not a guarantee
old = sys.getrecursionlimit()
sys.setrecursionlimit(5000)
print("recursive, 1 x 1500 with limit 5000:", exist_rec(row, "a" * 1500))
sys.setrecursionlimit(old)

# seeded random cross-check of iterative vs recursive Q9 on small boards
for _ in range(600):
    r, c = random.randint(1, 4), random.randint(1, 4)
    al = random.choice(["ab", "abc", "a"])
    b = ["".join(random.choice(al) for _ in range(c)) for _ in range(r)]
    w = "".join(random.choice(al) for _ in range(random.randint(1, min(8, 2 * r * c))))
    assert exist_iter(b, w) == exist_rec(b, w), (b, w)
print("600 seeded random boards: iterative == recursive")
assert not exist_iter(["abc", "xxx"], "abcb") and not exist_rec(["abc", "xxx"], "abcb")
assert exist_iter(["a"], "a") and not exist_iter(["a"], "aa") and not exist_iter(["ab"], "ba" + "a")
print("edge asserts ok")
